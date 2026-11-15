# AZURA - SPHEREx Sky Movie

**NASA Space Apps Challenge 2026 — "Planet X and SPHEREx"**
Solo project, built with vanilla HTML5 + JS + Python (Flask). No build step, no framework.

## What it does

A public-facing web tool that turns **SPHEREx spectral-image cutouts** into a
**blink movie**: you enter sky coordinates (RA/Dec), it queries NASA/IPAC IRSA
for every SPHEREx epoch covering that position and animates them in time order,
so moving objects (brown dwarfs, asteroids, high proper-motion stars) pop out
exactly the way Pluto was discovered in 1930.

- Preset high-proper-motion targets: **Barnard's Star**, **WISE 0855**, **Epsilon Indi B**, **RW Aurigae**
- **Difference mode** (epoch N − epoch N−1): moving sources appear as dipole pairs
- **Crude spectrum** (stretch goal): center-pixel flux vs wavelength across all 6 detector bandpasses
- **URL parameters**: `?ra=&dec=&fov=&band=` — shareable/queryable links
- **Aladin Lite** sky background + Gaia/WISE catalog overlay via the Aladin UI

## Stack

| Layer | Tech |
|---|---|
| Frontend | single `static/index.html`, vanilla JS, [Aladin Lite v3](https://aladin.cds.unistra.fr/AladinLite/) (CDS) |
| Backend | Flask (only as a CORS-safe proxy + image stretch) |
| Data | IRSA TAP (`spherex.artifact` × `spherex.plane`) + IRSA cutout service |

## Run locally

```bash
pip install flask requests numpy pillow astropy astroquery
python app.py            # http://localhost:5000
```

First real query takes ~10–60 s (IRSA TAP + first cutout download).
If IRSA is unreachable, the app falls back to `data/demo_cutouts.json`
(cached frame list) and shows a "demo mode" banner.

## Deploy (free tier)

- **Render / Railway / Fly.io**: web service, start command `python app.py`.
- **PythonAnywhere**: works out of the box (Flask app).
- Frontend alone won't work on GitHub Pages (needs the proxy for CORS), but the
  page can point at any deployed instance by visiting
  `https://<host>/?ra=269.4520&dec=4.6933&fov=0.5`.

## Updating for new data releases

Nothing to change: the TAP query runs against `spherex.artifact`/`spherex.plane`,
which IRSA updates weekly. Current searchable releases are **DR1** and **QR3**
(QR2 is superseded). To switch a fixed dataset, swap the TAP table to
`spherex_dr1.artifact` etc.

## Data sources & credits

- SPHEREx Spectral Image MEFs — NASA/IPAC IRSA: https://irsa.ipac.caltech.edu/Missions/spherex.html
- Cutout service docs: https://irsa.ipac.caltech.edu/data/SPHEREx/docs/cutout_tool.html
- Tutorial pattern (TAP query + cutout URL): https://caltech-ipac.github.io/irsa-tutorials/spherex-cutouts/
- Aladin Lite — CDS, Strasbourg

This research has made use of the NASA/IPAC Infrared Science Archive, which is
funded by the National Aeronautics and Space Administration and operated by the
California Institute of Technology.

## License

MIT
