# Verarbeitungsraster im positiven Raum, Zentrum (1,1,1), b = Schrittfaktor
import numpy as np, itertools as it
b=2.0
# 6 Schnitte = 3 Ebenen (x=1,y=1,z=1) x 2 Seiten (innen/aussen der Normalachse)
planes=[(ax,side) for ax in range(3) for side in (1/b,b)]
ring=[(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0)]   # 8 Felder um das Original (Log-Exponenten)
corners=[(-1,1),(-1,-1),(1,-1),(1,1)]   # 1 runter, 2 rechts, 3 hoch, 4 links  (Start oben links)
def cell(ax,side,e,lev):  # Log-Exponent e auf Ebene, Ring-Ebene lev (Skalierung 1/3^lev im Log)
    p=np.ones(3); others=[i for i in range(3) if i!=ax]
    p[ax]=side
    for i,k in zip(others,e): p[i]=b**(k/3**lev)
    return p
pts=[cell(ax,s,e,0) for ax,s in planes for e in ring]
print("T1 Felder: 6 Schnitte x 8 um das Original =",len(pts),"| alle positiv:",np.all(np.array(pts)>0))
# T2 Zyklus 1234: Schrittrichtungen und Drehwinkel
L=np.array(corners,float); steps=np.diff(np.vstack([L,L[:1]]),axis=0)
print("T2 Schritte (Log):",steps.tolist(),"| Drehung je Schritt:",[round(np.degrees(np.arctan2(np.cross(L[i],L[(i+1)%4]),L[i]@L[(i+1)%4])),1) for i in range(4)])
# T3 Rueckweg 4321 hebt exakt auf
x=np.array([1.,1.]); path=[x.copy()]
for s in steps: x=x*b**s; path.append(x.copy())
for s in steps[::-1]: x=x/b**s
print("T3 Rueckweg Fehler:",abs(x-1).max(), "| Zyklus schliesst:",np.allclose(path[0],path[-1]))
# T4 Ecken von aussen nach innen: Ring-Ebene k, Log-Abstand 1/3^k
for lev in range(5):
    c=cell(2,b,(1,1),lev); print(f"T4 Ring {lev}: Ecke =",np.round(c[:2],6),"Abstand zur 1 im Log:",round(np.log(c[0])/np.log(b),6))
# T5 jedes Achtel (innen/aussen je Achse) wird von genau 3 Schnitten an einer Ecke beruehrt
cnt={}
for ax,s in planes:
    for e in corners:
        p=cell(ax,s,e,0); o=tuple((p>1).astype(int)); cnt[o]=cnt.get(o,0)+1
print("T5 Ecken je Achtel:",sorted(cnt.values()),"| Achtel:",len(cnt))
# T6 Zellen je Ring-Ebene in Flaeche/Raum: 9^k bzw 27^k
print("T6 Flaeche 9^k:",[9**k for k in range(4)],"Raum 27^k:",[27**k for k in range(4)])
