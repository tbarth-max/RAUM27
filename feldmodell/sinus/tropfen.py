# 6 Tropfen (Achsen, ±) und 8 Tropfen (Diagonalen) als Winkelanteile auf der Einheitskugel; zwei Systeme ineinander
import numpy as np, json
rng=np.random.default_rng(27); n=400000
v=rng.normal(size=(n,3)); v/=np.linalg.norm(v,axis=1)[:,None]; x,y,z=v.T
achsen=[x,y,z]                       # drei Dipole (Anode/Kathode je Achse): 6 Keulen ±x ±y ±z
okt=x*y*z                            # Vorzeichen x·y·z: 8 Keulen zu den Raumdiagonalen (abwechselnd ±)
def keulen(f):                       # Zahl der Vorzeichen-Bereiche mit Spitze: grob über Richtungen der Maxima von |f|
    return None
# Orthogonalität (Mittel über die Kugel): Dipol-Anteile gegen Oktopol x*y*z
orth={f"<{n_}·xyz>":round(float(np.mean(a*okt)),5) for n_,a in zip("xyz",achsen)}
orth.update({"<x·y>":round(float(np.mean(x*y)),5),"<xyz·xyz>":round(float(np.mean(okt*okt)),5),"<x·x>":round(float(np.mean(x*x)),5)})
# Richtungen der stärksten Ausschläge
dirs6=[(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]
dirs8=[(a,b,c) for a in (1,-1) for b in (1,-1) for c in (1,-1)]
s3=1/np.sqrt(3)
max_okt=float(np.max(np.abs(okt))); max_bei_diag=s3**3
out=dict(orthogonalitaet=orth, oktopol_max=round(max_okt,5), erwartet_bei_raumdiagonale=round(max_bei_diag,5),
         oktopol_vorzeichen_der_8_ecken=[int(np.sign(a*b*c)) for a,b,c in dirs8],
         oktopol_auf_achsen=0.0, dipol_auf_diagonale=round(s3,5))
print(json.dumps(out,ensure_ascii=False,indent=1))
