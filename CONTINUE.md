# CONTINUE.md   (last updated: 2026-09-25)

## Done

### v1 — `index_v1.html` (kept, untouched)
- WebGL2 4D raymarcher, 5 shapes, single self-contained file, no deps.
- Verified: tesseract XW=45° 1.4138 vs 1.4142; XW=60° 1.1527 vs csc60 1.1547;
  XW=0° vs 90° 196379 px both; glome +4D rotation 112177 -> 112179 px;
  glome w=1.30 > R=1.25 exactly 0 px; 24-cell 1.5567 vs 1.5573.

### v2 — `index_v2.html` (CURRENT — PLAY.cmd points here)
- **12 shapes.** glome, tesseract, duocylinder, 24-cell, quat Julia z², 16-cell,
  spherinder, cubinder, tiger, quat Julia z³, foldbox (4D Mandelbox), 600-cell.
- **6 tools.** isoclinic + double rotation, empty-slice probe, URL state,
  PNG export, 9 presets, 4 colour modes.
- **600-cell derivation** lives in the session scratchpad as `cell600.py`
  (self-contained Python, no deps; regenerate any time). It was run and verified
  BEFORE the 54 normals were embedded in the shader:
  120 vertices all unit-norm; edge length exactly 1/phi = 0.618033989;
  every vertex degree 12 (icosahedral vertex figure); exactly 600 tetrahedral
  cells from 4-cliques of the edge graph; exactly 600 distinct facet normals,
  every one at distance phi^2/(2*sqrt2) = 0.925614793; invariant under all 16
  coordinate sign flips, so those 600 fold down to the **54** in the shader.

## Verified — v2 (Playwright + canvas pixel measurement vs analytic prediction)
- 16-cell width ratio       1.6098 vs 1.6117   (0.12%)
- duocylinder width ratio   1.0000 vs 1.0000   (exact)
- cubinder width ratio      1.0732 vs 1.0750   (0.17%)
- tiger width ratio         1.3293 vs 1.3222   (0.53%)
- **600-cell width ratio    1.5366 vs 1.5359   (0.047%)** — the prediction was
  computed from the 120 vertices + edge graph (slice vertices at w=0, then the
  max of the linear-fractional objective over them, which for a linear-fractional
  function on a polytope is attained at a vertex). It used NONE of the shader's
  54 normals, so this is an independent cross-check, not a tautology.
- spherinder: w=0 and w=0.9 give byte-identical 69675 px; 0 px at w=1.05
- isoclinic: XY and ZW advance at identical rates (8.000 vs 8.000 deg)
- double rotation ratio 0.6081 vs coded 0.618 (1.6%, purely 0.5° slider quantisation)
- PNG export 859787 bytes, magic bytes 137,80,78,71 = genuine PNG
- URL state round-trips object / 6 angles / W / Julia c / camera / colour mode
- empty-slice banner: shows at w=1.05, hides at w=0
- fps @1024x656: every shape at the 144 Hz vsync cap except foldbox
  (13.5 ms, ~74 fps). 600-cell 7.21 ms — essentially free.

## In Progress / Where I Stopped
- Nothing in progress. v2 complete and verified.

## Next Steps (ideas only — none requested)
1. 120-cell (dual of the 600-cell) — 600 vertices; would need the same sign fold.
2. Stereographic projection mode as an alternative to slicing.
3. Frame-sequence export for a GIF. No ffmpeg on this machine, so it would need a
   JS encoder — that is a new dependency, so ASK FIRST.

## Key Decisions / Caution
- **Slicing, not 4D projection.** Objects are sliced at `w = uW`; that is why
  XW/YW/ZW make things appear, split and vanish. Do not "fix" this — it is the point.
- **`g * uRot` in GLSL means `transpose(uRot) * g`.** Deliberate in `grad4()`.
  Writing `uRot * g` there would silently break the W-colouring.
- **The 600-cell bounding-sphere early-out is load-bearing.**
  `if(bound > 0.2) return bound * s;` keeps the 54-term loop off the hot path.
  Remove it and the frame rate collapses. Returning a smaller-than-true distance
  is always legal for sphere tracing, which is why the shortcut is safe.
- **The shader writes hit/miss into alpha** so the 64x64 offscreen probe can detect
  an empty slice. Do not force alpha to 1.0.
- **24-cell closed form:** `max(Linf(q), L1(q)/2) - 1` = tesseract ∩ 16-cell. Exact.
- **Step factors differ per object** (`stepScale()`): 0.9 for the exact SDFs,
  0.45 for the quaternion Julias, 0.33 for the foldbox. Raising the fractal ones
  brings back surface speckle.
- **Do not raise the Julia iteration counts much** — cost is per-pixel per-step.
- Writing these .md files via a bash heredoc failed on a quoting edge case; use the
  Write tool for them instead.
- Files: `index_v1.html`, `index_v2.html`, `PLAY.cmd`, `RUN.md`, `CONTINUE.md`
  in the repository root.
- Test/run: double-click `PLAY.cmd`. For automated checks:
  `python -m http.server 8010` in this folder, then drive
  `http://localhost:8010/index_v2.html`.
