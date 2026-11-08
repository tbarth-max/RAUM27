# Spaene mit Groessenstreuung je Ebene; Geschwindigkeit quadriert sich; Verzug-Streuung und Tunnel (Spiegel 0.9, Vorhalt 12.54)
import numpy as np, math, json
rng=np.random.default_rng(27); phis=math.radians(12.54); w0=2.0; T0=math.tan(phis)/w0; Fp=4*.9/.01; M=200000; out={}
def ebene(k,lo,hi,stufen=1):
    w=w0**(2**k); s_mid=w0/w
    u=rng.uniform(math.log(lo),math.log(hi),M); s=s_mid*np.exp(u)
    phi=np.arctan(w*s*T0)
    if stufen>1:   # Sieb mit Unterstufen: je Stufe eigener Vorhalt (Median der Stufe)
        b=np.minimum(((u-math.log(lo))/(math.log(hi)-math.log(lo))*stufen).astype(int),stufen-1)
        ref=np.array([np.median(phi[b==j]) for j in range(stufen)])[b]
    else: ref=np.full(M,phis)
    T=1/(1+Fp*np.sin(phi-ref)**2)
    p10,p90=np.degrees(np.percentile(phi,[10,90]))
    return dict(ebene=k,verzug_p10_p90=[round(p10,2),round(p90,2)],spanne=round(p90-p10,2),tunnel=round(float(T.mean()),3))
# A: feste relative Streuung Faktor 2 je Ebene
out["A_streuung_faktor2_je_ebene"]=[ebene(k,2**-0.5,2**0.5) for k in range(6)]
# B: Sieb-Fach fuellt die ganze Luecke bis zur naechsten Ebene (Faktor = Geschwindigkeitssprung w_k)
out["B_streuung_ganze_luecke"]=[ebene(k,(w0**(2**k))**-0.5,(w0**(2**k))**0.5) for k in range(5)]
# B mit Unterstufen: wie viele Stufen fuer Tunnel >= 0.9?
need=[]
for k in range(5):
    gap=w0**(2**k); n=1
    while n<=4096:
        r=ebene(k,gap**-0.5,gap**0.5,stufen=n)
        if r["tunnel"]>=0.9: break
        n*=2
    need.append(dict(ebene=k,luecke=gap,stufen_fuer_tunnel_0_9=n,tunnel=r["tunnel"],stufen_je_faktor2=round(n/max(math.log2(gap),1),2)))
out["B_noetige_unterstufen"]=need
print(json.dumps(out,ensure_ascii=False,indent=1)); json.dump(out,open('spaene.json','w'),ensure_ascii=False,indent=1)
