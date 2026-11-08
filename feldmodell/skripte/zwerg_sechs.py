# Zwerg in der Mitte (1, versorgt 8 Ecken) vs. 6 Zwerge auf den Flaechenmitten bei Radius 1 (je 4 Ecken)
import numpy as np, itertools as it, json
axes=[(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]; corn=list(it.product((1,-1),repeat=3))
nodes=[(0,0,0)]+axes+corn; ix={n:i for i,n in enumerate(nodes)}; n=len(nodes)
L=lambda a,b: float(np.linalg.norm(np.subtract(a,b)))
edges=[((0,0,0),a) for a in axes]+[(a,c) for a in axes for c in corn if np.dot(a,c)==1]+[(c,d) for c,d in it.combinations(corn,2) if sum(x!=y for x,y in zip(c,d))==1]
G=np.zeros((n,n))
for a,b in edges: g=1/L(a,b); i,j=ix[a],ix[b]; G[i,i]+=g;G[j,j]+=g;G[i,j]-=g;G[j,i]-=g
def abfall(quellen,senke,last=1.0):
    # Quellen halten Druck 1 (Zwerge), an der Senke wird 'last' entnommen; Druckabfall an der Senke
    fix=[ix[q] for q in quellen]; free=[i for i in range(n) if i not in fix]
    I=np.zeros(n); I[ix[senke]]=-last
    A=G[np.ix_(free,free)]; b=I[free]-G[np.ix_(free,fix)]@np.ones(len(fix))
    V=np.ones(n); V[free]=np.linalg.solve(A,b)
    strom={q:float(-(G[ix[q]]@V)+0) for q in quellen}
    return round(1-V[ix[senke]],4), {str(k):round(-v,4) for k,v in strom.items()}
out={}
out["Mitte: Abfall an Ecke, Stroeme"]=abfall([(0,0,0)],(1,1,1))
out["6 Flaechen: Abfall an Ecke, Stroeme"]=abfall(axes,(1,1,1))
out["6 Flaechen, einer (+X) ausgefallen"]=abfall([a for a in axes if a!=(1,0,0)],(1,1,1))
out["Mitte + 6 Flaechen"]=abfall([(0,0,0)]+axes,(1,1,1))
out["Abstand Mitte-Ecke / Flaeche-Ecke"]=[round(L((0,0,0),(1,1,1)),4),round(L((1,0,0),(1,1,1)),4)]
out["Versorger je Ecke (6 Flaechen)"]=sorted({sum(1 for a in axes if np.dot(a,c)==1) for c in corn})
print(json.dumps(out,indent=1)); json.dump(out,open('zwerg_sechs.json','w'),indent=1)
