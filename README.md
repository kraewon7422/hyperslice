# HYPERSLICE

**A true 4D renderer.** Twelve genuinely four-dimensional objects, sliced exactly and
raymarched in real time in the browser. No libraries, no build step, one HTML file.

### ▶ [Live demo — kraewon7422.github.io/hyperslice](https://kraewon7422.github.io/hyperslice/)

---

## What this actually is

Not a wireframe tesseract spinning in 3D. A **4D object, sliced.**

Every shape is defined by a *4D signed distance function* — a formula that takes any
point `(x, y, z, w)` and returns its distance to the object's four-dimensional surface.
To draw one frame the renderer:

1. rotates all of 4-space by a 4×4 matrix,
2. takes the 3D cross-section sitting at `w = 0`,
3. sphere-traces that cross-section.

The rotation matrix is orthogonal, so it preserves distance, so the 4D distance is
always a safe lower bound on the distance *within* the slice. Sphere tracing therefore
never overshoots — which means **the cross-section is exact, not approximated.**

That is why the `XW` / `YW` / `ZW` sliders feel wrong. They do not turn the object.
They swing a **different 3D cross-section** into our universe. Solid things split in
two, turn inside out, and blink out of existence — all of it geometrically correct.

---

## Run it

Open the [live demo](https://kraewon7422.github.io/hyperslice/), or locally:

```bash
git clone https://github.com/kraewon7422/hyperslice.git
cd hyperslice
# then just open index.html in a browser - no server, no install, works offline
```

On Windows you can double-click `PLAY.cmd`.

Requires WebGL2 (any browser since ~2018). Drag to orbit, scroll to zoom, space to play.

---

## The twelve objects

### Regular 4-polytopes
| Object | Notes |
|---|---|
| **Tesseract** | The 4-cube. At `XW = 45°` its cross-section stretches by exactly `√2`, then snaps back to a cube at 90°. |
| **16-cell** | The 4D cross-polytope. Slices are octahedra. |
| **24-cell** | **No 3D counterpart whatsoever.** It is exactly *tesseract ∩ 16-cell*, which collapses its SDF to `max(L∞, L₁/2) − 1`. Its `w = 0` slice is a cuboctahedron. |
| **600-cell** | 120 vertices, 720 edges, 1200 triangles, **600 tetrahedral cells**. The 4D analogue of the icosahedron, built on the golden ratio. |

### Round and product shapes
| Object | Notes |
|---|---|
| **Glome** | The 4-sphere. Slices are 3-balls of radius `√(R² − w²)`. Push `W` past `R` and it is simply gone. |
| **Duocylinder** | disk × disk. Impossible below four dimensions. |
| **Spherinder** | ball × interval. Its slice is a sphere that **never changes size at all**, then vanishes with no warning. |
| **Cubinder** | disk × square. |
| **Tiger** | A torus whose tube is itself swept around a second circle. |

### Fractals
| Object | Notes |
|---|---|
| **Quaternion Julia `z² + c`** | Natively 4D — it cannot be written in fewer dimensions. |
| **Quaternion Julia `z³ + c`** | Three-fold lobes instead of two. |
| **Foldbox** | The Mandelbox, generalised straight to four dimensions. |

---

## Isoclinic rotation

In 3D, every rotation leaves an **axis** standing still. You cannot spin a ball without
some line through it staying put. That is a theorem, not an engineering limitation.

In 4D it is false. Turn the `XY` plane and the `ZW` plane **at the same rate at the same
time** and nothing stays still except the single centre point. Every other point moves,
continuously, forever.

`Motion → Isoclinic`. There is no axis, because in four dimensions there doesn't have
to be one.

---

## Colour is data, not decoration

In the default mode, surface colour is the **w-component of the 4D surface normal**:

- **blue** — this surface lies flat in our 3-space
- **orange** — it is tilting *out of our universe* along W
- **glowing orange** — nearly tangent to our slice; about to vanish

For a 4-sphere this tilt is uniform over the entire surface and equals exactly `w / R`.

---

## How it is verified

Correctness here is not a matter of "it looks right." Every shape's rendered silhouette
was measured in pixels and compared against what the 4D geometry predicts analytically:

| Test | Predicted | Measured | Error |
|---|---|---|---|
| Tesseract `XW=45°` width | `1/cos45° = 1.4142` | 1.4138 | 0.03% |
| Tesseract `XW=60°` width | `1/sin60° = 1.1547` | 1.1527 | 0.17% |
| Tesseract `XW=0°` vs `90°` | identical | 196379 px both | exact |
| 16-cell width | 1.6117 | 1.6098 | 0.12% |
| Cubinder width | 1.0750 | 1.0732 | 0.17% |
| **600-cell width** | **1.5359** | **1.5366** | **0.047%** |
| Glome + 90°/37°/−52° 4D spin | must not change at all | 112177 → 112179 px | 0.002% |
| Glome at `w = 1.30 > R = 1.25` | zero pixels | 0 | exact |
| Spherinder `w=0` vs `w=0.9` | must not change at all | 69675 px both | exact |
| Isoclinic XY vs ZW rate | identical | 8.000° vs 8.000° | exact |

Two of these carry the most weight:

- **The glome test proves the rotation matrix is genuinely orthogonal.** A 4-sphere is
  rotation-invariant, so a violent 4D spin must change *nothing*. It changed 2 pixels
  out of 112,177.
- **The `w = 1.30` test proves the slicing is real.** The object's radius is 1.25; at
  `w = 1.30` our 3-space misses it entirely and the renderer returns an empty universe.

---

## The 600-cell

The hardest object here, and the one worth reading the code for.

An exact SDF for a convex polytope is `max` over its facet half-spaces. The 600-cell has
**600 facets** — far too many to evaluate per pixel, per raymarch step.

But the 600-cell is invariant under all 16 coordinate sign flips. So

```
max over the 600 signed normals of dot(p, n)  ==  max over 54 folded normals of dot(|p|, n)
```

54 is affordable, especially gated behind a bounding-sphere early-out. The result renders
at **7.21 ms/frame against a 6.94 ms vsync cap** — essentially free.

[`cell600.py`](cell600.py) derives and verifies those 54 numbers from scratch. It was run
*before* they were embedded in the shader, and it checks:

```
vertex count          : 120 (expect 120)
edge length           : 0.618033989   1/phi = 0.618033989
vertex degrees        : {12}  (icosahedral vertex figure)
tetrahedral cells     : 600 (expect 600)
distinct facet normals: 600 (expect 600)
inradius/circumradius : 0.925614793   phi^2/(2*sqrt2) = 0.925614793
sign-flip symmetric   : True
normals after |.| fold: 54
```

The rendered silhouette was then checked against a prediction computed independently from
the 120 vertices and their edge graph — using **none** of the 54 normals the shader uses.
They agree to 0.047%.

---

## Why I made it

I wanted to build something where the mathematics is load-bearing — where if the algebra
is wrong, nothing on screen works, and no amount of tweaking colours can hide it. Four
dimensions is a good place for that. You cannot eyeball whether a 4D cross-section is
correct; you have to predict it and measure it.

**Prior art, honestly:** rendering 4D cross-sections is not new — *Miegakure* is a whole
game built on the idea, and quaternion Julia sets go back to the 1980s. What I think is
worth showing here is doing it as an exact distance-field slice with the 4D normal driving
the shading, in one dependency-free file, with every shape's geometry verified numerically
rather than asserted.

---

## Technical notes

- WebGL2 + raw GLSL ES 3.00. No frameworks, no build step, no network requests.
- `index_v1.html` is the original 5-object build, kept deliberately as history.
  `index_v2.html` is current; `index.html` redirects to it, preserving any shared `#state`.
- Shareable links: the entire state — object, six rotation angles, slice position,
  Julia seed, camera, colour mode — is packed into the URL hash.
- The fragment shader writes hit/miss into **alpha**, so a 64×64 offscreen probe can
  detect when the slice is genuinely empty and say so on screen.

---

## Licence

MIT — see [LICENSE](LICENSE).

---
---

# HYPERSLICE (한국어)

**진짜 4차원 렌더러.** 4차원 공간에 존재하는 12개의 도형을 정확하게 잘라내어,
브라우저에서 실시간 레이마칭으로 그립니다. 라이브러리 없음, 빌드 없음, HTML 파일 하나.

### ▶ [라이브 데모](https://kraewon7422.github.io/hyperslice/)

## 이게 뭔가요

3D로 회전하는 테서랙트 와이어프레임이 아닙니다. **4차원 물체를 실제로 자른 단면**입니다.

모든 도형은 *4D 부호 거리 함수(SDF)* 로 정의됩니다. 임의의 점 `(x, y, z, w)` 를 받아
그 물체의 4차원 표면까지의 거리를 돌려주는 함수입니다. 한 프레임을 그릴 때마다:

1. 4차원 공간 전체를 4×4 행렬로 회전시키고,
2. `w = 0` 에 놓인 3차원 단면을 취한 뒤,
3. 그 단면을 스피어 트레이싱 합니다.

회전 행렬이 직교행렬이라 거리를 보존하고, 따라서 4D 거리는 단면 내부 거리의 안전한
하한이 됩니다. 스피어 트레이싱이 절대 건너뛰지 않는다는 뜻이고, 결국
**이 단면은 근사가 아니라 정확합니다.**

`XW` / `YW` / `ZW` 슬라이더가 이상하게 느껴지는 이유가 여기 있습니다. 이 슬라이더들은
물체를 돌리는 게 아니라, **다른 3차원 단면을 우리 우주 안으로 끌어옵니다.** 단단한
물체가 둘로 갈라지고, 뒤집히고, 존재하지 않게 됩니다. 전부 기하학적으로 정확합니다.

## 실행 방법

[라이브 데모](https://kraewon7422.github.io/hyperslice/)를 열거나, 로컬에서는
저장소를 받은 뒤 `index.html` 을 브라우저로 열면 됩니다. 윈도우에서는 `PLAY.cmd`
더블클릭. 서버도 설치도 인터넷도 필요 없습니다. WebGL2만 지원하면 됩니다.

드래그로 시점 회전, 스크롤로 확대, 스페이스바로 재생/정지.

## 등각 회전 (Isoclinic rotation)

3차원에서는 모든 회전이 **축** 하나를 반드시 고정시킵니다. 공을 돌릴 때 어떤 직선
하나는 반드시 제자리에 남습니다. 이건 기술의 한계가 아니라 정리(theorem)입니다.

4차원에서는 거짓입니다. `XY` 평면과 `ZW` 평면을 **같은 속도로 동시에** 돌리면,
중심점 하나를 빼고는 아무것도 멈춰 있지 않습니다. `Motion → Isoclinic` 을 눌러보세요.
고정축이 안 보이는 게 아니라, 애초에 없습니다.

## 색이 곧 데이터입니다

기본 모드에서 표면 색은 **4D 법선 벡터의 w 성분** 입니다.

- **파랑** — 이 면은 우리 3차원 공간에 평평하게 놓여 있음
- **주황** — 이 면은 W 축 방향으로, 우리 우주 바깥으로 기울고 있음
- **빛나는 주황** — 단면에 거의 접함. 곧 사라짐

4-구(glome)의 경우 이 기울기가 표면 전체에서 균일하고 정확히 `w / R` 입니다.

## 어떻게 검증했나

"그럴듯해 보인다"는 검증이 아닙니다. 모든 도형의 실루엣을 픽셀 단위로 측정해서,
4차원 기하학이 해석적으로 예측하는 값과 비교했습니다.

| 항목 | 예측 | 측정 | 오차 |
|---|---|---|---|
| 테서랙트 `XW=45°` 폭 | `1/cos45° = 1.4142` | 1.4138 | 0.03% |
| 16-cell 폭 | 1.6117 | 1.6098 | 0.12% |
| **600-cell 폭** | **1.5359** | **1.5366** | **0.047%** |
| 4-구 + 4D 회전 | 변하면 안 됨 | 112177 → 112179 px | 0.002% |
| 4-구 `w = 1.30 > R = 1.25` | 0 픽셀 | 0 | 정확 |
| 스페린더 `w=0` vs `w=0.9` | 변하면 안 됨 | 둘 다 69675 px | 정확 |

특히 두 가지가 핵심입니다. **4-구 테스트는 회전 행렬이 진짜 직교행렬임을 증명합니다.**
4-구는 회전 불변이라 4차원에서 아무리 돌려도 결과가 바뀌면 안 되는데, 112,177 픽셀 중
2픽셀이 바뀌었습니다. **`w = 1.30` 테스트는 단면이 진짜임을 증명합니다.** 반지름이
1.25인 물체를 `w = 1.30` 에서 자르면 우리 공간은 그 물체를 완전히 빗나가고, 렌더러는
텅 빈 우주를 돌려줍니다.

## 600-cell

여기서 제일 어려운 도형입니다. 볼록 다포체의 정확한 SDF는 각 면의 반공간에 대한
`max` 인데, 600-cell 은 면이 **600개** 라 픽셀마다 레이마칭 스텝마다 계산할 수 없습니다.

그런데 600-cell 은 16가지 좌표 부호 반전 전체에 대해 불변입니다. 따라서

```
600개 부호 있는 법선에 대한 max dot(p, n)  ==  54개로 접은 법선에 대한 max dot(|p|, n)
```

54개면 감당됩니다. 경계구 조기 종료까지 붙이면 프레임당 **7.21 ms** (수직동기 상한
6.94 ms) — 사실상 공짜입니다.

[`cell600.py`](cell600.py) 가 이 54개 숫자를 처음부터 유도하고 검증합니다. 셰이더에
숫자를 넣기 *전에* 먼저 돌려서, 꼭짓점 120개 · 모서리 길이 `1/φ` · 모든 꼭짓점 차수 12 ·
사면체 셀 600개 · 서로 다른 면 법선 600개 · 내접/외접 반지름 비 `φ²/(2√2)` 를 전부
확인했습니다.

## 왜 만들었나

수학이 실제로 무게를 지탱하는 걸 만들고 싶었습니다. 대수가 틀리면 화면에서 아무것도
동작하지 않고, 색을 아무리 만져도 숨길 수 없는 그런 것. 4차원이 그러기에 좋은 무대입니다.
4차원 단면이 맞는지는 눈으로 판단할 수 없고, 예측한 뒤 측정하는 수밖에 없으니까요.

**선행 연구에 대해 솔직히 말하면:** 4차원 단면 렌더링은 새로운 게 아닙니다. *Miegakure*
라는 게임이 통째로 이 아이디어 위에 서 있고, 쿼터니언 줄리아 집합은 1980년대부터
있었습니다. 여기서 보여줄 만하다고 생각하는 부분은, 이걸 정확한 거리장 단면으로 구현하고
4D 법선이 셰이딩을 직접 구동하게 만들었다는 것, 의존성 없는 파일 하나라는 것, 그리고
모든 도형의 기하를 주장이 아니라 수치로 검증했다는 것입니다.

## 라이선스

MIT — [LICENSE](LICENSE) 참고.
