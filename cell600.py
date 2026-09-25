import itertools, math, json
PHI = (1 + math.sqrt(5)) / 2

# ---- 120 vertices of the 600-cell (unit quaternions = binary icosahedral group 2I)
V = set()
def add(v):
    V.add(tuple(round(c, 12) + 0.0 for c in v))

for i in range(4):                                   # 8: perms of (+-1,0,0,0)
    for s in (1, -1):
        v = [0.0]*4; v[i] = float(s); add(v)

for signs in itertools.product((1, -1), repeat=4):   # 16: (+-1/2)^4
    add([s * 0.5 for s in signs])

base = [PHI/2, 0.5, 1/(2*PHI), 0.0]                  # 96: EVEN perms, all signs
def parity(p):
    n = 0
    for i in range(len(p)):
        for j in range(i+1, len(p)):
            if p[i] > p[j]: n += 1
    return n % 2
for perm in itertools.permutations(range(4)):
    if parity(perm) != 0: continue
    vals = [base[perm.index(k)] for k in range(4)]
    nz = [i for i, x in enumerate(vals) if abs(x) > 1e-12]
    for signs in itertools.product((1, -1), repeat=len(nz)):
        v = list(vals)
        for idx, s in zip(nz, signs): v[idx] = v[idx] * s
        add(v)

V = sorted(V)
print("vertex count          :", len(V), "(expect 120)")
print("all unit norm         :", all(abs(math.sqrt(sum(c*c for c in v))-1) < 1e-9 for v in V))

def d2(a, b): return sum((x-y)**2 for x, y in zip(a, b))
edge2 = sorted({round(d2(V[0], v), 9) for v in V if v != V[0]})[0]
print("edge length           :", round(math.sqrt(edge2), 9), " 1/phi =", round(1/PHI, 9))

adj = [[j for j in range(120) if j != i and abs(d2(V[i], V[j]) - edge2) < 1e-9] for i in range(120)]
print("vertex degrees        :", {len(a) for a in adj}, "(expect {12}: vertex figure is an icosahedron)")

adjset = [set(a) for a in adj]
cells = []
for i in range(120):
    for j in adj[i]:
        if j <= i: continue
        for k in adjset[i] & adjset[j]:
            if k <= j: continue
            for l in adjset[i] & adjset[j] & adjset[k]:
                if l <= k: continue
                cells.append((i, j, k, l))
print("tetrahedral cells     :", len(cells), "(expect 600)")

facets = {}
for c in cells:
    cen = [sum(V[t][a] for t in c)/4 for a in range(4)]
    L = math.sqrt(sum(x*x for x in cen))
    n = tuple(round(x/L, 9) + 0.0 for x in cen)
    facets[n] = max(sum(n[a]*V[t][a] for a in range(4)) for t in c)
print("distinct facet normals:", len(facets), "(expect 600)")

ds = list(facets.values())
print("facet distance d      : min %.12f  max %.12f" % (min(ds), max(ds)))
inr = sum(ds)/len(ds)
print("inradius/circumradius :", round(inr, 9), " phi^2/(2*sqrt2) =", round(PHI**2/(2*math.sqrt(2)), 9))

worst = max(max(sum(n[a]*v[a] for a in range(4)) for n in facets) - inr for v in V)
print("max vertex violation  : %.3e (must be ~0)" % worst)

red = sorted({tuple(round(abs(x), 9) + 0.0 for x in n) for n in facets})
print("normals after |.| fold:", len(red))

sign_ok = all(tuple(round(s*c, 12) + 0.0 for s, c in zip(sg, v)) in set(V)
              for v in V for sg in itertools.product((1,-1), repeat=4))
print("sign-flip symmetric   :", sign_ok, "(required for the fold to be valid)")

json.dump({"d": inr, "n": red}, open("cell600.json", "w"))
print("wrote cell600.json with", len(red), "normals")
