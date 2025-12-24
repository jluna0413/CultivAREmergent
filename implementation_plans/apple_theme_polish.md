# Implementation Plan: Apple Theme UI Polish & Dashboard Fix

## Phase 1: Functional Verification
- [ ] Restart Backend (Port 4200) using `run_fastapi.py`.
- [ ] Restart Flutter (Port 4242).
- [ ] Confirm Dashboard Stats API returns expected JSON.
- [ ] Confirm Flutter App renders the stats correctly (handling potential UI overflows).

## Phase 2: Design Reference & Theme Update
- [ ] Generate high-fidelity mockup for CultivAR "Apple Theme" Dashboard using `generate_image`.
- [ ] Review `lib/core/theme/app_theme.dart`:
    - Update color palette to use soft grays, deep blacks, and refined greens.
    - Ensure San Francisco or Outfit/Inter fonts are used.
    - Implement consistent border radii (e.g., 20px+).

## Phase 3: UI Polishing
- [ ] **Landing Page**:
    - Enhance glassmorphism effects.
    - Improve hero section spacing and typography weight.
    - Refine "Get Started" button animation.
- [ ] **Dashboard**:
    - Update Stat Cards to look more like iOS Widgets.
    - Add subtle micro-animations to data loading.
    - Refine chart aesthetics (smooth curves, clean axes).

## Phase 4: Validation
- [ ] Run automated screenshots across different screen sizes.
- [ ] Verify accessibility and responsiveness.
