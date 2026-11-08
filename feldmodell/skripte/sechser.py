# 9x9x9 Knoten (2 Ebenen 3x3x3), 6+8-Netz, gleicher Leitwert. Zwerge halten Druck 1, jeder Knoten entnimmt gleich viel.
import numpy as np, itertools as it, json
N=9; P=list(it.product(range(N),repeat=3)); ix={p:i for i,p in enumerate(P)}; n=len(P)
nb=[d for d in it.product((-1,0,1),repeat=3) if sum(map(abs,d))==1]+list(it.product((-1,1),repeat=3))
G=np.zeros((n,n))
for p in P:
    for d in nb:
        q=tuple(p[i]+d[i] for i in range(3))
        if q in ix: G[ix[p],ix[q]]-=1; G[ix[p],ix[p]]+=1
def fl(c,s):  # 6 Flaechenmitten eines Wuerfels mit Mitte c, Halbbreite s
    return [tuple(c[i]+s*a[i] for i in range(3)) for a in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]]
blocks=[tuple(3*b[i]+1 for i in range(3)) for b in it.product(range(3),repeat=3)]
varianten={
 "1 Zwerg je 3er-Block (Mitte), 27": blocks,
 "6 Zwerge je 3er-Block (Flaechen), 162": [q for c in blocks for q in fl(c,1)],
 "6 aus 6: nur die 6 Flaechenbloecke des Ganzen, je 6 Zwerge, 36": [q for c in fl((4,4,4),3) for q in fl(c,1)],
 "6 aus 6 + Zentrum-Block 6, 42": [q for c in fl((4,4,4),3)+[(4,4,4)] for q in fl(c,1)],
}
out={}
for name,Z in varianten.items():
    fix=[ix[z] for z in set(Z)]; free=[i for i in range(n) if i not in fix]
    I=np.full(n,-1.0/n)   # gleiche Entnahme je Knoten
    V=np.ones(n); V[free]=np.linalg.solve(G[np.ix_(free,free)], I[free]-G[np.ix_(free,fix)]@np.ones(len(fix)))
    out[name]=dict(zwerge=len(set(Z)),anteil_an_knoten=round(len(set(Z))/n,4),max_abfall=round(float(1-V.min()),5),mittel_abfall=round(float(1-V.mean()),5))
for k,v in out.items(): print(k,v)
print('6/27 =',round(6/27,4),'= 2/9')
json.dump(out,open('sechser.json','w'),indent=1)
