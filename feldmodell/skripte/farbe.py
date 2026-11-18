# Amplitude normieren, Periode als Information: Phasenversatz X gegen Y -> Farbe (gruen = in Phase, rot = X vor, blau = Y vor)
import numpy as np, json
rng=np.random.default_rng(27); N=9; w0=2*np.pi; T=10.0; t=np.linspace(0,T,4001); out={}
def lauf(defekte, amp_rausch=0.3, schwelle_grad=5.0):
    LFx=np.ones((N,N)); LFy=np.ones((N,N))
    for (i,j,achse,d) in defekte: (LFx if achse=='x' else LFy)[i,j]=1+d
    farbe=np.full((N,N),'G'); hits=[]
    for i in range(N):
        for j in range(N):
            ax=(1+amp_rausch*rng.standard_normal(len(t)))*np.sin(w0*LFx[i,j]*t)
            ay=(1+amp_rausch*rng.standard_normal(len(t)))*np.sin(w0*LFy[i,j]*t)
            # Amplitude normieren: nur Phase (analytisches Signal ueber Projektion je Periode am Ende)
            m=t>T-1
            px=np.angle(np.sum(ax[m]*np.exp(-1j*w0*t[m]))); py=np.angle(np.sum(ay[m]*np.exp(-1j*w0*t[m])))
            d=np.degrees(np.angle(np.exp(1j*(px-py))))
            if d>schwelle_grad: farbe[i,j]='R'
            elif d<-schwelle_grad: farbe[i,j]='B'
    return farbe
for name,defe in (("perfekt",[]),("X-Fehler bei (2,3) +1%",[(2,3,'x',0.01)]),("Y-Fehler bei (6,6) +1%",[(6,6,'y',0.01)]),
                  ("beide",[(2,3,'x',0.01),(6,6,'y',0.01)])):
    f=lauf(defe); out[name]=dict(rot=[list(map(int,p)) for p in zip(*np.where(f=='R'))],blau=[list(map(int,p)) for p in zip(*np.where(f=='B'))],gruen=int((f=='G').sum()))
# Vergleich: Amplitude als Traeger bei 30 % Rauschen
amp=[np.std((1+0.3*rng.standard_normal(4000))) for _ in range(81)]
out["amplitude_als_traeger_rauschen_rel"]=round(float(np.mean(amp)),3)
out["phasenversatz_nach_T=10_bei_1%_grad"]=round(0.01*360*T,1)
print(json.dumps(out,ensure_ascii=False,indent=1)); json.dump(out,open('farbe.json','w'),ensure_ascii=False,indent=1)
