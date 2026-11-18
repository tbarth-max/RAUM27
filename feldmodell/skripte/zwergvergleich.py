# Variante A: ein Zwerg je Block fuer alle 3 Ressourcen (Herz 0.2 bzw. 0.6) / B: ein Zwerg je Block und Ressource (Herz 0.2)
import numpy as np, itertools as it, json
nb=[d for d in it.product((-1,0,1),repeat=3) if sum(map(abs,d))==1]+list(it.product((-1,1),repeat=3)); wts=[1/9]*6+[1/72]*8
N=12;R=3;B=6;G=0.9
def blk(a): return a.reshape(R,B,2,B,2,B,2).sum(axis=(2,4,6))
def up(a): return np.repeat(np.repeat(np.repeat(a,2,1),2,2),2,3)
def lauf(variante,herz,T=30000,ALLE=1):
    rng=np.random.default_rng(27); p=np.ones((R,N,N,N)); z=np.ones((R,B,B,B)) if variante=="B" else np.ones((B,B,B))
    stat={r:[0,0] for r in range(R)}; zmin=9; pmin=9; quelle=0
    for t in range(T):
        want=np.where(rng.random(p.shape)<0.05,0.02*rng.random(p.shape),0.0)
        viel=10000<=t<20000
        if viel: want[:ALLE,2:4,2:4,2:4]+=0.05
        take=np.minimum(want,np.maximum(p-G,0)); p-=take
        if viel:
            for r in range(R): stat[r][0]+=want[r].sum(); stat[r][1]+=take[r].sum()
        p=2/9*p+sum(w*np.roll(p,d,axis=(1,2,3)) for d,w in zip(nb,wts))
        fehl=0.25*np.maximum(1-p,0); fb=blk(fehl)
        if variante=="B":
            gib=np.minimum(fb,z); ant=np.where(fb>0,gib/np.maximum(fb,1e-300),0); p+=fehl*up(ant); z-=gib
        else:
            tot=fb.sum(0); gib=np.minimum(tot,z); ant=np.where(tot>0,gib/np.maximum(tot,1e-300),0); p+=fehl*up(np.broadcast_to(ant,(R,B,B,B))); z-=gib
        q=herz*np.maximum(1-z,0); z+=q; quelle+=q.sum()
        if viel: zmin=min(zmin,z.min()); pmin=min(pmin,p.min())
    return dict(deckung_je_ressource=[round(stat[r][1]/stat[r][0],4) for r in range(R)],zwerg_min=round(float(zmin),3),druck_min=round(float(pmin),4),quelle=round(float(quelle),1))
out={f"{v}_herz{h}_stress{a}":lauf(v,h,ALLE=a) for a in (1,3) for v,h in (("A",0.2),("A",0.6),("B",0.2))}
print(json.dumps(out,indent=1)); json.dump(out,open('zwergvergleich.json','w'),indent=1)
