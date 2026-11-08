# Jeder Knoten Zentrum und Peripherie: Gitter mit 6 (Flaechen) + 8 (Ecken) Verbindungen, periodisch, keine Richtung
import numpy as np, itertools as it, json
from collections import deque
N=6; out={}
F=[d for d in it.product((-1,0,1),repeat=3) if sum(map(abs,d))==1]; E=[d for d in it.product((-1,1),repeat=3)]
nb=F+E; idx=lambda p: (p[0]%N)*N*N+(p[1]%N)*N+(p[2]%N)
nodes=list(it.product(range(N),repeat=3)); A={idx(p):{idx(tuple(p[i]+d[i] for i in range(3))) for d in nb} for p in nodes}
out["nachbarn_je_knoten"]=sorted({len(v) for v in A.values()})
out["verbindung_beidseitig"]=bool(all(a in A[b] for a in A for b in A[a]))
def bfs(s):
    D={s:0};q=deque([s])
    while q:
        u=q.popleft()
        for w in A[u]:
            if w not in D: D[w]=D[u]+1;q.append(w)
    return D
prof={tuple(np.bincount(list(bfs(s).values()))) for s in A}
out["abstandsprofil_je_zentrum_verschieden"]=len(prof); out["abstandsprofil"]=[int(x) for x in list(prof)[0]]
# Gewichte 6+8: Flaechen 1/9, Ecken 1/72, Rest 2/9
w=np.array([2/9]+[1/9]*6+[1/72]*8); out["gewichte_summe"]=float(w.sum()); out["nachbarn_zusammen"]=round(float(w[1:].sum()),6)
c=np.array([[0,0,0]]+F+E); out["impuls_null"]=bool(np.allclose(w@c,0))
out["isotrop_2_ordnung_sum_w_cicj"]=np.round(np.einsum('k,ki,kj->ij',w,c,c),6).tolist()
# Druck/Entnahme ohne festes Zentrum: jeder Knoten haelt X ueber seine 14 Nachbarn (7/9) + eigenen Rest (2/9)
rng=np.random.default_rng(27); p=np.ones(N**3); M=np.zeros((N**3,N**3))
for a in A:
    M[a,a]=2/9
    for d in nb:
        pass
for p_ in nodes:
    a=idx(p_)
    for d,wt in zip(nb,list(w[1:])): M[a,idx(tuple(p_[i]+d[i] for i in range(3)))]+=wt
res=[]
for t in range(3000):
    k=rng.integers(0,N**3); p[k]-=0.05*rng.random()
    p=M@p; p+= (1-p.mean())*0  # kein Zentrum, keine Nachspeisung: reine Umverteilung
    res.append(p.std())
out["ohne_zentrum_nur_umverteilen_streuung_ende"]=float('%.2e'%res[-1]); out["mittel_ende"]=round(float(p.mean()),4)
print(json.dumps(out,ensure_ascii=False,indent=1)); json.dump(out,open('netz14.json','w'),ensure_ascii=False,indent=1)
