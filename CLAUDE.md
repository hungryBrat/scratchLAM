# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in this folder.

# LAM Research Challenge 3.0

Competition workspace for the LAM Research Challenge 3.0 (E-Cell IIT Bombay × Lam Research × T-Works).

- `1788509443120-Lam Research Challenge 2026 Qualifier Round Stage1 Questionnaire.pdf`, `LAM_Challenge_3.0_Stage1_Solutions_Q4_Q6.md`: Stage 1 (qualifier), finished.
- `harware_hustle/`: Stage 2 "Hardware Hustle", the current work. The folder name has a typo; keep it, because paths and the build book depend on it.

## Stage 2: start here
Read `harware_hustle/BUILD_PLAN.md` first. It is the complete build plan, generated from the live build book: contract, team roles, milestones and run sheet, P&ID and line list, wiring and pin map, firmware design, calibration, answers, video, risks, and a file map. Its "Quick context" section says where the team's real bench data lives (the build book's database) and how to rebuild and republish.

Key facts:
- Upload by Sun 4 Oct 2026, 18:00 IST; the team targets 16:00.
- Team of four: HY (hydraulics), EF (electronics and firmware), DC (data and calibration), IV (integration, video, submission).
- Rule from the round: "no simulations, no shortcuts". The firmware simulator is a test tool; its output never goes into the video, photos or paper.
- Live build book (private, shared by the owner): https://claude.ai/artifact/GDvmoMtX1gnrWGFqVeGuy9

## Conventions
- The plan's single source of truth is `harware_hustle/plan/content.py` (plus `page_template.html` and `diagrams.py`). Rebuild with `python harware_hustle/plan/build_page.py`; it regenerates the page, the kit, `plan/ROADMAP.md` and `BUILD_PLAN.md`. Never hand-edit those generated files.
- Firmware lives only in `harware_hustle/firmware/lam_flow_rig/src/main.cpp`. After any change: `pio run` with zero warnings, the simulator in `test/` must print ALL PASS, then rebuild and republish the book.
- Python tools need only pyserial, matplotlib and numpy (`harware_hustle/tools/`).
