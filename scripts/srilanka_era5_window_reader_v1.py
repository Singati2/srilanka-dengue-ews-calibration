"""Windowed reads of ARCO-ERA5 raw single-level files (classic netCDF-3, 64-bit offset).

These files are contiguous int16 with scale_factor/add_offset, shape (24, 721, 1440). Because the
layout is contiguous and lon is the fastest axis, the lat rows we want form ONE contiguous byte span
per timestep -- so a Sri Lanka window costs 24 range requests per file instead of a 50 MB download.

Header parsing is deliberately explicit rather than delegated: scipy/xarray both want the whole file.
"""
import struct
import numpy as np

BASE = ("https://storage.googleapis.com/gcp-public-data-arco-era5/"
        "raw/date-variable-single_level/%04d/%02d/%02d/%s/surface.nc")

NC_BYTE, NC_CHAR, NC_SHORT, NC_INT, NC_FLOAT, NC_DOUBLE = 1, 2, 3, 4, 5, 6
TYPESIZE = {NC_BYTE: 1, NC_CHAR: 1, NC_SHORT: 2, NC_INT: 4, NC_FLOAT: 4, NC_DOUBLE: 8}
NPTYPE = {NC_BYTE: ">i1", NC_CHAR: "S1", NC_SHORT: ">i2", NC_INT: ">i4",
          NC_FLOAT: ">f4", NC_DOUBLE: ">f8"}


class _R:
    def __init__(self, b): self.b, self.p = b, 0
    def u32(self):
        v = struct.unpack_from(">I", self.b, self.p)[0]; self.p += 4; return v
    def u64(self):
        v = struct.unpack_from(">Q", self.b, self.p)[0]; self.p += 8; return v
    def name(self):
        n = self.u32()
        s = self.b[self.p:self.p + n].decode("utf-8", "replace")
        self.p += n + (-n % 4)                      # 4-byte padding
        return s
    def values(self, nc_type, n):
        sz = TYPESIZE[nc_type] * n
        raw = self.b[self.p:self.p + sz]
        self.p += sz + (-sz % 4)
        if nc_type == NC_CHAR:
            return raw.decode("utf-8", "replace")
        return np.frombuffer(raw, dtype=NPTYPE[nc_type])
    def atts(self):
        tag, n = self.u32(), self.u32()
        out = {}
        for _ in range(n):
            k = self.name()
            t = self.u32()
            out[k] = self.values(t, self.u32())
        return out


def parse_header(buf):
    """-> dict of varname -> {begin, nc_type, shape, atts}; needs only the first few KB."""
    r = _R(buf)
    assert buf[:3] == b"CDF", "not a classic netCDF"
    offs64 = buf[3] == 2
    r.p = 4
    r.u32()                                          # numrecs

    tag, ndims = r.u32(), r.u32()                    # dim_list
    dims = []
    for _ in range(ndims):
        dims.append((r.name(), r.u32()))

    r.atts()                                         # global atts

    tag, nvars = r.u32(), r.u32()                    # var_list
    out = {}
    for _ in range(nvars):
        nm = r.name()
        nd = r.u32()
        dimids = [r.u32() for _ in range(nd)]
        r.atts.__self__  # noqa  (keep linters quiet about the bound method)
        atts = r.atts()
        nc_type = r.u32()
        r.u32()                                      # vsize
        begin = r.u64() if offs64 else r.u32()
        out[nm] = dict(begin=begin, nc_type=nc_type, atts=atts,
                       shape=tuple(dims[i][1] for i in dimids))
    return out


def lat_lon_index(lat_hi, lat_lo, lon_w, lon_e, nlat=721, nlon=1440, res=0.25):
    """ERA5: lat descends 90..-90, lon ascends 0..359.75."""
    i0 = int(np.floor((90.0 - lat_hi) / res))
    i1 = int(np.ceil((90.0 - lat_lo) / res))
    j0 = int(np.floor(lon_w / res))
    j1 = int(np.ceil(lon_e / res))
    return i0, i1, j0, j1


def read_window(session, url, var, i0, i1, j0, j1, hdr=None):
    """Fetch (24, i1-i0+1, j1-j0+1) decoded floats using one range request per timestep."""
    if hdr is None:
        hdr = parse_header(_get(session, url, 0, 16383))
    v = hdr[var]
    nt, nlat, nlon = v["shape"]
    isz = TYPESIZE[v["nc_type"]]
    rowb = nlon * isz
    nrow = i1 - i0 + 1

    out = np.empty((nt, nrow, j1 - j0 + 1), dtype="float64")
    for t in range(nt):
        start = v["begin"] + t * nlat * rowb + i0 * rowb
        raw = _get(session, url, start, start + nrow * rowb - 1)
        a = np.frombuffer(raw, dtype=NPTYPE[v["nc_type"]]).reshape(nrow, nlon)
        out[t] = a[:, j0:j1 + 1]

    sf = v["atts"].get("scale_factor")
    ao = v["atts"].get("add_offset")
    if sf is not None:
        out = out * float(np.asarray(sf).ravel()[0])
    if ao is not None:
        out = out + float(np.asarray(ao).ravel()[0])
    return out


def _get(session, url, a, b):
    r = session.get(url, headers={"Range": "bytes=%d-%d" % (a, b)}, timeout=60)
    r.raise_for_status()
    return r.content
