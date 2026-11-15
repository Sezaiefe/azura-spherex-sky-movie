# Sprint 3 Report: Difference Imaging, Spectrum and an Offline-Safe Demo

> **Navigation:** [← Sprint 2](./sprint-2.md) | [Sprint Index](./README.md) | [Sprint 4 →](./sprint-4.md)

| Field | Value |
| :--- | :--- |
| **Project** | AZURA - SPHEREx Sky Movie |
| **Sprint Number** | 3 of 4 |
| **Sprint Window** | 15 November 2026, 06:00 – 16:00 (10 hours) |
| **Scrum Master** | Sezai Efe Sabırsız (`@sezaief`) |
| **Story Points** | **29 Planned** / **27 Delivered** (2 Carried) |
| **Status** | ✅ Closed |

---

## 1. Team and Contribution

| Member | Handle | Role | Work Assigned | Contribution |
| :--- | :--- | :--- | :--- | :---: |
| **Sezai Efe Sabırsız** | `@sezaief` | Team Owner, Scrum Master, Developer, Researcher, Technical Writer | All tasks | **100%** |
| Alperen Bektaş | `@alpbktss` | Team member | None | 0% |
| Emre Çeltikoğlu | `@emre_bok` | Team member | None | 0% |

---

## 2. Sprint Goal

Make change detection and spectral information usable by a judge with no astronomy background, and make the product demonstrable even while the upstream archive is unavailable.

---

## 3. Product Backlog

| ID | User Story | Priority | SP | Status |
| :---: | :--- | :---: | :---: | :---: |
| **US-11** | As a judge I want a Difference view of two epochs so that an object that moved becomes obvious instead of something I have to spot by eye. | Must | 8 | ✅ Done |
| **US-12** | As a scientist I want a quick spectrum of the target across the SPHEREx detector bands so that the tool shows more than a picture. | Should | 5 | ✅ Done |
| **US-13** | As a demonstrator I want the product to keep working when the archive is down so that the submission can be shown on any machine. | Must | 8 | ✅ Done |
| **US-14** | As a user I want every failure to appear as a readable sentence so that I am never shown a stack trace. | Must | 3 | ✅ Done |
| **US-15** | As a security-minded reviewer I want the proxy to refuse foreign URLs so that it cannot be used to fetch arbitrary hosts. | Should | 3 | ✅ Done |
| **US-16** | As a judge I want a public landing page and a hosted instance so that I do not have to run Python. | Must | 2 | ⚠️ Carried to Sprint 4 |

---

## 4. User Stories and Acceptance Criteria

<details>
<summary><strong>Click to expand Acceptance Criteria (US-11 to US-15)</strong></summary>

### US-11 — Difference View
- [x] `GET /api/difference?uri1=&uri2=` returns a PNG computed as `epoch2 - epoch1`, with fixed colour mapping around zero.
- [x] Control is reachable from the playback control bar and never blocks the movie.
- [x] When either frame cannot be retrieved, returns a JSON error rather than a broken image element.

### US-12 — Spectrum
- [x] `GET /api/spectrum?ra=&dec=&size=` queries the 6 SPHEREx detector bandpasses and reports flux at target position with wavelength in micrometres (`μm`).
- [x] Points returned as an array of `{wavelength, flux}` pairs.
- [x] When no band yields data, returns an empty array and explanatory message.

### US-13 — Offline-Safe Demo
- [x] When remote query fails, endpoint returns a successful response with a `demo` flag and synthetic sequence of epochs.
- [x] Synthetic sequence contains background stars plus one object displaced by a few pixels per frame.
- [x] Interface states plainly which data source is displayed.

### US-14 — Error Contract
- [x] Missing parameters return `HTTP 400` naming the parameter.
- [x] Non-numeric and out-of-range values rejected before any remote call.
- [x] Band names validated against an explicit allow-list of the six SPHEREx detector names.

### US-15 — Proxy Safety
- [x] Both image endpoints accept only URLs beginning with the archive base path.
- [x] Any other host returns `HTTP 400` and fetches zero bytes.

</details>

---

## 5. Task Breakdown

