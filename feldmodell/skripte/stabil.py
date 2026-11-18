# Stabiler, erweiterbarer Raum: 7/9 Ordnung (Feld lenkt), 2/9 Chaos, Takt 1234 (runter/Seite/hoch/Seite), Durchlauf nach innen
# Zustand je Zelle: Abweichung e = log2(L*F) als 2D-Vektor (Phase in der Ebene). Ziel L*F = 1 (e = 0).
import numpy as np, json, math
rng=np.random.default_rng(27); out={}
Rot=np.array([[0,-1],[1,0]])          # 90° je Takt um die 1
def lauf(K,T,modus,bias=0.0,chaos=1.0):
    e=np.zeros((K,24,2)); hist=[]
    for t in range(T):
        xi=rng.uniform(-chaos,chaos,(K,24,2))
        src=np.roll(e,1,axis=0); src[0]=0           # Durchlauf: Takt nach innen (Ring k-1 -> k), aussen frischer Eingang
        src=np.roll(src,1,axis=1)                   # ein Feld zur Seite
        moved=src@Rot.T + xi + bias
        if modus=="feld79": e=(2/9)*moved            # Feld lenkt 7/9 zurueck auf Bahn, 2/9 bleibt frei
        elif modus=="ohne":  e=moved                 # kein Feld: Chaos laeuft weiter
        elif modus=="tau5":  e=e+(moved-e)/5         # Vergleich: exponentielle Beruhigung mit tau = 5 Takte (nur Glaettung)
        if t%max(1,T//50)==0 or t==T-1: hist.append(float(np.sqrt((e**2).sum(-1)).mean()))
    rms=np.sqrt((e**2).sum(-1))
    return dict(mittel_ende=round(float(rms.mean()),4), max_ende=round(float(rms.max()),4),
                je_ring_mittel=[round(float(x),4) for x in rms.mean(1)[[0,K//2,K-1]]],
                LF_bereich=[round(float(2**-rms.max()),4),round(float(2**rms.max()),4)],
                verlauf_anfang_ende=[round(hist[1],4),round(hist[-1],4)])
for K in (9,27,81):
    out[f"feld79_K{K}"]=lauf(K,4000,"feld79")
out["ohne_feld_K9"]=lauf(9,4000,"ohne")
out["tau5_K9"]=lauf(9,4000,"tau5")
out["feld79_K9_mit_bias0.5"]=lauf(9,4000,"feld79",bias=0.5)
# Einschwingen: Stoss 1.0, wie viele Takte bis Rest < e^-5 (= '5 tau')
for name,f in (("feld79",lambda x:(2/9)*x),("tau5",lambda x:x-x/5)):
    x=1.0; n=0
    while x>math.exp(-5): x=f(x); n+=1
    out[f"takte_bis_5tau_rest_{name}"]=n
out["(2/9)^4"]=round((2/9)**4,5); out["e^-5"]=round(math.exp(-5),5)
out["stationaer_theorie_bias"]=round(0.5*(2/9)/(1-2/9),4)
print(json.dumps(out,ensure_ascii=False,indent=1)); json.dump(out,open('stabil.json','w'),ensure_ascii=False,indent=1)
