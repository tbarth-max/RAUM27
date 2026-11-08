# Aufgabe der Komplexitaet C rekrutiert Knoten schalenweise (6+8-Nachbarn), jeder Knoten gibt nur Ueberschuss ueber dem Boden
import numpy as np, itertools as it, json
from collections import deque
N=15; X=1.0; G=0.9; out={}
nb=[d for d in it.product((-1,0,1),repeat=3) if 0<sum(map(abs,d)) and (sum(map(abs,d))==1 or 0 not in d)]
def nachbarn(p): return [tuple((p[i]+d[i])%N for i in range(3)) for d in nb]
def aufgabe(p,start,C):
    # Breitensuche = Schalen um den Startknoten; nimm Ueberschuss bis C gedeckt
    seen={start};q=deque([(start,0)]);got=0;used=0;shell=0
    while q and got<C-1e-12:
        u,s=q.popleft(); take=min(p[u]-G,C-got)
        if take>0: p[u]-=take;got+=take;used+=1;shell=max(shell,s)
        for w in nachbarn(u):
            if w not in seen: seen.add(w);q.append((w,s+1))
    return used,shell,got
rows=[]
for C in (0.1,1,5,20,60,150):
    p={q:X for q in it.product(range(N),repeat=3)}
    used,shell,got=aufgabe(p,(7,7,7),C); rows.append(dict(komplexitaet=C,knoten=used,schalen=shell,gedeckt=round(got,4),boden_min=round(min(p.values()),4)))
out["einzelaufgabe"]=rows
# zwei Aufgaben gleichzeitig, ueberlappend: Knoten gehoeren beiden Clustern an (Zentrum/Peripherie)
p={q:X for q in it.product(range(N),repeat=3)}
a=aufgabe(p,(7,7,7),20); b=aufgabe(p,(9,7,7),20)
out["zwei_ueberlappend"]=dict(A=dict(knoten=a[0],schalen=a[1]),B=dict(knoten=b[0],schalen=b[1]),boden_min=round(min(p.values()),4))
out["schalen_volumen_6+8"]="1,14,62,... (aus netz14)"
print(json.dumps(out,ensure_ascii=False,indent=1)); json.dump(out,open('cluster.json','w'),ensure_ascii=False,indent=1)
