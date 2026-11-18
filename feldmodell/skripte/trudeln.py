# Kreisel im Wuerfelfeld (Rueckstellung zur Achse z), Spin w3; Trudeln und 180°-Inversion
import numpy as np, math, json
I1,I3,k,th0=1.0,0.5,1.0,math.radians(10)
from scipy.integrate import solve_ivp
def run(w3):
    a=I3*w3; b=a*math.cos(th0)
    def f(t,y):
        th,thd,ph=y; phd=(b-a*math.cos(th))/(I1*math.sin(th)**2)
        return [thd,(phd**2*I1*math.sin(th)*math.cos(th)-a*phd*math.sin(th)-k*math.sin(th))/I1,phd]   # Rueckstellmoment -k sin
    ev=lambda t,y: abs(y[2])-2*math.pi-0.2; ev.terminal=True
    Tp=2*math.pi*a/k*1.3
    sol=solve_ivp(f,(0,Tp*3),[th0,0,0],events=ev,rtol=1e-10,atol=1e-12,max_step=2*math.pi/w3/20)
    T,TH,PH=sol.t,sol.y[0],np.abs(sol.y[2])
    d=np.stack([np.sin(TH)*np.cos(PH),np.sin(TH)*np.sin(PH)],1)
    i_half=np.searchsorted(PH,math.pi); i_full=np.searchsorted(PH,2*math.pi)
    # Inversion: jeder Punkt der ersten Halbrunde + sein 180°-Partner
    res=[]
    for i in range(0,i_half,max(1,i_half//400)):
        j=np.searchsorted(PH,PH[i]+math.pi); res.append(np.linalg.norm(d[i]+d[j]))
    return dict(spin=w3, neigung_grad=round(math.degrees(th0),2), trudel_nutation_grad=round(math.degrees(TH.max()-TH.min()),5),
                praezession_umlaufzeit=round(float(T[i_full]),3), mittlere_achse_ueber_umlauf=float('%.2e'%np.linalg.norm(d[:i_full].mean(0))),
                rest_nach_180_inversion=float('%.2e'%max(res)), rest_ohne_inversion=round(float(np.linalg.norm(d,axis=1).max()),4))
out=[run(w) for w in (5,10,20,40)]
for r in out: print(r)
json.dump(out,open('trudeln.json','w'),indent=1)
