# RAUM27 geschlossenes Feldmodell – alle Regeln zusammen, ein Lauf
import numpy as np, math, json
rng=np.random.default_rng(27); R={}
# 1) Ebenenzyklus XY -> XZ -> XT -> XY  (Achsen X,Y,Z,T; X fest, freie Achse Y->Z->T->Y)
P=np.zeros((3,3)); P[1,0]=P[2,1]=P[0,2]=1          # Y->Z, Z->T, T->Y  (Spalten = Bild von Y,Z,T)
d=np.ones(3)/3**.5; ang=math.degrees(math.acos((np.trace(P)-1)/2))
R["1_ebenenzyklus"]=dict(det=round(float(np.linalg.det(P)),6), drehwinkel_grad=round(ang,3),
    achse_ist_diagonale=bool(np.allclose(P@d,d)), drei_schritte_identitaet=bool(np.allclose(np.linalg.matrix_power(P,3),np.eye(3))))
th=np.linspace(0,2*np.pi,7)[:-1]; V=np.stack([np.sin(th-k*2*np.pi/3) for k in range(3)],1)
R["1_ebenenwechsel_dreht_3phasen_um_120"]=bool(np.allclose(V@P.T, np.stack([np.sin(th-2*np.pi/3-k*2*np.pi/3) for k in range(3)],1)) or
                                            np.allclose(V@P.T, np.stack([np.sin(th+2*np.pi/3-k*2*np.pi/3) for k in range(3)],1)))
R["1_ebenen_auf_der_dekade"]={"XY":1,"XZ":round(10**(1/3),4),"XT":round(10**(2/3),4),"XY_wieder":10}
# 2) Schalen: Feld x2, Sieb x1/2, Verzug aus Regel 'Halbwert = eine Phasenrunde' -> phi*=12.54 Grad
phis=math.radians(12.54); N=200000; s=np.exp(rng.uniform(math.log(2**-6),0,N))
# T0 so, dass der Median-Verzug in Schale 0 = phi*  (Partikel der Schale 0: s in (1/2,1])
m0=(s>0.5); T0=math.tan(phis)/(2*math.pi*np.median(s[m0]))
def schalen(sieb=True):
    n=np.clip(np.floor(np.log(s)/np.log(0.5)).astype(int),0,4) if sieb else rng.integers(0,5,N)
    out=[]
    for k in range(4):
        m=n==k; phi=np.arctan(2*math.pi*2**k*s[m]*T0); pm=float(np.median(phi))
        # Tunnel: Wegphase mit festem Vorhalt 180-12.54, Spiegel R=0.9
        F=4*0.9/(0.1**2); T=1/(1+F*np.sin((math.pi-phis+phi-math.pi))**2)   # Abweichung von 180 = phi - phi*
        out.append(dict(schale=k, verzug_median_grad=round(math.degrees(pm),2),
            dreiphasen_leistung=round(1.5*math.cos(pm),4), tunnel_durchlass_mittel=round(float(T.mean()),3)))
    return out
R["2_mit_sieb"]=schalen(True); R["2_ohne_sieb"]=schalen(False); R["2_T0_aus_regel"]=round(T0,5)
# 3) Innen/aussen gegenlaeufig ueber Spiegel, 2:1, Ring 24
ring=24; meet=sorted({(2*t)%ring for t in range(1,3*ring) if (2*t+1*t)%ring==0})
R["3_treffpunkte_24er_ring_2zu1"]=[m*15 for m in meet]
co=sorted({(2*t)%ring for t in range(1,3*ring) if (2*t-1*t)%ring==0})
R["3_ohne_spiegel_gleichsinnig"]=[m*15 for m in co]
# 4) 16/9-Doppelsinus, Resonanz bei x=1
lam2=16/(9*(math.pi-phis)); R["4_lambda2_fuer_resonanz_x1"]=round(lam2,5); R["4_phase_x1_grad"]=round(math.degrees(16/(9*lam2)),2)
R["4_treffpunkte_16_9"]={"gleichsinnig":16-9,"gegenlaeufig":16+9}
# 5) Raster-Erhaltung: Umlaufprodukt 1234 im positiven Raum
b=2.0; corners=[(-1,1),(-1,-1),(1,-1),(1,1)]; a=np.array([.7,.5,.4]); eps=.3
F_=lambda u: math.exp(u@a+eps*u[0]*u[1]*u[2])
dev=0
for ax in range(3):
    for side in (-1,1):
        u0=np.zeros(3); u0[ax]=side; p=1
        for e in corners:
            u=u0.copy(); o=[i for i in range(3) if i!=ax]; u[o[0]],u[o[1]]=e; p*=F_(u)
        dev=max(dev,abs(p/F_(u0)**4-1))
R["5_umlauf_1234_neutral_abweichung"]=float('%.1e'%dev)
print(json.dumps(R,ensure_ascii=False,indent=1)); json.dump(R,open('gesamt.json','w'),ensure_ascii=False,indent=1)
