# Gleicher Widerstand an jedem Knoten (Leitwert k je Verbindung). Drei Nachschubwege, Druck als Messung fuers ganze System.
import numpy as np, json
rng=np.random.default_rng(27); K=9; X=1.0; k=1/4; out={}
def lauf(weg, d, ticks=4000):
    a=np.full(K,X); v=np.zeros(K); H=50.0; Hl=np.full(K,5.0); tot0=a.sum()+v.sum()+H+Hl.sum(); mins=[]; defi=[]; flow=[]
    for t in range(ticks):
        need=np.minimum(np.where(rng.random(K)<0.5,2*d*rng.random(K),0.0),a); a-=need; v+=need
        up=np.concatenate(([X],a[:-1])); f=k*(up-a); f[0]=min(f[0],H); H-=f[0]; a+=f; a[:-1]-=f[1:]   # Radien
        if weg=="linear":                                          # Linearvektor: jede Ebene ein Knoten direkt am Herzen
            fl=np.minimum(k*(X-a),H/K); fl=np.maximum(fl,0); a+=fl; H-=fl.sum()
        if weg=="ebene":                                           # Vordruck-Punkt je Ebene (kleines Herz an der lokalen Eins)
            fl=np.minimum(np.maximum(k*(X-a),0),Hl); a+=fl; Hl-=fl
        g=k*v; v-=g
        if weg=="ebene": Hl+=g                                     # lokale Vene speist lokales Herz
        else: v[:-1]+=g[1:]; H+=g[0]
        if t>ticks//2: mins.append(a.min()); defi.append(X-a.mean()); flow.append(need.sum())
    return dict(aussen_min=round(float(min(mins)),4), mittel_defizit=float(np.mean(defi)), bedarf=float(np.mean(flow)),
                volumen_ok=bool(abs(a.sum()+v.sum()+H+Hl.sum()-tot0)<1e-6))
for weg in ("radien","linear","ebene"):
    rows=[lauf(weg,d) for d in (0.0,0.002,0.004,0.008,0.016)]
    x=np.array([r["bedarf"] for r in rows]); y=np.array([r["mittel_defizit"] for r in rows])
    slope=float(np.polyfit(x,y,1)[0]); r2=float(np.corrcoef(x,y)[0,1]**2) if x.std()>0 else 0
    out[weg]=dict(aussen_min_je_last=[r["aussen_min"] for r in rows], defizit_je_last=[round(r["mittel_defizit"],5) for r in rows],
                  ruhe_defizit=rows[0]["mittel_defizit"], druck_misst_gesamtbedarf_R2=round(r2,4), steigung=round(slope,3),
                  volumen_ok=all(r["volumen_ok"] for r in rows))
print(json.dumps(out,ensure_ascii=False,indent=1)); json.dump(out,open('wege.json','w'),ensure_ascii=False,indent=1)
