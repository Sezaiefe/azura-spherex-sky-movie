"""
AZURA -- SPHEREx Sky Movie (Planet X & SPHEREx, NASA Space Apps 2026)
Minimal Flask proxy: TAP query -> cutout URLs -> PNG frames -> blink movie.

v4 fixes (15 Nov 2026):
  - ALL /api/* endpoints now ALWAYS return JSON with a consistent schema:
    {ok: bool, frames: [...], error: str|null, ...} -- even on bad input,
    so the frontend never meets an HTML error page or a 500 without JSON.
  - input validation on ra/dec/size/band/limit (no more ValueError 500s).
  - retries with backoff in _fetch() (IRSA intermittently drops requests).
  - memory cache of decoded FITS arrays + disk/memory PNG cache:
    replays and difference frames are computed from cached arrays.
  - /favicon.ico returns 204 (no more 404 noise in logs).
"""
import hashlib
import io
import json
import os
import re
import time
from collections import OrderedDict

import numpy as np
import requests
from astropy.utils.data import conf
from flask import Flask, Response, jsonify, request, send_from_directory

conf.remote_timeout = 120  # SPHEREx files can be slow to read

from astropy.io import fits
from astroquery.ipac.irsa import Irsa
from PIL import Image

app = Flask(__name__, static_folder="static", static_url_path="")

BASE_DIR = os.path.dirname(__file__)
DEMO_CACHE = os.path.join(BASE_DIR, "data", "demo_cutouts.json")
PNG_DIR = os.path.join(BASE_DIR, "data", "cache")
os.makedirs(PNG_DIR, exist_ok=True)

_MEM_PNG: dict[str, bytes] = {}                           # cache_key -> png bytes
_ARR_CACHE: OrderedDict[str, np.ndarray] = OrderedDict()  # uri -> 2D array
_ARR_CACHE_MAX = 300

_BAND_RE = re.compile(r"^SPHEREx-D[1-6]$")  # only the six detector bandpasses


def _remember_array(uri: str, arr: np.ndarray) -> None:
    _ARR_CACHE[uri] = arr
    _ARR_CACHE.move_to_end(uri)
    while len(_ARR_CACHE) > _ARR_CACHE_MAX:
        _ARR_CACHE.popitem(last=False)


# ---------------------------------------------------------------- static ----
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/favicon.ico")
def favicon():
    return Response(status=204)


# ------------------------------------------------------------------ TAP -----
TAP_TEMPLATE = """
SELECT TOP {limit}
    'https://irsa.ipac.caltech.edu/' || a.uri || '?center={ra},{dec}d&size={size}' AS uri,
    p.time_bounds_lower AS obs_time
FROM spherex.artifact a
JOIN spherex.plane p ON a.planeid = p.planeid
WHERE 1 = CONTAINS(POINT('ICRS', {ra}, {dec}), p.poly)
  AND p.energy_bandpassname = '{band}'
ORDER BY p.time_bounds_lower
"""


def _num(args: dict, name: str, default=None, lo=None, hi=None):
    """Parse a float query param; raise ValueError with a clean message."""
    raw = args.get(name)
    if raw is None or raw == "":
        if default is None:
            raise ValueError(f"missing required parameter '{name}'")
        raw = default
    try:
        val = float(raw)
    except (TypeError, ValueError):
        raise ValueError(f"parameter '{name}' must be a number, got '{raw}'")
    if lo is not None and val < lo:
        raise ValueError(f"parameter '{name}' must be >= {lo}")
    if hi is not None and val > hi:
        raise ValueError(f"parameter '{name}' must be <= {hi}")
    return val


def _int_num(args: dict, name: str, default: int, lo: int, hi: int) -> int:
    raw = args.get(name, default)
    try:
        val = int(float(raw))
    except (TypeError, ValueError):
        raise ValueError(f"parameter '{name}' must be an integer, got '{raw}'")
    return max(lo, min(hi, val))


