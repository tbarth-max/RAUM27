# Fehlerkurve des Dauerlaeufers: welches Gesetz? linear, Wurzel (Zufall), Potenz t^b, log, exponentiell
import json, sys, numpy as np
rows=[json.loads(l) for l in open(sys.argv[1])] if len(sys.argv)>1 else None
if rows: t=np.array([r['takt'] for r in rows],float); e=np.abs(np.array([r['bilanzfehler'] for r in rows],float))
else:    t=np.array([1e3,2e4,8e4,1.2e5,5.5e5]); e=np.array([2.84e-10,5.42e-9,2.28e-8,3.62e-8,1.05e-7])
m=e>0; t,e=t[m],e[m]
def r2(y,f): return 1-np.sum((y-f)**2)/np.sum((y-y.mean())**2)
out={}
a=np.sum(t*e)/np.sum(t*t); out['linear a*t']=(r2(e,a*t),f'a={a:.3e}')
a=np.sum(np.sqrt(t)*e)/np.sum(t); out['Wurzel a*sqrt(t)']=(r2(e,a*np.sqrt(t)),f'a={a:.3e}')
b,la=np.polyfit(np.log(t),np.log(e),1); out['Potenz a*t^b']=(r2(e,np.exp(la)*t**b),f'a={np.exp(la):.3e}, b={b:.3f}')
c=np.polyfit(np.log(t),e,1); out['Log a*ln(t)+c']=(r2(e,np.polyval(c,np.log(t))),f'a={c[0]:.3e}')
k,la2=np.polyfit(t,np.log(e),1); out['Exp a*e^(k t)']=(r2(e,np.exp(la2+k*t)),f'k={k:.3e}')
for n,(q,p) in sorted(out.items(),key=lambda x:-x[1][0]): print(f'{n:18s} R2={q:.4f}  {p}')
b=out['Potenz a*t^b'][1]; print('Grenze 1e-6 (Potenzgesetz) bei Takt ~ %.3g'%((1e-6/np.exp(la))**(1/np.polyfit(np.log(t),np.log(e),1)[0])))
