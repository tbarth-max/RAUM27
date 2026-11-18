# 8 Eckzweige und 6 Flaechenzweige starten gleichzeitig an der Wand; wo kommen sie im selben Takt an (Resonanz)?
import itertools as it, json
from collections import deque
F=[d for d in it.product((-1,0,1),repeat=3) if sum(map(abs,d))==1]; E=list(it.product((-1,1),repeat=3))
def wellen(R,links,quellen):
    L=2*R+1; S=set(it.product(range(L),repeat=3)); D={};q=deque()
    for s in quellen: D[s]=0;q.append(s)
    while q:
        u=q.popleft()
        for d in links:
            w=tuple(u[i]+d[i] for i in range(3))
            if w in S and w not in D: D[w]=D[u]+1;q.append(w)
    return D,S
def lauf(R,links,name):
    L=2*R+1; ecken=[tuple(c*(L-1) for c in e) for e in it.product((0,1),repeat=3)]
    flaechen=[tuple(R+d[i]*R for i in range(3)) for d in F]
    D8,S=wellen(R,links,ecken); D6,_=wellen(R,links,flaechen); m=(R,R,R)
    gleich=[p for p in S if D8[p]==D6[p]]
    # Resonanzzellen auf den Raumdiagonalen / Achsen
    diag=[p for p in gleich if abs(p[0]-R)==abs(p[1]-R)==abs(p[2]-R)]
    return dict(R=R,links=name,ankunft_zentrum_8=D8[m],ankunft_zentrum_6=D6[m],gleichzeitig_im_zentrum=D8[m]==D6[m],
                resonanzzellen=len(gleich),anteil=round(len(gleich)/len(S),4),davon_auf_raumdiagonalen=len(diag))
out=[]
for R in (4,13):
    out.append(lauf(R,F,"nur Flaechen (Treppe)")); out.append(lauf(R,F+E,"6+8"))
for r in out: print(r)
json.dump(out,open('resonanz68.json','w'),ensure_ascii=False,indent=1)
