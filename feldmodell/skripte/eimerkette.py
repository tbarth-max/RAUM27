# Eimerkette von 1/9 bis 9 (Log-Stufen Faktor 3: 1/9,1/3,1,3,9 bzw. feiner 9 Stufen). Jeder reicht nur an den Nachbarn weiter.
# Innen (1/9) Quelle mit Vordruck, aussen (9) schwankende Entnahme. Gemessen: Schwankung je Stelle, Fluss je Glied.
import numpy as np, json
rng=np.random.default_rng(27); out={}
for K in (5,9):
    pos=np.logspace(np.log10(1/9),np.log10(9),K)
    p=np.ones(K); g=0.25; T=40000; hist=[]; fl=[]
    for t in range(T):
        f=g*(p[:-1]-p[1:])                    # Weitergabe an den Nachbarn (Hand zu Hand)
        p[:-1]-=f; p[1:]+=f
        p[0]=1.0                              # innen: Nullpunkt-Vordruck
        p[-1]-=0.02*rng.random()*2*(rng.random()<0.5)   # aussen: schwankende Entnahme
        if t>T//2: hist.append(p.copy()); fl.append(f.copy())
    H=np.array(hist); Fm=np.array(fl).mean(0)
    out[f"K{K}"]=dict(stellen=[round(x,3) for x in pos], schwankung_je_stelle=[float('%.2e'%x) for x in H.std(0)],
                      mittlerer_fluss_je_glied=[round(float(x),5) for x in Fm], druck_mittel=[round(float(x),4) for x in H.mean(0)])
for k,v in out.items():
    print(k); [print('  ',a,b) for a,b in v.items()]
print('Spiegel: 1/9 * 9 =',1/9*9,'; Spanne 9/(1/9) = 81 = 9^2; Mitte (geom.) =',round(float(np.sqrt(1/9*9)),3))
json.dump(out,open('eimerkette.json','w'),indent=1)
