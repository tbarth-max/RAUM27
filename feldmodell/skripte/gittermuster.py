# Grundgitter Kugel/Wuerfel im Raum, gerechnet wird nur EIN Achtel (x,y,z >= 0) + 3 Richt-Bits
# Bits: Seite (welches Achtel, 3 Bit innen/aussen je Achse = Spiegel), Blick (innen->aussen / aussen->innen), Fluss (hinaus / zurueck)
import numpy as np, itertools as it, json, math
R=6
achtel=[(x,y,z) for x,y,z in it.product(range(R+1),repeat=3)]
def typ(p):
    n0=sum(1 for c in p if c==0)
    return {3:'Zentrum',2:'Achse',1:'Spiegelflaeche',0:'innen'}[n0]
rows=[]
for p in achtel:
    w=max(p); k=round(math.sqrt(sum(c*c for c in p)))   # Wuerfelschale (Chebyshev) / Kugelschale (euklidisch, gerundet)
    rows.append(dict(p=p,wuerfelschale=w,kugelschale=k,typ=typ(p)))
# Vollgitter aus dem Achtel durch Spiegeln (Punkte auf Spiegelflaechen nicht doppelt)
voll=set()
for p in achtel:
    for s in it.product((1,-1),repeat=3): voll.add(tuple(a*b for a,b in zip(p,s)))
print('Achtel-Knoten:',len(achtel),'| Vollgitter durch Spiegeln:',len(voll),'= (2R+1)^3 =',(2*R+1)**3)
print('Typen im Achtel:',{t:sum(1 for r in rows if r['typ']==t) for t in ('Zentrum','Achse','Spiegelflaeche','innen')})
print('Schale | Wuerfelschale-Knoten im Achtel | Kugelschale-Knoten im Achtel')
for s in range(R+1):
    print(s,'|',sum(1 for r in rows if r['wuerfelschale']==s),'|',sum(1 for r in rows if r['kugelschale']==s and r['wuerfelschale']<=R))
json.dump([{**r,'p':list(r['p'])} for r in rows],open('gittermuster_achtel.json','w'))
