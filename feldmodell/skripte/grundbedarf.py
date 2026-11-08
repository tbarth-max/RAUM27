# Grundbedarf: Boden G je Zelle, egal wo. Reservoir an jedem Ort (lokale Eins), Entnahme nur aus dem Ueberschuss ueber G.
import numpy as np, json
rng=np.random.default_rng(27); X=1.0; G=0.9; kappa=1/9; out={}
def lauf(N,viel_ort,ticks=20000,boden=True,ueberall=True,will=0.05):
    p=np.full((N+2,N+2),X); mins=[]; viel_bekommen=0.0
    vi,vj={"mitte":(N//2+1,N//2+1),"rand":(1,N//2+1),"ecke":(1,1)}[viel_ort]
    for t in range(ticks):
        for _ in range(max(1,N*N//81)):
            i,j=rng.integers(1,N+1,2); a=0.004*rng.random(); p[i,j]-=min(a,max(p[i,j]-G,0) if boden else p[i,j])
        a=will; nimm=min(a,max(p[vi,vj]-G,0) if boden else p[vi,vj]); p[vi,vj]-=nimm; viel_bekommen+=nimm
        lap=np.zeros_like(p); lap[1:-1,1:-1]=p[:-2,1:-1]+p[2:,1:-1]+p[1:-1,:-2]+p[1:-1,2:]-4*p[1:-1,1:-1]
        p[1:-1,1:-1]+=kappa*lap[1:-1,1:-1]
        if ueberall: p[1:-1,1:-1]+=(X-p[1:-1,1:-1])*(7/9)         # jeder Ort hat sein Reservoir (lokale Eins)
        p[0,:]=p[-1,:]=X; p[:,0]=p[:,-1]=X
        if t>1000: mins.append(p[1:-1,1:-1].min())
    q=p[1:-1,1:-1]
    return dict(minimum_ueberall_jemals=round(float(min(mins)),4), boden_gehalten=bool(min(mins)>=G-1e-12),
                mittel=round(float(q.mean()),4), nachbar_vom_vielentnehmer=round(float(p[vi+1,vj]),4),
                vielentnehmer_bekam_je_takt=round(viel_bekommen/ticks,4))
for N in (9,27):
    for ort in ("mitte","rand","ecke"): out[f"N{N}_{ort}"]=lauf(N,ort)
out["N9_mitte_OHNE_boden_nur_randreservoir"]=lauf(9,"mitte",boden=False,ueberall=False)
out["N9_mitte_will0.5_boden_ohne_lokale"]=lauf(9,"mitte",will=0.5,ueberall=False)
out["N9_mitte_will0.5_ohne_boden_ohne_lokale"]=lauf(9,"mitte",will=0.5,boden=False,ueberall=False)
out["N9_mitte_will0.5_boden_und_lokale"]=lauf(9,"mitte",will=0.5)
out["N27_mitte_will0.5_boden_ohne_lokale"]=lauf(27,"mitte",will=0.5,ueberall=False)
print(json.dumps(out,ensure_ascii=False,indent=1)); json.dump(out,open('grundbedarf.json','w'),ensure_ascii=False,indent=1)
