# 8 Zweige (Achtel) laufen von der Wand gleichzeitig nach innen. Seriell vs parallel; Treppe (nur Flaechen) vs 6+8.
import itertools as it, json
from collections import deque
F=[d for d in it.product((-1,0,1),repeat=3) if sum(map(abs,d))==1]; E=list(it.product((-1,1),repeat=3))
def lauf(R,links):
    L=2*R+1; S=set(it.product(range(L),repeat=3)); ecken=[tuple(c*(L-1) for c in e) for e in it.product((0,1),repeat=3)]
    D={};q=deque()
    for e in ecken: D[e]=0;q.append(e)
    quelle={e:{e} for e in ecken}
    while q:
        u=q.popleft()
        for d in links:
            w=tuple(u[i]+d[i] for i in range(3))
            if w in S:
                if w not in D: D[w]=D[u]+1;quelle[w]=set(quelle[u]);q.append(w)
                elif D[w]==D[u]+1: quelle[w]|=quelle[u]
    m=(R,R,R)
    return dict(R=R,knoten=L**3,seriell_takte=L**3,parallel_takte_bis_zentrum=D[m],alle_erreicht_nach=max(D.values()),
                zweige_gleichzeitig_im_zentrum=len(quelle[m]))
out={}
for R in (4,13,40):
    out[f"R{R}_treppe_nur_flaechen"]=lauf(R,F)
    out[f"R{R}_6+8"]=lauf(R,F+E)
for k,v in out.items(): print(k,v)
json.dump(out,open('durchlauf.json','w'),ensure_ascii=False,indent=1)
