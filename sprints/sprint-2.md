# Sprint 2 Report: From Epoch List to Playable Movie

> **Navigation:** [← Sprint 1](./sprint-1.md) | [Sprint Index](./README.md) | [Sprint 3 →](./sprint-3.md)

| Field | Value |
| :--- | :--- |
| **Project** | AZURA - SPHEREx Sky Movie |
| **Sprint Number** | 2 of 4 |
| **Sprint Window** | 14 November 2026, 22:00 – 15 November 2026, 06:00 (8 hours) |
| **Scrum Master** | Sezai Efe Sabırsız (`@sezaief`) |
| **Story Points** | **26 Planned** / **24 Delivered** (2 Carried) |
| **Status** | ✅ Closed |

---

## 1. Team and Contribution

| Member | Handle | Role | Work Assigned | Contribution |
| :--- | :--- | :--- | :--- | :---: |
| **Sezai Efe Sabırsız** | `@sezaief` | Team Owner, Scrum Master, Developer | All tasks | **100%** |
| Alperen Bektaş | `@alpbktss` | Team member (registration only) | None | 0% |
| Emre Çeltikoğlu | `@emre_bok` | Team member (registration only) | None | 0% |

---

## 2. Sprint Goal

Turn the epoch list into a moving picture: fetch every SPHEREx observation for a coordinate once, render each FITS cutout server-side, and play the sequence back and forth instantly.

---

## 3. Product Backlog

| ID | User Story | Priority | SP | Status |
| :---: | :--- | :---: | :---: | :---: |
| **US-05** | As a judge I want each SPHEREx observation rendered as an image on the page so that I can see the sky instead of a file name. | Must | 8 | ✅ Done |
| **US-06** | As a judge I want to play, pause and scrub the sequence so that I can spot what moves. | Must | 5 | ✅ Done |
| **US-07** | As a judge I want the movie to be smooth after the first load so that scrubbing is not a waiting game. | Must | 5 | ✅ Done |
| **US-08** | As a user I want one-click target presets so that I can start from a known moving object. | Should | 3 | ✅ Done |
| **US-09** | As an operator I want the server to retry and cache so that a single dropped request does not break the movie. | Must | 5 | ✅ Done |
| **US-10** | As a team we want the whole pipeline verified against live IRSA data so that the demo is not a mock-up. | Must | 2 | ⚠️ Carried to Sprint 3 |

---

## 4. User Stories and Acceptance Criteria

<details>
<summary><strong>Click to expand Acceptance Criteria (US-05 to US-09)</strong></summary>

### US-05 — FITS to PNG
- [x] `GET /api/cutout?uri=` downloads the multi-extension FITS cutout, finds the first 2D image array, applies a square-root stretch with percentile clipping, and returns a PNG.
- [x] The rendered image is deterministic for the same input.
- [x] A malformed response never reaches the browser as an HTML error page.

### US-06 — Playback
- [x] Play control toggles between play and pause; label reflects real state.
- [x] Scrub control jumps to any frame immediately.
- [x] Frame counter shows current and total frames (`500 ms` per frame).

### US-07 — Smooth Playback
- [x] All frames are fetched into browser memory before playback starts, showing `loaded / total` progress.
- [x] Scrubbing after preload issues zero network requests.
- [x] Re-requesting a frame is served from browser memory → server memory cache → disk cache.

### US-08 — Presets
- [x] **Barnard's Star:** `RA 269.4520, Dec +4.6933, FOV 0.5`
- [x] **WISE 0855:** `RA 133.7953, Dec -7.2451, FOV 0.5`
- [x] **Epsilon Indi B:** `RA 330.8040, Dec -56.7860, FOV 0.4`
- [x] **RW Aurigae:** `RA 76.9850, Dec +30.4010, FOV 0.2`

### US-09 — Retry and Cache
- [x] Each download attempted up to 3 times with exponential back-off.
- [x] Rendered PNGs are held in server memory and on disk and survive a restart.
- [x] Cached responses carry a 24-hour cache header.

</details>

---

## 5. Task Breakdown

| Task | Description | Assignee | Est. | Status | Evidence |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **T2.1** | FITS download helper with timeout and retry | `@sezaief` | 2 h | ✅ Done | Retry loop, three attempts |
| **T2.2** | Image extraction and square-root stretch to PNG | `@sezaief` | 3 h | ✅ Done | `GET /api/cutout` returns PNG |
| **T2.3** | Two-layer cache: memory and disk | `@sezaief` | 2 h | ✅ Done | Cache directory + in-process store |
| **T2.4** | Frame preloader and progress indicator in the browser | `@sezaief` | 3 h | ✅ Done | Loaded over total counter |
| **T2.5** | Play, pause, scrub and 500 ms frame timer | `@sezaief` | 2 h | ✅ Done | Control bar under stage |
| **T2.6** | Four target presets wired to the query | `@sezaief` | 2 h | ✅ Done | Preset buttons |
| **T2.7** | Guard every frame access against an empty array | `@sezaief` | 1 h | ✅ Done | No uncaught `TypeError` in console |
| **T2.8** | Fix repeated downloads during scrubbing | `@sezaief` | 2 h | ✅ Done | Playback issues no requests after preload |
| **T2.9** | Live end-to-end verification | `@sezaief` | 2 h | ⚠️ Carried | IRSA TAP unreachable during sprint |

---

## 6. Daily Scrum Notes

* **14 Nov 2026, 22:00 — Sprint Planning:** 26 SP committed. Risk accepted: movie depends on remote archive, so caching and preloading are core requirements.
* **15 Nov 2026, 00:30:** Done: `T2.1`, `T2.2`. First FITS cutout rendered to PNG. *Blocker:* Some files had no 2D image extension and crashed the naive reader. *Resolution:* Search all extensions and raise a readable error when none is usable.
* **15 Nov 2026, 03:00:** Done: `T2.3`, `T2.4`. *Blocker:* UI re-downloaded the same frame on every scrub/loop. *Resolution:* Preload all frames once into browser memory.
* **15 Nov 2026, 05:00:** Done: `T2.5`–`T2.8`. Eliminated console `TypeError` on undefined frames by guarding array accesses and resetting on query start.
* **15 Nov 2026, 06:00:** `T2.9` could not be closed: archive returned gateway errors for every query from dev machine. Carried to Sprint 3.

---

## 7. Sprint Review

* **Demonstrated:** Coordinate produces a preloaded sequence, counter advances, playback runs at `500 ms`/frame, scrubbing is instantaneous.
* **Accepted Evidence:** Repeated frame requests disappeared from server logs after preload implementation.
* **Not Accepted:** Live-data playback (full four-target run against live archive remained blocked upstream).

---

## 8. Sprint Retrospective

* **Went Well:** Caching and preloading solved slow first paint and stuttering rewind, making the demo feel like a video player.
* **Did Not Go Well:** ~2 hours lost treating a third-party remote outage as an internal bug.
* **Action Items:**
  1. Distinguish clearly between internal defects and upstream outages in logs and UI.
  2. Ship a local demonstration dataset so the product can be shown offline.
  3. Add a health signal so the UI can report what is unavailable.
