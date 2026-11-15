import requests

timeout = 25
urls = [
    "https://irsa.ipac.caltech.edu/SIA?COLLECTION=spherex_dr1&POS=269.452,4.6933&SIZE=0.5",
    "https://irsa.ipac.caltech.edu/SIA?COLLECTION=spherex&POS=269.452,4.6933&SIZE=0.5",
    "https://irsa.ipac.caltech.edu/cgi-bin/SIA/nph-sia?COLLECTION=spherex_dr1&POS=269.452,4.6933&SIZE=0.5",
    "https://irsa.ipac.caltech.edu/ibe/search/spherex/dr1/level2?POS=269.452,4.6933&SIZE=0.5",
    "https://irsa.ipac.caltech.edu/ibe/search/spherex/qr3/level2?POS=269.452,4.6933&SIZE=0.5",
    "https://irsa.ipac.caltech.edu/applications/spherex/",
    "https://irsa.ipac.caltech.edu/ibe/data/spherex/dr1/level2/2025W18_1B/l2b-v27-2026-196/4/level2_2025W18_1B_0023_2D4_spx_l2b-v27-2026-196.fits?center=305.59875000000005,41.14888888888889d&size=0.01",
]
for u in urls:
    try:
        r = requests.get(u, timeout=timeout, stream=True)
        chunk = r.raw.read(240)
        print("---", r.status_code, r.headers.get("content-type"), u[:110])
        print(chunk[:220])
    except Exception as e:
        print("--- EXC", type(e).__name__, u[:90], e)
