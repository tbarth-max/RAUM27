# RAUM27 Dauerlauf: 6+8-Netz, 8+1 (ein Zwerg je 2x2x2-Block), Vordruck X, Boden G, 3 Ressourcen, Verbrauch + Stabilitaet
import numpy as np, itertools as it, json, sys, time
rng=np.random.default_rng(27)
N=12; R=3; X=1.0; G=0.9; kap=0.2; kz=0.25; TICKS=int(sys.argv[1]) if len(sys.argv)>1 else 100000; LOG=1000
nb=[d for d in it.product((-1,0,1),repeat=3) if sum(map(abs,d))==1]+list(it.product((-1,1),repeat=3)); w=np.array([1/9]*6+[1/72]*8)
p=np.full((R,N,N,N),X)                     # Knotendruck je Ressource
B=N//2; zwerg=np.full((R,B,B,B),1.0)       # Zwerg-Vorrat je Block (8+1)
def blocksum(a): return a.reshape(R,B,2,B,2,B,2).sum(axis=(2,4,6))
def up(a): return np.repeat(np.repeat(np.repeat(a,2,1),2,2),2,3)
tot_verbrauch=0; tot_quelle=0; log=[]; viel=(slice(None),slice(2,4),slice(2,4),slice(2,4))
gesamt0=p.sum()+zwerg.sum(); t0=time.time()
win=dict(bedarf=0,verbrauch=0,quelle=0,boden_verletzt=0,minp=9,defizit=0)
for t in range(1,TICKS+1):
    # Bedarf: zufaellig je Knoten/Ressource; Phase mit Vielentnehmer (jeden 3. Abschnitt von 20000 Takten)
    want=np.where(rng.random(p.shape)<0.05,0.02*rng.random(p.shape),0.0)
    if (t//20000)%3==1: want[viel]+=0.05
    take=np.minimum(want,np.maximum(p-G,0)); p-=take
    win["bedarf"]+=want.sum(); win["verbrauch"]+=take.sum(); tot_verbrauch+=take.sum()
    # Normierung im Netz (6+8, Rest 2/9)
    p=2/9*p+sum(wi*np.roll(p,d,axis=(1,2,3)) for d,wi in zip(nb,w))
    # Zwerg je Block schiebt genau nach, was zum Vordruck fehlt (aus seinem Vorrat)
    fehl=np.maximum(X-p,0)*kz; bedarfblock=blocksum(fehl); gib=np.minimum(bedarfblock,zwerg); anteil=np.where(bedarfblock>0,gib/np.maximum(bedarfblock,1e-300),0)
    p+=fehl*up(anteil); zwerg-=gib
    # Herz (Linearvektor, gleicher Widerstand): fuellt jeden Zwerg auf 1 auf -> Quelle von aussen
    q=np.maximum(1.0-zwerg,0)*kap; zwerg+=q; win["quelle"]+=q.sum(); tot_quelle+=q.sum()
    m=p.min(); win["minp"]=min(win["minp"],m); win["boden_verletzt"]+=int((p<G-1e-12).sum()); win["defizit"]+=float(X-p.mean())
    if t%LOG==0:
        bil=(p.sum()+zwerg.sum())-(gesamt0+tot_quelle-tot_verbrauch)
        rec=dict(takt=t,bedarf=round(win["bedarf"],3),verbrauch=round(win["verbrauch"],3),quelle=round(win["quelle"],3),
                 bilanzfehler=float('%.1e'%bil),min_druck=round(float(win["minp"]),4),boden_verletzt=win["boden_verletzt"],
                 mittl_defizit=round(win["defizit"]/LOG,5),streuung=float('%.2e'%p.std()),zwerg_min=round(float(zwerg.min()),4),
                 vielentnehmer=bool((t//20000)%3==1))
        log.append(rec); win=dict(bedarf=0,verbrauch=0,quelle=0,boden_verletzt=0,minp=9,defizit=0)
        if t%(LOG*10)==0:
            json.dump(log,open('dauerlauf_log.json','w'),indent=0); print(rec,round(time.time()-t0,1),'s',flush=True)
json.dump(log,open('dauerlauf_log.json','w'),indent=0)
