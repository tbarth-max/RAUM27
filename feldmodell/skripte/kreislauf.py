# Bild Thomas: Herz haelt Vordruck X konstant (kein Schlag). Zellen nehmen bei Bedarf aus der Arterie und geben an die Vene.
# Das Herz schiebt genau so viel nach, wie am Eingang fehlt. Geschlossener Kreis, kein Reservoir ausserhalb.
import numpy as np, json
rng=np.random.default_rng(27); K=9; X=1.0; k=1/4; out={}
def lauf(bedarf_an, ticks=6000):
    a=np.full(K,X); v=np.zeros(K); H=5.0; tot0=a.sum()+v.sum()+H; push=[]; flow=[]; dem=[]
    for t in range(ticks):
        need=np.where(rng.random(K)<0.2,0.01*rng.random(K),0.0) if bedarf_an(t) else np.zeros(K)
        need=np.minimum(need,a); a-=need; v+=need; dem.append(need.sum())
        up=np.concatenate(([X],a[:-1])); f=k*(up-a)            # Arterie: Druckunterschied zum inneren Nachbarn (Ring 0 haengt am Herzen)
        f[0]=min(f[0],H); H-=f[0]
        a+=f; a[:-1]-=f[1:]
        g=k*v; v-=g; v[:-1]+=g[1:]; H+=g[0]                      # Vene: fliesst Ring fuer Ring zum Herzen zurueck
        push.append(f[0]); flow.append(float(np.abs(f).sum()))
    return dict(arterie_min=round(float(a.min()),4), herz_schiebt_mittel=float('%.3e'%np.mean(push[-2000:])),
                bedarf_mittel=float('%.3e'%np.mean(dem[-2000:])), fluss_mittel=float('%.3e'%np.mean(flow[-2000:])),
                volumen_erhalten=bool(abs(a.sum()+v.sum()+H-tot0)<1e-9))
out["ruhe"]=lauf(lambda t: False)
out["bedarf"]=lauf(lambda t: True)
out["bedarf_dann_ruhe"]=lauf(lambda t: t<3000)
print(json.dumps(out,ensure_ascii=False,indent=1)); json.dump(out,open('kreislauf.json','w'),ensure_ascii=False,indent=1)
