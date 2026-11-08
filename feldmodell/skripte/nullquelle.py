# Alles kommt aus dem Nullpunkt (Mitte = einzige Quelle, Druck 1). 6 Zwerge auf den Flaechen = Speicher (Kapazitaet C), keine Quelle.
import numpy as np, itertools as it, json
axes=[(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]; corn=list(it.product((1,-1),repeat=3))
nodes=[(0,0,0)]+axes+corn; ix={n:i for i,n in enumerate(nodes)}; n=len(nodes)
edges=[((0,0,0),a) for a in axes]+[(a,c) for a in axes for c in corn if np.dot(a,c)==1]+[(c,d) for c,d in it.combinations(corn,2) if sum(x!=y for x,y in zip(c,d))==1]
G=np.zeros((n,n))
for a,b in edges:
    g=1/np.linalg.norm(np.subtract(a,b)); i,j=ix[a],ix[b]; G[i,i]+=g;G[j,j]+=g;G[i,j]-=g;G[j,i]-=g
def lauf(Cz, puls=20, last=0.5, T=400, dt=0.05):
    C=np.ones(n); C[[ix[a] for a in axes]]=Cz
    V=np.ones(n); ecke=ix[(1,1,1)]; quelle=0; verbrauch=0; minV=1
    for s in range(int(T/dt)):
        t=s*dt; I=np.zeros(n)
        if t<puls: I[ecke]=-last; verbrauch+=last*dt
        flow=-G@V            # Zufluss je Knoten
        quelle+=(-flow[0])*dt # was die Mitte abgibt (sie haelt V=1)
        V+= dt*(flow+I)/C; V[0]=1.0
        minV=min(minV,V[ecke])
    speicher=float(((1-V)*C).sum())
    return dict(C_zwerg=Cz,tiefster_druck_ecke=round(float(minV),4),aus_nullpunkt=round(float(quelle),4),verbraucht=round(verbrauch,4),noch_offen=round(speicher,5))
out=[lauf(c) for c in (1,10,100)]
for r in out: print(r)
json.dump(out,open('nullquelle.json','w'),indent=1)