| Task | Description | Assignee | Est. | Status | Evidence |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **T3.1** | Difference endpoint: fetch both epochs, subtract, colour-map to PNG | `@sezaief` | 3 h | ✅ Done | `GET /api/difference` |
| **T3.2** | Spectra across the six detector bandpasses with wavelength conversion | `@sezaief` | 3 h | ✅ Done | `GET /api/spectrum`, `points[]` |
| **T3.3** | Synthetic epoch generator for the offline demo | `@sezaief` | 2 h | ✅ Done | Noise field, stars, moving object |
| **T3.4** | Validation layer for numeric and enumerated parameters | `@sezaief` | 2 h | ✅ Done | `HTTP 400` with parameter name |
| **T3.5** | Allow-list on proxied URLs | `@sezaief` | 1 h | ✅ Done | Foreign host rejected with `400` |
| **T3.6** | Empty favicon response to stop 404 noise in log | `@sezaief` | 0.5 h | ✅ Done | `HTTP 204` |
| **T3.7** | Static landing page with embedded demo description | `@sezaief` | 3 h | ✅ Done | `docs/index.html` |
| **T3.8** | Deployment manifests for static host and web-service host | `@sezaief` | 2 h | ✅ Done | Pages workflow, `render.yaml` |
| **T3.9** | Endpoint contract test sweep: nine cases | `@sezaief` | 2 h | ✅ Done | All cases returned JSON |
| **T3.10** | Live four-target verification | `@sezaief` | 2 h | ⚠️ Carried | Archive unreachable during sprint |

---

## 6. Daily Scrum Notes

* **15 Nov 2026, 06:00 — Sprint Planning:** 29 SP committed. Carried item stays at top of backlog marked as blocked.
* **15 Nov 2026, 09:00:** Done: `T3.1`. *Blocker:* Subtracting two cutouts with slightly different pointings leaves a residual rim. *Resolution:* Keep comparison honest and document it rather than smoothing it away.
* **15 Nov 2026, 11:30:** Done: `T3.2`, `T3.4`, `T3.5`, `T3.6`. *Blocker:* Initial spectrum implementation was slow querying bands sequentially. *Resolution:* Return partial results when a band fails instead of failing the whole request.
* **15 Nov 2026, 14:00:** Done: `T3.3`, `T3.9`. Synthetic sequence makes movie, difference view, and scrubbing demonstrable offline. Nine contract cases returned consistent JSON.
* **15 Nov 2026, 15:45:** Done: `T3.7`, `T3.8`. `T3.10` remains blocked: queries return gateway error while archive root responds 200, confirming upstream fault.

---

## 7. Sprint Review

* **Demonstrated:** Coordinate entry, playable movie, Difference view isolating the moving object, spectrum panel, and seamless fallback when network is unplugged.
* **Accepted Evidence:** 9-case JSON contract sweep; Difference PNG output; Spectrum wavelength/flux pairs; foreign URL refused with `HTTP 400`.
* **Feedback Recorded:**
  1. Difference view is the strongest single idea in the product because it turns *"look carefully"* into *"watch this"*.
  2. Demo mode must be disclosed to judges, not hidden—honesty is worth more than the illusion of live data.
  3. Deployment is now the critical path.

---

## 8. Sprint Retrospective

* **Went Well:** Offline demo generator turned a blocking dependency into a resilient feature. Centralized validation eliminated stack traces in the UI.
* **Did Not Go Well:** Three separate attempts were spent trying alternate archive endpoints before concluding the fault was upstream.
* **Action Items:**
  1. Classify an outage in a single probe, then trigger fallback.
  2. Write contract tests in the same session as every new endpoint.
  3. Write documentation directly from code artefacts, not memory.

---

## 9. Burndown Data

| Checkpoint | Ideal Remaining SP | Actual Remaining SP |
| :--- | :---: | :---: |
| 15 Nov 06:00 | 29 | 29 |
| 15 Nov 09:00 | 21 | 23 |
| 15 Nov 11:30 | 14 | 12 |
| 15 Nov 14:00 | 7 | 4 |
| 15 Nov 16:00 | 0 | **2** *(blocked item carried)* |
