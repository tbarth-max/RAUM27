# Sternfoermig: Nullpunkt (Druck 1) in der Mitte, Weitergabe Ring fuer Ring in alle Richtungen (6+8-Netz),
# Entnahme gesamt Q=1 gleichmaessig auf der aeussersten Schale. Vergleich: 1D-Eimerkette gleicher Laenge.
import numpy as np, itertools as it, json, scipy.sparse as sp, scipy.sparse.linalg as spl
nb=[d for d in it.product((-1,0,1),repeat=3) if sum(map(abs,d))==1]+list(it.product((-1,1),repeat=3))
out={}
for R in (3,6,9,12):
    L=2*R+1; idx=lambda x,y,z:(x*L+y)*L+z; n=L**3
    rows=[];cols=[];vals=[]; deg=np.zeros(n)
    for x,y,z in it.product(range(L),repeat=3):
        i=idx(x,y,z)
        for d in nb:
            a,b,c=x+d[0],y+d[1],z+d[2]
            if 0<=a<L and 0<=b<L and 0<=c<L: rows.append(i);cols.append(idx(a,b,c));vals.append(-1.0);deg[i]+=1
    G=sp.csr_matrix((vals,(rows,cols)),shape=(n,n))+sp.diags(deg)
    shell=[idx(x,y,z) for x,y,z in it.product(range(L),repeat=3) if max(abs(x-R),abs(y-R),abs(z-R))==R]
    I=np.zeros(n); I[shell]=-1.0/len(shell)
    c=idx(R,R,R); free=np.array([i for i in range(n) if i!=c])
    A=G[free][:,free]; b=I[free]-G[free][:,[c]].toarray().ravel()
    V=np.ones(n); V[free]=spl.spsolve(A.tocsc(),b)
    kette=R*1.0   # 1D-Kette: R Glieder, Leitwert 1, Fluss 1 -> Abfall R
    out[R]=dict(knoten=n,aussenschale=len(shell),stern_abfall_max=round(float(1-V.min()),4),kette_abfall=kette)
    print(R,out[R])
json.dump(out,open('stern.json','w'),indent=1)
