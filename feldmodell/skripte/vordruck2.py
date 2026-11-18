# Mehrere Ressourcen, jede mit Vordruck X; Ausgleich nur ueber Delta-Druck; ein Vielentnehmer
import numpy as np, json
rng=np.random.default_rng(27); N=9; X=np.array([1.0,1.0,1.0]); kappa=1/9; out={}
def lauf(viel=0.0, lokal_reservoir=False, ticks=20000):
    p=np.ones((3,N+2,N+2))*X[:,None,None]; c=N//2+1
    for t in range(ticks):
        r=rng.integers(0,3); i,j=rng.integers(1,N+1,2); a=min(0.004*rng.random(),p[r,i,j]); p[r,i,j]-=a   # alle entnehmen zufaellig
        if viel: a=min(viel,p[0,c,c]); p[0,c,c]-=a                                                      # einer nimmt viel von Ressource 0
        lap=np.zeros_like(p); lap[:,1:-1,1:-1]=p[:,:-2,1:-1]+p[:,2:,1:-1]+p[:,1:-1,:-2]+p[:,1:-1,2:]-4*p[:,1:-1,1:-1]
        p[:,1:-1,1:-1]+=kappa*lap[:,1:-1,1:-1]
        p[:,0,:]=X[:,None]; p[:,-1,:]=X[:,None]; p[:,:,0]=X[:,None]; p[:,:,-1]=X[:,None]
        if lokal_reservoir: p[:,1:-1:2,1:-1:2]+= (X[:,None,None]-p[:,1:-1:2,1:-1:2])*(7/9)   # Reservoir an jedem 2. Punkt (lokale Einsen)
    q=p[:,1:-1,1:-1]
    return {f"Ressource{r}":dict(mittel=round(float(q[r].mean()),4),spanne_alle=round(float(q[r].max()-q[r].min()),4),
            vielentnehmer=round(float(q[r][N//2,N//2]),4),nachbar=round(float(q[r][N//2,N//2+1]),4),weit_weg=round(float(q[r][0,0]),4)) for r in range(3)}
out["alle_gleich"]=lauf()
out["ein_vielentnehmer_0.05"]=lauf(viel=0.05)
out["ein_vielentnehmer_0.05_lokale_reservoirs"]=lauf(viel=0.05,lokal_reservoir=True)
print(json.dumps(out,ensure_ascii=False,indent=1)); json.dump(out,open('vordruck2.json','w'),ensure_ascii=False,indent=1)
