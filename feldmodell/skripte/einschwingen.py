# Auslesen nur, wenn kein Delta-Tensor mehr messbar ist (System eingeschwungen).
# Chaos kommt als Eingangsimpuls (Ausloeser), danach nur Feldschritte (90° + 7/9-Lenkung); Uebertrag nach innen alle 16 Takte.
import numpy as np, json
rng=np.random.default_rng(27); Rot=np.array([[0,-1],[1,0]]); out={}
EPS=1e-12   # Messschwelle: Rest unterhalb = nicht mehr messbar
def tensor(e):
    v=e.reshape(-1,2); T=v.T@v/len(v); w=np.linalg.eigvalsh(T); return float(np.abs(v).max()), [float(x) for x in w]
def lauf(K,impulse=30,dauerchaos=False,maxticks=20000):
    e=np.zeros((K,24,2)); z=0; ablesungen=[]; t_imp=0; n=0
    e[0]=rng.uniform(-1,1,(24,2))                 # erster Ausloeser
    while n<impulse and z<maxticks:
        if (z&15)==1: e=np.roll(e,1,axis=0); e[0]=0          # Uebertrag
        else:
            moved=np.roll(e,1,axis=1)@Rot.T
            if dauerchaos: moved=moved+rng.uniform(-1,1,e.shape)
            e=(2/9)*moved
        z+=1
        m,w=tensor(e)
        if m<EPS:                                           # nichts mehr messbar -> auslesen, naechster Ausloeser
            ablesungen.append(dict(takte=z-t_imp, max_rest=m, tensor_eigen=w)); n+=1; t_imp=z
            e[0]=rng.uniform(-1,1,(24,2))
    if not ablesungen: return dict(ablesungen=0, takte=z, rest_ende=round(tensor(e)[0],4))
    tk=[a["takte"] for a in ablesungen]
    return dict(ablesungen=len(ablesungen), takte_bis_ablesen_min_mittel_max=[min(tk),round(float(np.mean(tk)),2),max(tk)],
                max_rest_bei_ablesen=float('%.1e'%max(a["max_rest"] for a in ablesungen)),
                tensor_eigen_max_bei_ablesen=float('%.1e'%max(max(a["tensor_eigen"]) for a in ablesungen)))
for K in (9,27,81): out[f"impuls_K{K}"]=lauf(K)
out["dauerchaos_K9"]=lauf(9,dauerchaos=True,maxticks=5000)
out["theorie_schritte_1_auf_1e-12"]=round(float(np.log(1e-12)/np.log(2/9)),2)
print(json.dumps(out,ensure_ascii=False,indent=1)); json.dump(out,open('einschwingen.json','w'),ensure_ascii=False,indent=1)
