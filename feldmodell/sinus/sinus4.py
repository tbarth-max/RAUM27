# RAUM27 – Herzstück: die vier Sinusfunktionen, u = 16x/(9*l2)
#  f1 = l1 sin u   f2 = 1/(l1 sin u)   f3 = l1 sin^2 u   f4 = l1 sinh u
# und die Sinustransformation, die Flächen zu Räumen verbindet: sin(ux) sin(uy) sin(uz)
import numpy as np, itertools, json, math
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
l1, l2 = 1.0, 1.0
k = 16/(9*l2); P = 2*math.pi/k
out = dict(k=round(k,6), periode_x=round(P,6), halbperiode=round(P/2,6),
  steigung_am_ursprung_sin_und_sinh=round(16*l1/(9*l2),6), f2_kleinster_betrag=1/l1, f3_mittelwert=l1/2, f3_periode=round(P/2,6))
gleich=umgekehrt=0
for v in itertools.product((-1,0,1),repeat=3):
    s=int(np.prod([(-1)**abs(c) for c in v]))
    if s>0: gleich+=1
    else: umgekehrt+=1
out["3D_sinusprodukt_zellen_gleiches_vorzeichen"]=gleich; out["3D_umgekehrtes_vorzeichen"]=umgekehrt
# numerische Probe: Inversion r->1/r bildet r=sin(k th) exakt auf r=1/sin(k th) ab; Berührung an r=1
th=np.linspace(0.01,math.pi/k-0.01,1000); r=np.sin(k*th)
out["inversion_max_fehler"]=float(np.max(np.abs(1/r - 1/np.sin(k*th))))
out["polar_1/sin_ueberstrichener_winkel_grad"]=round(180/k,4)
fig,ax=plt.subplots(2,2,figsize=(12,10))
x=np.linspace(-P,P,4000); u=k*x
a=ax[0,0]
a.plot(x,l1*np.sin(u),label="1  λ₁·sin u  (Welle / Kreis)")
with np.errstate(divide="ignore"):
    y2=1/(l1*np.sin(u)); y2[np.abs(y2)>4]=np.nan
a.plot(x,y2,label="4  1/(λ₁·sin u)  (Spiegelzellen)")
a.plot(x,l1*np.sin(u)**2,label="2  λ₁·sin² u  (Verdopplung)")
y4=l1*np.sinh(u); y4[np.abs(y4)>4]=np.nan
a.plot(x,y4,label="3  λ₁·sinh u  (Wand)")
for yy in (1,-1): a.axhline(yy,color="gray",lw=0.8,ls="--")
a.set_ylim(-4,4); a.set_title("Kartesisch y(x), u = 16x/(9λ₂), λ₁ = λ₂ = 1\nSpiegellinien y = ±1 (gestrichelt): dort berühren sich 1 und 4"); a.legend(fontsize=8,loc="lower right")
a=ax[0,1]; a.set_aspect("equal")
thp=np.linspace(0.001,math.pi-0.001,3000)
for kk,col in ((1.0,"C0"),(16/9,"C1")):
    rr=np.sin(kk*thp); m=rr>0
    a.plot(rr[m]*np.cos(thp[m]),rr[m]*np.sin(thp[m]),col,label=f"r = sin({kk:.2f}·θ)")
    with np.errstate(divide="ignore"):
        ri=1/np.sin(kk*thp); ri[(ri<=0)|(ri>4)]=np.nan
    a.plot(ri*np.cos(thp),ri*np.sin(thp),col,ls=":",label=f"r = 1/sin({kk:.2f}·θ)")
t=np.linspace(0,2*math.pi,400); a.plot(np.cos(t),np.sin(t),"k",lw=0.8,label="Einheitskreis = Spiegel")
a.set_xlim(-3,3); a.set_ylim(-0.5,4); a.set_title("Polar: Sinus innen ↔ 1/Sinus außen,\ngespiegelt am Einheitskreis (Inversion)"); a.legend(fontsize=7)
g=np.linspace(-P,P,600); Xg,Yg=np.meshgrid(g,g); F=np.sin(k*Xg)*np.sin(k*Yg)
a=ax[1,0]; a.contourf(Xg,Yg,F,levels=21,cmap="RdBu"); a.contour(Xg,Yg,F,levels=[0],colors="k",linewidths=1); a.set_aspect("equal")
a.set_title("Fläche: sin(ux)·sin(uy)\nNulllinien = Würfelwände, je Zelle ein runder Bauch, Vorzeichen ±")
with np.errstate(divide="ignore"):
    G=np.clip(1/F,-6,6)
a=ax[1,1]; a.contourf(Xg,Yg,G,levels=25,cmap="RdBu"); a.set_aspect("equal")
a.set_title("Invers: 1/(sin·sin)\nMinimum |1| in der Zellmitte, Wände → unendlich (Gitterlinien)")
plt.tight_layout(); plt.savefig("sinus4.png",dpi=110)
print(json.dumps(out,ensure_ascii=False,indent=1))