@app.route("/api/query")
def api_query():
    try:
        ra = _num(request.args, "ra", lo=0.0, hi=360.0)
        dec = _num(request.args, "dec", lo=-90.0, hi=90.0)
        size = _num(request.args, "size", default=0.1, lo=0.01, hi=1.5)
        band = request.args.get("band", "SPHEREx-D2")
        if not _BAND_RE.match(band):
            return jsonify({"ok": False, "frames": [],
                            "error": f"unknown band '{band}' (use SPHEREx-D1..D6)"})
        limit = _int_num(request.args, "limit", default=40, lo=1, hi=200)

        query = TAP_TEMPLATE.format(ra=ra, dec=dec, size=size, band=band, limit=limit)
        try:
            res = Irsa.query_tap(query)
        except Exception as exc:  # noqa: BLE001 -- IRSA down / sandbox blocked
            demo: dict = {"ok": True, "demo": True, "frames": [],
                          "error": f"IRSA unreachable: {exc}"}
            if os.path.exists(DEMO_CACHE):
                with open(DEMO_CACHE) as fh:
                    cached = json.load(fh)
                    demo["frames"] = cached.get("frames", [])
            return jsonify(demo)

        rows = [{"uri": str(r["uri"]), "time": str(r["obs_time"]), "demo": False}
                for r in res]
        if not rows:
            return jsonify({"ok": True, "frames": [],
                            "error": "no SPHEREx images cover this position (yet)"})
        return jsonify({"ok": True, "frames": rows, "band": band,
                        "ra": ra, "dec": dec, "error": None})
    except ValueError as exc:
        return jsonify({"ok": False, "frames": [], "error": str(exc)}), 400
    except Exception as exc:  # noqa: BLE001 -- last resort, still JSON
        return jsonify({"ok": False, "frames": [],
                        "error": f"unexpected server error: {exc}"}), 500


# ---------------------------------------------------------------- pixels ----
def _fetch(uri: str, tries: int = 3) -> bytes:
    """Download with retries + backoff (IRSA intermittently drops requests)."""
    last: Exception | None = None
    for attempt in range(tries):
        try:
            r = requests.get(uri, timeout=120)
            r.raise_for_status()
            return r.content
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(1.5 * (attempt + 1))  # 1.5s, 3s, 4.5s
    assert last is not None
    raise last


def _image_array(uri: str) -> np.ndarray:
    """Decode FITS to a 2D array, with a bounded memory cache."""
    if uri in _ARR_CACHE:
        _ARR_CACHE.move_to_end(uri)
        return _ARR_CACHE[uri]
    with fits.open(io.BytesIO(_fetch(uri))) as hdul:
        for hdu in hdul:
            data = getattr(hdu, "data", None)
            if data is not None and getattr(data, "ndim", 0) == 2:
                arr = np.array(data, dtype=float)
                _remember_array(uri, arr)
                return arr
    raise ValueError("no 2D image HDU found in this file")


def _stretch(img: np.ndarray, lo=1.0, hi=99.5) -> np.ndarray:
    img = np.nan_to_num(img, nan=0.0, posinf=0.0, neginf=0.0)
    vmin, vmax = np.percentile(img, [lo, hi])
    span = max(vmax - vmin, 1e-9)
    norm = np.clip((img - vmin) / span, 0.0, 1.0)
    return (np.sqrt(norm) * 255).astype(np.uint8)  # sqrt ~ asinh stretch


def _png_bytes(arr: np.ndarray, side=384) -> bytes:
    im = Image.fromarray(arr).resize((side, side))
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    return buf.getvalue()


def _cached_png(cache_key: str, render) -> Response:
    """Serve rendered PNG from memory/disk cache; render+store only on miss."""
    png = _MEM_PNG.get(cache_key)
    if png is None:
        path = os.path.join(PNG_DIR, f"{cache_key}.png")
        if os.path.exists(path):
            with open(path, "rb") as fh:
                png = fh.read()
        else:
            png = render()
            with open(path, "wb") as fh:
                fh.write(png)
        _MEM_PNG[cache_key] = png
    return Response(png, mimetype="image/png",
                    headers={"Cache-Control": "public, max-age=86400"})


