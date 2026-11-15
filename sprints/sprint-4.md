# Sprint 4 Report: Documentation, Narrative and Submission

> **Navigation:** [← Sprint 3](./sprint-3.md) | [Sprint Index](./README.md)

| Field | Value |
| :--- | :--- |
| **Project** | AZURA - SPHEREx Sky Movie |
| **Sprint Number** | 4 of 4 |
| **Sprint Window** | 15 November 2026, 16:00 – 22:00 (6 hours) |
| **Scrum Master** | Sezai Efe Sabırsız (`@sezaief`) |
| **Story Points** | **21 Planned** / **19 Delivered** (2 Carried/Blocked) |
| **Status** | ✅ Closed |

---

## 1. Team and Contribution

| Member | Handle | Role on Space Apps Roster | Work Assigned | Contribution |
| :--- | :--- | :--- | :--- | :---: |
| **Sezai Efe Sabırsız** | `@sezaief` | Team Owner, Scrum Master, Developer, Researcher, Technical Writer, Presenter | All tasks | **100%** |
| Alperen Bektaş | `@alpbktss` | Team member | None | 0% |
| Emre Çeltikoğlu | `@emre_bok` | Team member | None | 0% |

---

## 2. Sprint Goal

Convert a working prototype into a submission that a judge can evaluate without the author in the room: a public repository, a written explanation of the science, a short video, and four sprint reports.

---

## 3. Product Backlog

| ID | User Story | Priority | SP | Status |
| :---: | :--- | :---: | :---: | :---: |
| **US-16** | As a judge I want a public landing page and a hosted instance so that I do not have to run Python myself. | Must | 2 | ✅ Done |
| **US-17** | As a judge I want a README that states the problem, the data source and the limits so that I can judge the work honestly. | Must | 3 | ✅ Done |
| **US-18** | As a technical reviewer I want an engineering document describing the pipeline so that the code can be maintained after the event. | Should | 5 | ✅ Done |
| **US-19** | As an organiser I want four sprint reports with a consistent structure so that process tracking is possible. | Must | 5 | ✅ Done |
| **US-20** | As a presenter I want a three-minute video script that fits the time limit so that the demo cannot overrun. | Must | 3 | ✅ Done |
| **US-21** | As a maintainer I want issue templates and a board proposal so that the repository looks like a project rather than a folder. | Could | 1 | ✅ Done |
| **US-22** | As a team we want the four-target live run recorded as evidence. | Must | 2 | ⛔ Carried (upstream unavailable) |

---

## 4. User Stories and Acceptance Criteria

<details>
<summary><strong>Click to expand Acceptance Criteria (US-16 to US-21)</strong></summary>

### US-16 — Public Entry Points
- [x] Static landing page served from `docs/index.html`.
- [x] Hosted instance runs the application without local install.
- [x] Both links appear in the root `README.md`.

### US-17 — README
- [x] States challenge, 4 demonstration targets, and coordinate format.
- [x] States data source (IRSA SPHEREx) and MIT licence.
- [x] Explicitly states known limitation regarding upstream availability.

### US-18 — Engineering Document
- [x] Describes request flow from coordinate to image.
- [x] Lists every endpoint with parameters and failure behaviour.
- [x] Records verification commands used during the event.

### US-19 — Sprint Reports
- [x] Consistent structure across Sprints 1–4 (goal, backlog, tasks, daily notes, review, retrospective, burndown).
- [x] Every task lists Sezai Efe Sabırsız as assignee.

### US-20 — Video Script
- [x] Opens with the problem in one sentence.
- [x] Demonstrates coordinate entry, movie playback, Difference view, and spectrum.
- [x] Plainly states which data source is on screen and closes with data sources and licence.

### US-21 — Repository Governance
- [x] Issue templates and project board structure added under `.github/`.

</details>

---

## 5. Task Breakdown

