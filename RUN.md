# HYPERSLICE — a true 4D renderer

**Run it:** double-click `PLAY.cmd`. That's all. No server, no install, works offline.

`index_v2.html` is current (12 shapes). `index_v1.html` is the original 5-shape build, kept deliberately.

---

## What you are actually looking at

Not a 3D picture of a 4D object. A **4D object, sliced.**

Each shape is defined by a *4D signed distance function* — a formula that takes any
point `(x, y, z, w)` and returns how far it is from the object's four-dimensional
surface. To draw one frame the renderer:

1. rotates all of 4-space by a 4x4 matrix,
2. takes the 3D cross-section sitting at `w = 0`,
3. sphere-traces that cross-section.

Because the rotation is orthogonal it preserves distance, so the 4D distance is always
a safe lower bound on the distance inside the slice. Sphere tracing therefore never
overshoots, and **the cross-section is exact — not approximated.**

---

## The controls

| Control | What it does |
|---|---|
| **XY / XZ / YZ** | Ordinary rotation. Turns the object the way anything turns in 3D. |
| **XW / YW / ZW** | The impossible ones. These do **not** turn the object — they swing a *different 3D cross-section* into our universe. |
| **W** | Slides our entire 3-space up and down the 4th axis. |
| **Motion** | Still / sweep through W / double rotation / **isoclinic** (see below). |
| **SPD** | Motion speed. |
| **Julia seed c** | Only for the two Julia sets. Changes which fractal exists. |
| **Colour** | W-tilt / depth / 4D normal / plain material. |
| **RES** | Render resolution. Drop it if your GPU struggles. |
| **Save PNG** | Writes the current frame to a file. The panel is not included. |
| **Copy link** | Packs the entire state into the URL. Send it and they see exactly your view. |

Drag to orbit · scroll to zoom · space to play/stop.

---

## Isoclinic rotation — the one with no 3D counterpart

In 3D every rotation leaves an **axis** standing still. You cannot spin a ball without
some line through it staying put. That is a theorem, not a limitation of engineering.

In 4D it is false. Turn the XY plane and the ZW plane **at the same rate at the same
time** and *nothing* stays still except the single centre point. Every other point of
the object moves, continuously, forever. That is an isoclinic rotation, and it has no
analogue below four dimensions.

Choose **Motion → Isoclinic** and watch. Nothing on screen is a fixed axis, because
there isn't one.

---

## What the colours mean

Colour is not decoration. In the default mode it is the **w-component of the 4D
surface normal.**

- **Blue** — this surface lies flat in our 3-space.
- **Orange** — this surface is tilting *out of our universe* along the W axis.
- **Glowing orange** — nearly tangent to our slice. About to vanish.

For a 4-sphere the tilt is uniform over the whole surface and exactly `w / R`, which
is why the glome warms up evenly as you slide W.

---

## The twelve objects

### Regular 4-polytopes

| Object | Why it matters |
|---|---|
| **Tesseract** | The 4-cube. At XW = 45° its cross-section stretches by exactly `sqrt(2)` along x, then snaps back to a cube at 90°. |
| **16-cell** | The 4D cross-polytope, the set where `abs(x)+abs(y)+abs(z)+abs(w) <= 2`. Its slices are octahedra. |
| **24-cell** | **No 3D counterpart whatsoever** — there is nothing like it among the Platonic solids. It is exactly *tesseract ∩ 16-cell*, which is why its formula collapses to `max(Linf, L1/2) - 1`. Its `w = 0` slice is a cuboctahedron. |
| **600-cell** | 120 vertices, 720 edges, 1200 triangles, **600 tetrahedral cells**. The 4D analogue of the icosahedron, built on the golden ratio. It looks nearly spherical because it genuinely is — the roundest regular polytope that exists. |

### Round and product shapes

| Object | Why it matters |
|---|---|
| **Glome** | The 4-sphere. Slice it and you get a 3-ball whose radius is `sqrt(R² − w²)`. Slide W past R and it is simply *gone*. |
| **Duocylinder** | disk × disk. Genuinely impossible below four dimensions. Its `w = 0` slice is a cylinder. |
| **Spherinder** | ball × interval. Its slice is a sphere that **never changes size at all**, and then vanishes with no warning — the exact opposite of the glome. |
| **Cubinder** | disk × square. Sits between the duocylinder and the tesseract. |
| **Tiger** | A torus whose tube is itself swept around a second circle. No 3D analogue, and the prettiest exact SDF in four dimensions. |

### Fractals

| Object | Why it matters |
|---|---|
| **Quaternion Julia z² + c** | `z <- z² + c` over the quaternions. Natively four-dimensional; it cannot be written in fewer dimensions. |
| **Quaternion Julia z³ + c** | Three-fold lobes instead of two. |
| **Foldbox** | The Mandelbox, generalised straight to four dimensions. Infinite structure at every slice. |

---

## What to show people

1. Pick **Glome**. Drag **W** slowly. A solid sphere shrinks to a point and blinks out.
   Explain: the sphere didn't move. *We* did.
2. Pick **Spherinder** and drag **W** again. This time the sphere does not shrink at
   all — and then it is simply not there. Show this immediately after the glome.
3. Pick **Tesseract**. Push **XW** to 45°. The cube stretches. Push to 90°. It is a cube
   again. It never rotated in any direction you can point at.
4. Pick **24-cell**, then **600-cell**, with Motion set to **Sweep through W**. Faces
   appear out of nothing, flare orange as they tilt out of our space, and are gone.
   Nothing is faked or morphed — every frame is an exact cross-section.
5. Set Motion to **Isoclinic** on anything at all, and explain that nothing on screen
   is standing still, because in 4D nothing has to.
6. Pick **Tiger** and **Foldbox** and just let them turn.

If the screen goes empty it will tell you so. That is not a bug: the object has left
our 3-space entirely. Keep turning; it comes back.
