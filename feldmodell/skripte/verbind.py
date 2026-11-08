import numpy as np, itertools as it
P=lambda v,a: v-np.outer(v@a,a)  # project onto plane perp to axis a
faces=np.array([s*e for e in np.eye(3) for s in (1,-1)])
corners=np.array(list(it.product((1,-1),repeat=3)),float)
def view(pts,a):
    a=a/np.linalg.norm(a); q=P(pts,a); r=np.round(np.linalg.norm(q,axis=1),6)
    c=(r==0).sum(); ring=np.unique(np.round(q[r>0],6),axis=0)
    return c,len(ring)
for name,a in [("Achse z",np.array([0,0,1.])),("Diagonale",np.array([1,1,1.]))]:
    print(name,"| 6 Flaechen -> (Mitte,Ring):",view(faces,a),"| 8 Ecken -> (Mitte,Ring):",view(corners,a))
# Winkel im Ring bei Diagonalsicht
a=np.array([1,1,1])/3**.5; q=P(corners,a); q=q[np.linalg.norm(q,axis=1)>1e-9]
e1=P(np.array([[1,0,0.]]),a)[0]; e1/=np.linalg.norm(e1); e2=np.cross(a,e1)
print("Ring-Winkel Ecken:",sorted(np.round(np.degrees(np.arctan2(q@e2,q@e1))%360,3)))
qf=P(faces,a); print("Ring-Winkel Flaechen:",sorted(np.round(np.degrees(np.arctan2(qf@e2,qf@e1))%360,3)))
print("Winkel Achse-Diagonale:",np.degrees(np.arccos(1/3**.5)))
# 16/9
pE=4*(8/9)**2; print("Kreis d=9 vs Quadrat 8: pi~",pE,"=256/81, Fehler %",100*(pE-np.pi)/np.pi)
print("256=2^8=4^4, 81=3^4 ; 16/9=2^4/3^2 ; ln:",4*np.log(2)-2*np.log(3),np.log(16/9))
# D2Q9 / D3Q27 Gewichte (Produkt aus 1D 4/6,1/6,1/6)
w1={0:2/3,1:1/6,-1:1/6}
for d in (2,3):
    W={};
    for c in it.product((-1,0,1),repeat=d):
        k=sum(map(abs,c)); W[k]=W.get(k,0)+np.prod([w1[x] for x in c])
    each={k:np.prod([w1[0]]*(d-k)+[w1[1]]*k) for k in W}
    print(f"D{d}Q{3**d}: je Klasse Summe",{k:round(v,5) for k,v in W.items()},"einzeln",{k:round(v,5) for k,v in each.items()})
