# Sprint 1 Report: Problem Analysis and Data Access

> **Navigation:** [← Sprint Index](./README.md) | [Sprint 2 →](./sprint-2.md)

| Field | Value |
| :--- | :--- |
| **Project** | AZURA - SPHEREx Sky Movie |
| **Event** | NASA Space Apps Challenge 2026, Niğde Local Event |
| **Challenge** | Planet X and SPHEREx |
| **Sprint Number** | 1 of 4 |
| **Sprint Window** | 14 November 2026, 10:00 – 22:00 (12 hours) |
| **Scrum Master** | Sezai Efe Sabırsız (`@sezaief`) |
| **Team Size** | 3 members (1 active) |
| **Story Points** | **21 Planned** / **21 Delivered** (0 Carry-over) |
| **Status** | ✅ Closed |

---

## 1. Team and Contribution

| Member | Handle | Role | Work Assigned | Contribution |
| :--- | :--- | :--- | :--- | :---: |
| **Sezai Efe Sabırsız** | `@sezaief` | Team Owner, Scrum Master, Developer, Researcher | All tasks | **100%** |
| Alperen Bektaş | `@alpbktss` | Team member (registration only) | None | 0% |
| Emre Çeltikoğlu | `@emre_bok` | Team member (registration only) | None | 0% |

> *Note: Both additional roster members produced no commits, code, research, documentation, or reviews. Every task was executed by the Scrum Master alone.*

---

## 2. Sprint Goal

Prove that the **Planet X and SPHEREx** challenge can be solved with publicly reachable SPHEREx data, and stand up a repository that serves a working page and one machine-readable data endpoint.

---

## 3. Product Backlog

| ID | User Story | Priority | SP | Status |
| :---: | :--- | :---: | :---: | :---: |
| **US-01** | As a judge I want a public page that opens with one click so that I can start exploring without installing software. | Must | 5 | ✅ Done |
| **US-02** | As an astronomer I want to type a Right Ascension, a Declination and a field of view so that the tool shows the piece of sky I care about. | Must | 5 | ✅ Done |
| **US-03** | As a front-end developer I want one endpoint that returns the list of SPHEREx epochs covering a coordinate so that the browser never talks to IRSA directly and never hits CORS. | Must | 8 | ✅ Done |
| **US-04** | As a team I want a repository with a licence and a README so that the submission has a permanent, citable link. | Should | 3 | ✅ Done |

---

## 4. User Stories and Acceptance Criteria

<details>
<summary><strong>Click to expand Acceptance Criteria (US-01 to US-04)</strong></summary>

### US-01 — Public Page
- [x] Given the Flask application is running, opening `/` returns HTTP 200 with a rendered control panel and image stage.
- [x] The page contains inputs for RA, Dec, FOV, and band, and lists the four demonstration targets.
- [x] No build tool, package manager, or install step is required in the browser.

### US-02 — Coordinate Entry and Field of View
- [x] RA is accepted in degrees (`0` to `360`), Dec in degrees (`-90` to `+90`), FOV in degrees.
- [x] Invalid input produces a readable message, never a stack trace.
- [x] The same state is expressible as URL parameters so a link can be shared.

### US-03 — Epoch List Endpoint
- [x] `GET /api/query?ra=&dec=&size=&band=&limit=` returns JSON with an ordered list of `{uri, time}` objects.
- [x] The list is ordered by observation time, ascending.
- [x] The endpoint always returns JSON, including on failure.

### US-04 — Repository
- [x] MIT licence present at the repository root.
- [x] README states what the tool does, how to run it, and which data source it uses.
- [x] `.gitignore` excludes caches, logs, and compiled files.

</details>

---

## 5. Task Breakdown

| Task | Description | Assignee | Est. | Status | Evidence |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **T1.1** | Read challenge statement, extract 4 test targets & considerations | `@sezaief` | 2 h | ✅ Done | Notes in repository brief |
| **T1.2** | Discover IRSA SPHEREx table structure used for cone search | `@sezaief` | 2 h | ✅ Done | ADQL over `spherex.artifact` joined to `spherex.plane` |
| **T1.3** | Run a live TAP smoke test against IRSA for a real coordinate | `@sezaief` | 2 h | ✅ Done | Cutout URLs returned for test position |
| **T1.4** | Build the Flask skeleton and the epoch list endpoint | `@sezaief` | 4 h | ✅ Done | `app.py`, `GET /api/query` |
| **T1.5** | Initialise the repository, MIT licence, `.gitignore`, README | `@sezaief` | 2 h | ✅ Done | Repository root files |
| **T1.6** | Collect the four target coordinates from published values | `@sezaief` | 1 h | ✅ Done | Presets for Barnard's Star, WISE 0855, Epsilon Indi B, RW Aurigae |
| **T1.7** | Verify the endpoint contract with `curl` | `@sezaief` | 1 h | ✅ Done | HTTP 200 and valid JSON |

---

## 6. Daily Scrum Notes

* **14 Nov 2026, 10:00 — Sprint Planning:** Goal accepted. Backlog of 21 SP agreed. No impediments. *Decision:* The browser must never call IRSA directly; all remote access goes through the Flask server.
* **14 Nov 2026, 14:00:** Done: challenge statement broken down, four targets extracted. In progress: TAP schema discovery. *Blocker:* Public documentation page does not publish ADQL table names, so the join was reconstructed from a worked example in the IRSA tutorial.
* **14 Nov 2026, 18:00:** Done: `T1.2`, `T1.3`. Working query joins `spherex.artifact` and `spherex.plane` on `planeid`, filters with `CONTAINS(POINT('ICRS', ra, dec), p.poly)`, selects band with `p.energy_bandpassname`, and appends `?center=ra,decd&size=deg`. In progress: `T1.4`.
* **14 Nov 2026, 21:30:** Done: `T1.4` to `T1.7`. Endpoint returns an ordered epoch list for the test coordinate. *Next sprint:* Turn those epochs into pictures.

---

## 7. Sprint Review

* **Demonstrated:** Opening the page, entering a coordinate, and receiving an ordered list of SPHEREx observation epochs for that position.
* **Accepted Evidence:** HTTP 200 on root path; JSON payload from `/api/query` containing cutout URIs and observation times.
* **Feedback Recorded:**
  1. A list of epochs is not yet a product; the challenge asks for a tool showing how the sky changes, not a catalogue browser.
  2. Interface must assume a judge with no astronomy background.
  3. *Risk raised:* Epoch endpoint depends on a single remote service being up.

---

## 8. Sprint Retrospective

* **Went Well:** Data access was solved early before UI work. Building the query from a worked example saved hours. Server-side remote queries eliminated browser CORS issues.
* **Did Not Go Well:** First TAP attempt timed out and initially looked like a malformed query. Undocumented table names required reverse-engineering.
* **Action Items:**
  1. Every remote call must carry a timeout and a retry.
  2. Every failure path returns JSON, never HTML.
  3. Build a local fallback so the interface can be demonstrated when the remote service is down.

---

## 9. Burndown Data

| Checkpoint | Ideal Remaining SP | Actual Remaining SP |
| :--- | :---: | :---: |
| 14 Nov 10:00 | 21 | 21 |
| 14 Nov 14:00 | 16 | 17 |
| 14 Nov 18:00 | 11 | 10 |
| 14 Nov 22:00 | 0 | **0** |

---

## 10. Definition of Done

- [x] Code runs from a clean checkout with documented commands.
- [x] Endpoint returns JSON in both success and failure cases.
- [x] Repository contains a licence and a README.
- [x] Behaviour was demonstrated at the sprint review.
