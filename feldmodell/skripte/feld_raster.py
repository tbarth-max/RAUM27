# Raster (6 Schnitte x 8 Felder, Zyklus 1234, Ringe nach innen) im Feldmodell Stufe 3
# Positiver Raum, Zentrum (1,1,1). Log-Koordinate u = log_b(x) dient nur zum Rechnen; Werte bleiben positiv.
import numpy as np, itertools as it, json, math
rng=np.random.default_rng(27); out={}
b=2.0; eps=0.3; a=np.array([0.7,0.5,0.4])   # Dipol-Staerke je Achse (6 Achsentropfen), eps = Oktopol (8 Diagonaltropfen)
def F(x):                       # Feld: Achsenanteil (Produkt) x Diagonalanteil (Wechselwirkung), immer positiv
    u=np.log(x)/np.log(b); return np.exp(u@a)*np.exp(eps*u[...,0]*u[...,1]*u[...,2])
def cube(k):                    # 3x3x3 um (1,1,1), Ring k: Log-Abstand 3^-k
    s=3.0**-k; g=np.array([b**(-s),1.0,b**s]); X=np.stack(np.meshgrid(g,g,g,indexing='ij'),-1); return F(X)
def rebuild_err(f):
    e=[]
    for c in it.product((0,2),repeat=3):
        i,j,k=c; r=f[i,j,1]*f[i,1,k]*f[1,j,k]*f[1,1,1]/(f[i,1,1]*f[1,j,1]*f[1,1,k]); e.append(abs(r/f[c]-1))
    return max(e)
# R1 Rueckbau der 8 Achtel aus den 6 Schnitten je Ring
R1=[rebuild_err(cube(k)) for k in range(6)]
out["R1_rueckbaufehler_je_ring"]=[float('%.3e'%v) for v in R1]
out["R1_verhaeltnis_ring_zu_ring"]=[round(R1[k]/R1[k+1],3) for k in range(5)]
def rb(eps_):
    global eps; e0=eps; eps=eps_; v=rebuild_err(cube(0)); eps=e0; return v
out["R1_kontrolle_ohne_oktopol"]=float('%.1e'%rb(0.0))
# R2 Zyklus 1234 in jedem der 6 Schnitte: Produkt der Feldfaktoren ueber einen Umlauf (neutral = 1)
corners=[(-1,1),(-1,-1),(1,-1),(1,1)]
prods=[]; okt={}
for ax in range(3):
    for side in (-1,1):
        for k in range(4):
            s=3.0**-k; P=1.0
            for e in corners:
                u=np.zeros(3); u[ax]=side*s; o=[i for i in range(3) if i!=ax]; u[o[0]]=e[0]*s; u[o[1]]=e[1]*s
                x=b**u; P*=F(x)/F(np.ones(3))**0
                if k==0: key=tuple((x>1).astype(int)); okt[key]=okt.get(key,0)+1
            # normiert auf Mittelpunkt der Schnittflaeche
            uc=np.zeros(3); uc[ax]=side*s; prods.append(P/F(b**uc)**4)
out["R2_umlaufprodukt_max_abweichung_von_1"]=float('%.1e'%max(abs(p-1) for p in prods))
out["R2_besuche_je_achtel_pro_vollzyklus"]=sorted(okt.values())
# R3 Partikel mit Sieb auf den Ringen (nach innen: Feld x f, Loch x h je Ring), Antwortzeit ~ Groesse
N=200000; s=np.exp(rng.uniform(math.log(3.0**-6),0,N)); T0=0.05
def lauf(f,h,sieb=True,R=5):
    n=np.clip(np.floor(np.log(s)/np.log(h)).astype(int),0,R-1) if sieb else rng.integers(0,R,N)
    res=[]
    for k in range(R):
        m=n==k; phi=np.arctan(2*math.pi*f**k*s[m]*T0)
        res.append(dict(ring=k,anzahl=int(m.sum()),verzug_grad=round(float(np.degrees(phi).mean()),2),
                        verlust_je_schritt=round(float((np.sin(phi)*np.cos(phi)).mean()),4),
                        verlust_je_zyklus_1234=round(float(4*(np.sin(phi)*np.cos(phi)).mean()),4)))
    sp=[r["verzug_grad"] for r in res[:-1]]   # letzter Ring = Sammelbecken
    return dict(ringe=res,spreizung_grad=round(max(sp)-min(sp),2))
out["R3a_raster_passt (Feld x3, Loch x1/3)"]=lauf(3,1/3)
out["R3b_gestern_b2 (Feld x2, Loch x1/2)"]=lauf(2,1/2)
out["R3c_gemischt (Feld x3, Loch x1/2)"]=lauf(3,1/2)
out["R3d_gemischt (Feld x2, Loch x1/3)"]=lauf(2,1/3)
out["R3e_ohne_sieb (Feld x3)"]=lauf(3,1/3,sieb=False)
print(json.dumps(out,ensure_ascii=False,indent=1)); json.dump(out,open('feld_raster.json','w'),ensure_ascii=False,indent=1)
