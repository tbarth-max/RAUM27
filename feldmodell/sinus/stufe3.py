# RAUM27 – Gesamtsimulation Stufe 3: Schalen (Radius 1,2,4,8,16), Tropfenfelder (6 Achsen + 8 Diagonalen), Partikel mit Sieb
# Feste Regeln: Feldfrequenz je Schale f_n = b^n; Siebloch je Schale h_n = c^n (Partikel passt in Schale n, wenn Größe <= h_n);
# Partikel-Antwortzeit tau = s * T0 (proportional zur Größe); Phasenverzug phi = atan(2 pi f tau); Verlust je Zyklus ∝ sin(phi) cos(phi)
import numpy as np, json, math
rng=np.random.default_rng(27)
out={}
# A) Tropfengeometrie je Schale: Winkelanteil identisch (per Konstruktion); Mischungsverhältnis Oktopol/Dipol der echten Feldlösung
radien=[1,2,4,8,16]
out["A_innen_oktopol_zu_dipol (r^3/r^1)"]=[r**2 for r in radien]
out["A_aussen_oktopol_zu_dipol (r^-4/r^-2)"]=[round(r**-2,6) for r in radien]
# B) Partikel durch das Sieb
N=200000; s=np.exp(rng.uniform(math.log(2**-6),0,N))      # Größen log-gleichverteilt zwischen 1/64 und 1
T0=0.05
def lauf(b,c,mit_sieb=True):
    res=[]
    if mit_sieb:
        n_of=np.floor(np.log(s)/np.log(c)).astype(int)        # tiefste Schale, in die das Teilchen passt: s <= c^n
        n_of=np.clip(n_of,0,4)
    else:
        n_of=rng.integers(0,5,N)                               # ohne Sieb: zufällige Schale
    for n in range(5):
        m=n_of==n
        if m.sum()==0: res.append(dict(schale=n,anzahl=0)); continue
        w=2*math.pi*b**n; phi=np.arctan(w*s[m]*T0)
        res.append(dict(schale=n, anzahl=int(m.sum()), verzug_mittel_grad=round(float(np.degrees(phi).mean()),2),
                        verlust_mittel=round(float((np.sin(phi)*np.cos(phi)).mean()),4)))
    return res
out["B1_halbierung_passt (f×2, Loch×1/2)"]=lauf(2,0.5)
out["B2_dreier (f×3, Loch×1/3)"]=lauf(3,1/3)
out["B3_falsch_gepaart (f×2, Loch×1/3)"]=lauf(2,1/3)
out["B4_ohne_sieb (f×2)"]=lauf(2,0.5,mit_sieb=False)
# C) Kennzahl: Streuung des mittleren Verzugs über die Schalen 1–4 (Schale 0 ist Sammelbecken der großen Teilchen)
def spread(r): v=[x["verzug_mittel_grad"] for x in r[1:] if x["anzahl"]>0]; return round(max(v)-min(v),2)
out["C_spreizung_verzug_grad"]={k:spread(out[k]) for k in ("B1_halbierung_passt (f×2, Loch×1/2)","B2_dreier (f×3, Loch×1/3)","B3_falsch_gepaart (f×2, Loch×1/3)","B4_ohne_sieb (f×2)")}
print(json.dumps(out,ensure_ascii=False,indent=1))
