# RAUM27 Gesamttest v2 – alle Bausteine, jeder Status im Code berechnet
import numpy as np, itertools as it, math, json
from collections import deque
rng=np.random.default_rng(27); R={}; ok={}
phis=math.radians(12.54)
# --- 1 Raum: Rueckbau der Achtel, Faktor 27 je Ring
a=np.array([.7,.5,.4]); F=lambda u: np.exp(u@a+.3*u[...,0]*u[...,1]*u[...,2])
err=[]
for k in range(9):
    s=3.0**-k; g=np.array([-s,0,s]); U=np.stack(np.meshgrid(g,g,g,indexing='ij'),-1); f=F(U)
    err.append(max(abs(f[i,1,1]**0*f[i,j,1]*f[i,1,l]*f[1,j,l]*f[1,1,1]/(f[i,1,1]*f[1,j,1]*f[1,1,l])/f[i,j,l]-1) for i,j,l in it.product((0,2),repeat=3)))
fak=[err[k]/err[k+1] for k in range(1,8)]; R["1_rueckbau_faktor"]=[round(x,2) for x in fak]; ok["1 Rueckbau x27 je Ring"]=all(26<x<28 for x in fak)
# --- 2 Spaene: Geschwindigkeit quadriert, Groesse passend, 4 Siebstufen je Faktor 2
w0=2.0; T0=math.tan(phis)/w0; Fp=360.0; tun=[]; lag=[]
for k in range(5):
    w=w0**(2**k); gap=w; M=100000; u=rng.uniform(-.5*math.log(gap),.5*math.log(gap),M); s=(w0/w)*np.exp(u)
    phi=np.arctan(w*s*T0); n=max(4,int(4*math.log2(gap))); b=np.minimum(((u+.5*math.log(gap))/math.log(gap)*n).astype(int),n-1)
    ref=np.array([np.median(phi[b==j]) for j in range(n)])[b]; tun.append(float((1/(1+Fp*np.sin(phi-ref)**2)).mean())); lag.append(math.degrees(float(np.median(phi))))
R["2_tunnel_je_ebene"]=[round(x,3) for x in tun]; R["2_verzug_median"]=[round(x,2) for x in lag]
ok["2 Tunnel >=0.9 alle Ebenen"]=min(tun)>=0.9; ok["2 Verzug-Median 12.54+-0.5"]=all(abs(x-12.54)<0.5 for x in lag)
# --- 3 Einschwingen per Impuls, Auslesen wenn nichts messbar
Rot=np.array([[0,-1],[1,0]]); tk={}
for K in (9,27,81):
    e=np.zeros((K,24,2)); e[0]=rng.uniform(-1,1,(24,2)); z=0
    while np.abs(e).max()>=1e-12:
        if (z&15)==1: e=np.roll(e,1,axis=0); e[0]=0
        else: e=(2/9)*(np.roll(e,1,axis=1)@Rot.T)
        z+=1
    tk[K]=z
R["3_takte_bis_auslesen"]=tk; ok["3 Einschwingen tiefenunabhaengig"]=len(set(tk.values()))==1
# --- 4 Hex-Register: XOR1/XOR7 = Kehrwert
dev=0
for h in range(8,16):
    X=np.array([2.0**(1 if h>>(2-i)&1 else -1) for i in range(3)]); X2=np.array([2.0**(1 if (h^7)>>(2-i)&1 else -1) for i in range(3)]); dev=max(dev,abs(X*X2-1).max())
ok["4 XOR7 = Kehrwert"]=dev<1e-12
# --- 5 Kreislauf: gleicher Widerstand, Linearvektor, Druck misst Bedarf linear
def kreis(d,K=9,k=.25,ticks=3000):
    A=np.full(K,1.0); D=[]; 
    for t in range(ticks):
        need=np.minimum(np.where(rng.random(K)<.5,2*d*rng.random(K),0),A); A-=need
        up=np.concatenate(([1.0],A[:-1])); f=k*(up-A); A+=f; A[:-1]-=f[1:]; A+=np.maximum(k*(1-A),0)
        if t>ticks//2: D.append((1-A.mean(),need.sum()))
    D=np.array(D); return D[:,0].mean(),D[:,1].mean()
