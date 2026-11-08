# Leitungsnetz ohne Flaechen: Zentrum + 6 Achsenpole + 8 Wuerfelecken, gleiche Widerstaende/Laengen
import numpy as np, itertools as it, json
out={}
P=[tuple(s*e for e in [1]) for s in (1,)]  # Platzhalter
axes=[(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]
corn=list(it.product((1,-1),repeat=3))
nodes=[(0,0,0)]+axes+corn; ix={n:i for i,n in enumerate(nodes)}
edges=[((0,0,0),a) for a in axes]
edges+=[(a,c) for a in axes for c in corn if sum(x*y for x,y in zip(a,c))==1]        # Pol -> 4 angrenzende Ecken
edges+=[(c,d) for c,d in it.combinations(corn,2) if sum(x!=y for x,y in zip(c,d))==1] # 12 Wuerfelkanten
out["kanten"]=len(edges)
n=len(nodes); Lap=np.zeros((n,n))
for a,b in edges: i,j=ix[a],ix[b]; Lap[i,i]+=1;Lap[j,j]+=1;Lap[i,j]-=1;Lap[j,i]-=1
# Gleichstrom: 1 rein bei +X, raus im Zentrum
I=np.zeros(n); I[ix[(1,0,0)]]=1; I[0]=-1
A=Lap.copy(); A[0,:]=0; A[0,0]=1; b=I.copy(); b[0]=0; V=np.linalg.solve(A,b)
cur={(a,b):V[ix[a]]-V[ix[b]] for a,b in edges}
knoten_ok=max(abs(sum(cur[e] if e[0]==nd else -cur[e] for e in edges if nd in e)-I[ix[nd]]) for nd in nodes)
out["knotenregel_max_abw"]=float('%.1e'%knoten_ok)
nah=[c for c in corn if c[0]==1]; fern=[c for c in corn if c[0]==-1]
out["potential_ecken_nah_(+x)"]=sorted({round(V[ix[c]],4) for c in nah}); out["potential_ecken_fern_(-x)"]=sorted({round(V[ix[c]],4) for c in fern})
out["strom_direkt_ins_zentrum"]=round(cur[((0,0,0),(1,0,0))]*-1,4)
out["leistung_I2R (Verlust)"]=round(sum(v*v for v in cur.values()),4)
# Wellen-Variante (L-C, verlustfrei): Leapfrog auf demselben Netz
u=np.zeros(n); u[ix[(1,0,0)]]=1.0; v=np.zeros(n); dt=0.005; E0=None; Es=[]
for t in range(200000):
    v-=dt*(Lap@u); u+=dt*v
    E=0.5*v@v+0.5*u@(Lap@u)
    if E0 is None: E0=E
    Es.append(E)
out["LC_energie_drift_rel"]=float('%.1e'%((max(Es)-min(Es))/E0))
out["v_normiert = (lambda/2pi)*(2pi*nu)/c"]=1.0
print(json.dumps(out,ensure_ascii=False,indent=1)); json.dump(out,open('leitungsnetz.json','w'),ensure_ascii=False,indent=1)