def _key(*parts: str) -> str:
    return hashlib.md5("|".join(parts).encode()).hexdigest()


# --------------------------------------------------------------- cutout -----
@app.route("/api/cutout")
def api_cutout():
    uri = (request.args.get("uri") or "").strip()
    if not uri.startswith("https://irsa.ipac.caltech.edu/"):
        return jsonify({"ok": False,
                        "error": "parameter 'uri' must be an IRSA image URL"}), 400
    key = _key("cutout", uri)

    def render() -> bytes:
        return _png_bytes(_stretch(_image_array(uri)))

    try:
        return _cached_png(key, render)
    except Exception as exc:  # noqa: BLE001
        return jsonify({"ok": False, "error": str(exc)}), 502


@app.route("/api/difference")
def api_difference():
    uri1 = (request.args.get("uri1") or "").strip()
    uri2 = (request.args.get("uri2") or "").strip()
    for u in (uri1, uri2):
        if not u.startswith("https://irsa.ipac.caltech.edu/"):
            return jsonify({"ok": False,
                            "error": "parameters 'uri1' and 'uri2' must be IRSA image URLs"}), 400
    key = _key("diff", uri1, uri2)

    def render() -> bytes:
        a = _image_array(uri1)   # served from memory cache after first use
        b = _image_array(uri2)
        diff = b - a             # moving sources appear as dipole pairs
        return _png_bytes(_stretch(diff, lo=5.0, hi=95.0))

    try:
        return _cached_png(key, render)
    except Exception as exc:  # noqa: BLE001
        return jsonify({"ok": False, "error": str(exc)}), 502


# -------------------------------------------------------------- spectrum ----
@app.route("/api/spectrum")
def api_spectrum():
    """STRETCH GOAL -- center-pixel flux vs wavelength across the 102 bands.

    Uses one MEF per detector bandpass (SPHEREx-D1..D6); the center pixel of
    each cutout gives a crude low-resolution spectrum. Experimental.
    """
    try:
        ra = _num(request.args, "ra", lo=0.0, hi=360.0)
        dec = _num(request.args, "dec", lo=-90.0, hi=90.0)
        size = _num(request.args, "size", default=0.05, lo=0.01, hi=0.5)
    except ValueError as exc:
        return jsonify({"ok": False, "points": [], "error": str(exc)}), 400

    points: list[dict] = []
    try:
        for det in ["SPHEREx-D1", "SPHEREx-D2", "SPHEREx-D3",
                    "SPHEREx-D4", "SPHEREx-D5", "SPHEREx-D6"]:
            q = TAP_TEMPLATE.format(ra=ra, dec=dec, size=size, band=det, limit=1)
            res = Irsa.query_tap(q)
            if len(res) == 0:
                continue
            uri = str(res[0]["uri"])
            data = _image_array(uri)
            cy, cx = np.array(data.shape) // 2
            flux = float(data[cy, cx])
            wave = None
            try:
                from astropy.wcs import WCS
                with fits.open(io.BytesIO(_fetch(uri))) as hdul:
                    for hdu in hdul:
                        if getattr(hdu, "data", None) is not None:
                            w = WCS(hdu.header, fobj=hdul, key="W")
                            wave = float(w.pixel_to_world(cx, cy).to("um").value)
                            break
            except Exception:  # noqa: BLE001
                wave = None
            if wave:
                points.append({"wavelength_um": wave, "flux": flux,
                               "detector": det})
        points.sort(key=lambda p: p["wavelength_um"])
        return jsonify({"ok": True, "points": points, "error": None})
    except Exception as exc:  # noqa: BLE001
        return jsonify({"ok": False, "points": points,
                        "error": f"spectrum unavailable: {exc}"}), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