pts=[kreis(d) for d in (0,.002,.004,.008,.016)]; x=np.array([p[1] for p in pts]); y=np.array([p[0] for p in pts])
r2=float(np.corrcoef(x,y)[0,1]**2); R["5_R2_druck_vs_bedarf"]=round(r2,5); R["5_ruhe_defizit"]=pts[0][0]
ok["5 Druck misst Bedarf linear (R2>0.999)"]=r2>0.999; ok["5 Ruhe: Fluss steht"]=pts[0][0]==0
# --- 6 Resonanz 6x8: alle 14 gleichzeitig im Zentrum (mit Eckverbindungen)
Fa=[d for d in it.product((-1,0,1),repeat=3) if sum(map(abs,d))==1]; Ea=list(it.product((-1,1),repeat=3))
def bfs(Rr,links,src):
    L=2*Rr+1; S=set(it.product(range(L),repeat=3)); D={s:0 for s in src}; q=deque(src)
    while q:
        u=q.popleft()
        for d in links:
            w=tuple(u[i]+d[i] for i in range(3))
            if w in S and w not in D: D[w]=D[u]+1; q.append(w)
    return D
Rr=6; L=2*Rr+1; ec=[tuple(c*(L-1) for c in e) for e in it.product((0,1),repeat=3)]; fl=[tuple(Rr+d[i]*Rr for i in range(3)) for d in Fa]
m=(Rr,Rr,Rr); d8=bfs(Rr,Fa+Ea,ec)[m]; d6=bfs(Rr,Fa+Ea,fl)[m]; t8=bfs(Rr,Fa,ec)[m]
R["6_ankunft_8_6_treppe8"]=[d8,d6,t8]; ok["6 8 und 6 gleichzeitig (6+8)"]=d8==d6; ok["6 Treppe nicht im Takt"]=t8!=d6
# --- 7 4D: 24 Nachbarn gleich weit
P=[np.array(v) for v in it.product((-.5,.5),repeat=4)]+[s*np.eye(4)[i] for i in range(4) for s in (1,-1)]
ok["7 4D 24 Nachbarn Abstand 1"]=len(P)==24 and all(abs(np.linalg.norm(p)-1)<1e-12 for p in P)
# --- 8 Normierung: Energie bleibt, Amplitude gleich
N=6; w=[1/9]*6+[1/72]*8; q=np.zeros((N,N,N)); q[0,0,0]=216.0
for t in range(60): q=2/9*q+sum(wt*np.roll(q,d,axis=(0,1,2)) for d,wt in zip(Fa+Ea,w))
R["8_gesamt_streuung"]=[round(float(q.sum()),9),float('%.1e'%q.std())]; ok["8 Energie erhalten, normiert"]=abs(q.sum()-216)<1e-9 and q.std()<1e-3
# --- 9 Farbe im gekoppelten Netz: Phasenfeld eines 1%-Fehlers (stationaer, Laplace), Hof und Ort
N=15; idx=lambda i,j:i*N+j; Lp=np.zeros((N*N,N*N))
for i in range(N):
    for j in range(N):
        for di,dj in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
            ii,jj=i+di,j+dj
            if 0<=ii<N and 0<=jj<N: Lp[idx(i,j),idx(i,j)]+=1; Lp[idx(i,j),idx(ii,jj)]-=1
for i in range(N):   # Rand haengt am Vordruck (Bezugsphase)
    for j in range(N):
        if i in (0,N-1) or j in (0,N-1): Lp[idx(i,j),idx(i,j)]+=1
dw=np.zeros(N*N); dw[idx(5,9)]=0.01*360   # X-Kanal 1 % schneller (Grad je Periode)
phi=np.linalg.solve(Lp,dw).reshape(N,N)
pk=np.unravel_index(np.argmax(phi),phi.shape); R["9_phasen_max_ort"]=[int(pk[0]),int(pk[1])]; R["9_hof_abfall"]=[round(float(phi[5,9+r]),3) for r in range(0,5)]
ok["9 Farbhof zentriert auf Fehler"]=pk==(5,9); ok["9 Hof faellt nach aussen"]=all(phi[5,9+r]>phi[5,9+r+1] for r in range(4))
R["CHECKS"]={k:bool(v) for k,v in ok.items()}; R["ALLE_OK"]=bool(all(ok.values()))
print(json.dumps(R,ensure_ascii=False,indent=1,default=str)); json.dump(R,open('gesamt_v2.json','w'),ensure_ascii=False,indent=1,default=str)
