# AZURA — Sprint & Agile Documentation Index

**Project:** AZURA - SPHEREx Sky Movie  
**Event:** NASA Space Apps Challenge 2026 — Niğde Local Event  
**Challenge:** Planet X and SPHEREx  

---

## 📋 Team Roster & Contribution

| Name | Handle | Roster Role | Project Role | Contribution |
| :--- | :--- | :--- | :--- | :---: |
| **Sezai Efe Sabırsız** | `@sezaief` | Team Owner | Scrum Master, Developer, Researcher, Technical Writer, Presenter | **100%** |
| Alperen Bektaş | `@alpbktss` | Team Member | Registration only | 0% |
| Emre Çeltikoğlu | `@emre_bok` | Team Member | Registration only | 0% |

> *Note: All three names, handles, and the "Team Owner" badge reflect the official Space Apps team roster. Every commit, technical artifact, and report was executed by `@sezaief`.*

---

## 🚀 Sprint Index & Velocity Summary

| Sprint | Window (UTC+3) | Goal | Planned SP | Delivered SP | Status | Report |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| **Sprint 1** | 14 Nov 2026, 10:00–22:00 | Prove challenge solvability with public SPHEREx data & stand up repo | 21 | 21 | ✅ Closed | [View Report](./sprint-1.md) |
| **Sprint 2** | 14 Nov 22:00 – 15 Nov 06:00 | Turn the epoch list into a playable, instantly scrubbable movie | 26 | 24 | ✅ Closed | [View Report](./sprint-2.md) |
| **Sprint 3** | 15 Nov 2026, 06:00–16:00 | Difference imaging, spectrum, and an offline-safe demo | 29 | 27 | ✅ Closed | [View Report](./sprint-3.md) |
| **Sprint 4** | 15 Nov 2026, 16:00–22:00 | Documentation, narrative, video script, and submission | 21 | 19 | ✅ Closed | [View Report](./sprint-4.md) |
| **TOTAL** | **36 Hours** | **End-to-End Delivery** | **97 SP** | **91 SP** | **93.8%** | — |

*6 SP (Live 4-target archive verification) carried/blocked due to an upstream IRSA gateway outage.*

---

## 🔭 Product Summary & Known Limitations

* **Product:** AZURA takes a sky coordinate (RA, Dec) and field of view (FOV), retrieves SPHEREx observations, renders FITS cutouts to PNG, and plays them as an interactive movie. Includes a **Difference View** (epoch subtraction) and a **6-band Spectrum Panel**.
* **Demonstration Targets:** Barnard's Star, WISE 0855, Epsilon Indi B, and RW Aurigae.
* **Known Limitation:** During the hackathon, programmatic TAP/cutout queries to the public IRSA archive returned gateway errors (`502/504`) while the root path responded normally. AZURA ships with a **synthetic fallback sequence** (explicitly disclosed in the UI) so playback, difference imaging, and scrubbing remain fully testable offline.

---

## 🛠️ Interactive GitHub Workflow Setup

This package also includes ready-to-use GitHub templates inside `.github/`:
* **Issue Templates** (`.github/ISSUE_TEMPLATE/user_story.yml` & `bug_report.yml`) so you can convert backlog items (`US-01` to `US-22`) directly into trackable GitHub Issues and link them to a **GitHub Projects** board.
