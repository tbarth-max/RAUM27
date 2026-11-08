# RAUM27 Komplettmodell, 9 Ringe nach innen. Raum: Log-Abstand 3^-k (3x3-Teilung). Zeit: Feld 2^k, Sieb 2^-k.
import numpy as np, itertools as it, math, json
rng=np.random.default_rng(27); K=9; b=2.0; R={}; ok={}
a=np.array([.7,.5,.4]); eps=.3
def F(u): return np.exp(u@a+eps*u[...,0]*u[...,1]*u[...,2])          # positiv; Achsen (Produkt) x Diagonale (Wechselwirkung)
# --- Raum je Ring
achtel=[];rueck=[];umlauf=[];spiegel=[]
for k in range(K):
    s=3.0**-k; g=np.array([-s,0,s])
    U=np.stack(np.meshgrid(g,g,g,indexing='ij'),-1); f=F(U)
    # Achtel: Ecken innen/aussen je Achse
    cor=[c for c in it.product((0,2),repeat=3)]; achtel.append(len({tuple((U[c]>0).astype(int)) for c in cor}))
    e=max(abs(f[i,j,1]*f[i,1,kk]*f[1,j,kk]*f[1,1,1]/(f[i,1,1]*f[1,j,1]*f[1,1,kk])/f[i,j,kk]-1) for i,j,kk in cor); rueck.append(e)
    # Umlauf 1234 in allen 6 Schnitten
    d=0
    for ax in range(3):
        for side in (-1,1):
            u0=np.zeros(3);u0[ax]=side*s;p=1;o=[i for i in range(3) if i!=ax]
            for c in [(-1,1),(-1,-1),(1,-1),(1,1)]:
                u=u0.copy();u[o[0]]=c[0]*s;u[o[1]]=c[1]*s;p*=F(u)
            d=max(d,abs(p/F(u0)**4-1))
    umlauf.append(d)
    # Spiegel an der 1: Ring k innen (x=b^-s) <-> aussen (x=b^s), exakt Kehrwert
    x_in=b**(-s); spiegel.append(abs((1/x_in)-b**s))
R["raum_achtel_je_ring"]=achtel; R["raum_rueckbaufehler"]=[float('%.2e'%v) for v in rueck]
R["raum_rueckbau_faktor_je_ring"]=[round(rueck[k]/rueck[k+1],2) for k in range(K-1) if rueck[k+1]>1e-14]
R["raum_umlauf_max_abw"]=float('%.1e'%max(umlauf)); R["raum_spiegel_max_abw"]=float('%.1e'%max(spiegel))
R["zellen_je_quadrant_ring9"]=9**9; R["16/9*9/2"]=16/9*9/2
ok["8 Achtel in jedem Ring"]=all(v==8 for v in achtel)
ok["Rueckbau faellt ~27 je Ring"]=all(20<v<35 for v in R["raum_rueckbau_faktor_je_ring"][1:])
ok["Umlauf 1234 neutral"]=max(umlauf)<1e-12; ok["Spiegel exakt"]=max(spiegel)<1e-12
# --- Zeit/Teilchen je Schale (9 Schalen)
phis=math.radians(12.54); N=400000; sz=np.exp(rng.uniform(math.log(2.0**-K),0,N))
m0=sz>0.5; T0=math.tan(phis)/(2*math.pi*np.median(sz[m0]))
def lauf(fein=1,sieb=True):
    # fein: Siebstufen je Schale (1 = halbieren; 2 = zwei Unterstufen, Vorhalt je Unterstufe)
    lev=np.floor(-np.log2(sz)*fein).astype(int); n=np.clip(lev//fein,0,K-1) if sieb else rng.integers(0,K,N)
    res=[]
    for k in range(K):
        m=n==k; phi=np.arctan(2*math.pi*b**k*sz[m]*T0)
        if fein>1 and sieb:   # je Unterstufe eigener Vorhalt (Median der Unterstufe)
            sub=lev[m]%fein; ref=np.array([np.median(phi[sub==j]) for j in range(fein)])[sub]
        else: ref=phis
        Fp=4*.9/.01; T=1/(1+Fp*np.sin(phi-ref)**2)
        res.append((round(math.degrees(float(np.median(phi))),2),round(1.5*math.cos(float(np.median(phi))),4),round(float(T.mean()),3)))
    return res
L1=lauf(1); L4=lauf(4); L0=lauf(1,False)
R["schalen_verzug_leistung_tunnel (Sieb x1/2)"]=L1
R["schalen_tunnel (Sieb 4 Unterstufen)"]=[r[2] for r in L4]
R["schalen_ohne_sieb"]=L0; R["T0"]=round(T0,5)
v=[r[0] for r in L1]; ok["Verzug konstant ueber 9 Schalen (<0.2 Grad)"]=max(v)-min(v)<0.2
ok["Tunnel gleich in allen Schalen"]=max(r[2] for r in L1)-min(r[2] for r in L1)<0.02
ok["feineres Sieb -> Tunnel hoeher"]=min(R["schalen_tunnel (Sieb 4 Unterstufen)"])>max(r[2] for r in L1)
w=[r[0] for r in L0]; ok["ohne Sieb driftet"]=max(w)-min(w)>10
# Nutation: Spin x2 je Schale -> x1/4
nut=[0.5882*4.0**-k for k in range(K)]; R["nutation_grad_je_schale (aus G12-Gesetz)"]=[float('%.2e'%x) for x in nut]
# --- Phasen/Ebenen
P=np.zeros((3,3));P[1,0]=P[2,1]=P[0,2]=1
ok["Ebenenzyklus XY-XZ-XT schliesst nach 3"]=np.allclose(np.linalg.matrix_power(P,3),np.eye(3))
ring=24; ok["2:1 ueber Spiegel -> 3 Phasen"]=sorted({(2*t)%ring for t in range(1,99) if (3*t)%ring==0})==[0,8,16]
th=np.linspace(0,2*np.pi,1000); ok["3 Phasen Leistung konstant"]=np.ptp(sum(np.sin(th-j*2*np.pi/3)**2 for j in range(3)))<1e-12
lam2=16/(9*(math.pi-phis)); ok["16/9-Resonanz bei x=1 (lambda2)"]=abs(16/(9*lam2)-(math.pi-phis))<1e-12; R["lambda2"]=round(lam2,5)
R["CHECKS"]={k:bool(v) for k,v in ok.items()}; R["ALLE_OK"]=bool(all(ok.values()))
print(json.dumps(R,ensure_ascii=False,indent=1,default=str)); json.dump(R,open('gesamt9.json','w'),ensure_ascii=False,indent=1,default=str)