| Task | Description | Assignee | Est. | Status | Evidence |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **T4.1** | Static landing page content review and link check | `@sezaief` | 1 h | ✅ Done | `docs/index.html` |
| **T4.2** | README rewrite in two languages with problem, data source & limits | `@sezaief` | 2 h | ✅ Done | Repository root `README.md` |
| **T4.3** | Engineering document with endpoint table and verification log | `@sezaief` | 2 h | ✅ Done | `docs/TEKNIK_DOKUMAN.md` |
| **T4.4** | Project brief for hand-over to other assistants | `@sezaief` | 1 h | ✅ Done | `PROJECT_BRIEF.md` |
| **T4.5** | Sprint reports 1 to 4 | `@sezaief` | 2 h | ✅ Done | `sprints/` |
| **T4.6** | Deployment manifests and workflow verification | `@sezaief` | 1 h | ✅ Done | Pages workflow, `render.yaml` |
| **T4.7** | Issue templates and board proposal | `@sezaief` | 0.5 h | ✅ Done | `.github/ISSUE_TEMPLATE` |
| **T4.8** | Three-minute video script and shot list | `@sezaief` | 1.5 h | ✅ Done | Submission script |
| **T4.9** | Clean-checkout rehearsal: unpack, install, run, open | `@sezaief` | 1 h | ✅ Done | Root path returned HTTP 200 |
| **T4.10** | Final submission package | `@sezaief` | 1 h | ✅ Done | Repository archive and links |
| **T4.11** | Recorded four-target live run | `@sezaief` | 2 h | ⛔ Carried | Upstream archive unavailable |

---

## 6. Daily Scrum Notes

* **15 Nov 2026, 16:00 — Sprint Planning:** 21 SP committed. *Rule accepted:* Nothing is written into a report that cannot be shown from the repository.
* **15 Nov 2026, 18:00:** Done: `T4.2`, `T4.3`, `T4.4`. *Blocker:* README had been written from memory and described outdated features. *Resolution:* Re-read every claim against code and removed outdated sentences.
* **15 Nov 2026, 19:30:** Done: `T4.5`, `T4.7`. Four reports standardized with identical sections for side-by-side reading.
* **15 Nov 2026, 21:00:** Done: `T4.1`, `T4.6`, `T4.9`. Clean checkout rehearsal passed (unpacked to empty folder, installed requirements, started server, root returned 200).
* **15 Nov 2026, 21:45:** Done: `T4.8`, `T4.10`. `T4.11` remains blocked upstream and is documented honestly in the README.

---

## 7. Sprint Review

* **Demonstrated:** Repository tree, landing page, README, engineering document, four sprint reports, and clean-checkout execution.
* **Accepted Evidence:** HTTP 200 from clean copy; consistent section structure across all four sprint reports; endpoint table matching implemented routes.
* **Rejected During Review:** An earlier draft claiming a completed four-target live run was deleted and replaced with an explicit limitation statement. *Quality bar:* Submission must not contain any claim that cannot be reproduced.

---

## 8. Sprint Retrospective

* **Went Well:** Writing reports directly from code artefacts caught three inaccurate claims in the README before submission. Video script forced a crisp narrative: *problem → coordinate → movie → difference → spectrum*.
* **Did Not Go Well:** Documentation started in the final sprint, placing submission packaging on the critical path during the last six hours.
* **Action Items:**
  1. Move documentation into the sprint where each feature is built.
  2. Delete any claim that cannot be reproduced rather than softening it.
  3. State known limitations prominently in the README.

---

## 9. Burndown Data

| Checkpoint | Ideal Remaining SP | Actual Remaining SP |
| :--- | :---: | :---: |
| 15 Nov 16:00 | 21 | 21 |
| 15 Nov 18:00 | 14 | 12 |
| 15 Nov 19:30 | 8 | 7 |
| 15 Nov 21:00 | 4 | 4 |
| 15 Nov 22:00 | 0 | **2** *(blocked item carried)* |

**Sprint 4 Velocity:** 19 SP | **Cumulative Project Velocity:** `21 + 24 + 27 + 19 = 91 SP` delivered (6 SP blocked upstream).
