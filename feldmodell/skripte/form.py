# 216 Knoten als ein Strukturblock: dicht (Wuerfel) vs breit (flach) - Aussenverbindungen und innere Wege (6+8-Netz)
import itertools as it, json
from collections import deque
nb=[d for d in it.product((-1,0,1),repeat=3) if (sum(map(abs,d))==1) or (0 not in d)]
def mass(a,b,c):
    S=set(it.product(range(a),range(b),range(c)))
    aussen=sum(1 for p in S for d in nb if tuple(p[i]+d[i] for i in range(3)) not in S)
    innen=sum(1 for p in S for d in nb if tuple(p[i]+d[i] for i in range(3)) in S)//2
    def ecc(s):
        D={s:0};q=deque([s])
        while q:
            u=q.popleft()
            for d in nb:
                w=tuple(u[i]+d[i] for i in range(3))
                if w in S and w not in D: D[w]=D[u]+1;q.append(w)
        return max(D.values())
    durchm=max(ecc(s) for s in [(0,0,0),(a-1,b-1,c-1),(a-1,0,0),(0,b-1,0)])
    return dict(form=f"{a}x{b}x{c}",knoten=len(S),aussenverbindungen=aussen,innenverbindungen=innen,durchmesser=durchm,
                aussen_je_knoten=round(aussen/len(S),2))
rows=[mass(*f) for f in ((6,6,6),(12,6,3),(9,8,3),(12,9,2),(18,12,1),(24,9,1),(36,6,1),(216,1,1))]
for r in rows: print(r)
json.dump(rows,open('form.json','w'),ensure_ascii=False,indent=1)
