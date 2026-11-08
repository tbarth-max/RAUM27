# Freies Potenzial mit Vordruck X: Entnahme wird automatisch ausgeglichen, nur lokale Regel, keine Ueberwachung
import numpy as np, json
rng=np.random.default_rng(27); out={}; X=1.0
def lauf(N=9,ticks=20000,rate=0.002,offen=True,kappa=1/9):
    p=np.full((N+2,N+2),X)                      # Rand = Reservoir mit Vordruck X
    entnommen=0.0; zufluss=0.0; tief=[]
    for t in range(ticks):
        i,j=rng.integers(1,N+1,2); a=rate*rng.random()*2; a=min(a,p[i,j]); p[i,j]-=a; entnommen+=a   # irgendwer entnimmt
        # lokale Regel: jede Zelle tauscht mit 4 Nachbarn (Fluss ~ Druckunterschied), nichts wird gezaehlt oder gesteuert
        lap=np.zeros_like(p); lap[1:-1,1:-1]=p[:-2,1:-1]+p[2:,1:-1]+p[1:-1,:-2]+p[1:-1,2:]-4*p[1:-1,1:-1]
        fluss_rand=kappa*(lap[1,1:-1].sum()*0)  # (nur Buchhaltung unten)
        alt=p[1:-1,1:-1].sum()
        p[1:-1,1:-1]+=kappa*lap[1:-1,1:-1]
        if offen: p[0,:]=p[-1,:]=p[:,0]=p[:,-1]=X     # Reservoir haelt Vordruck
        else:     p[0,:]=p[1,:];p[-1,:]=p[-2,:];p[:,0]=p[:,1];p[:,-1]=p[:,-2]   # geschlossen, kein Nachschub
        zufluss+=p[1:-1,1:-1].sum()-alt
        if t>ticks//2: tief.append(p[1:-1,1:-1].min())
    inn=p[1:-1,1:-1]
    return dict(entnommen=round(entnommen,4), zufluss_aus_reservoir=round(zufluss,4),
                bilanz_rest=round(entnommen-zufluss-(N*N*X-inn.sum()),6),
                druck_mittel=round(float(inn.mean()),4), druck_min_spaete_haelfte=round(float(min(tief)),4),
                druck_mitte=round(float(inn[N//2,N//2]),4), druck_rand=round(float(inn[0,N//2]),4))
out["offen_9x9"]=lauf()
out["offen_27x27"]=lauf(N=27,ticks=20000,rate=0.002*9)
out["geschlossen_9x9"]=lauf(offen=False)
out["offen_9x9_ueberlast_x20"]=lauf(rate=0.04)
print(json.dumps(out,ensure_ascii=False,indent=1)); json.dump(out,open('vordruck.json','w'),ensure_ascii=False,indent=1)
