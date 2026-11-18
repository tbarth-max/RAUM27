# RAUM27 – Herzstück über alle Ebenen prüfen (Schnitte, Sinus dazwischen, Spiegel an der Eins, log-Uhr, 90°-Sprung,
# Felder schneller / Teilchen kleiner, 6 Tropfen außen-/8 Tropfen innen-Gewichte)
import numpy as np, itertools, math, json
from fractions import Fraction as Fr
out={}
k0=16/9
# T1 Schnitte und Quadranten je Ebene n (Frequenz 2^n): 8 Oktanten, Vorzeichenparität 13/14 im 3x3x3-Zellblock
t1=[]
for n in range(5):
    k=k0*2**n; h=math.pi/k                       # Zellbreite = Halbperiode
    signs=[]
    for v in itertools.product((-1,0,1),repeat=3):
        p=[(c+0.5)*h for c in v]                   # Zellmitte
        signs.append(np.sign(np.prod([math.sin(k*q) for q in p])))
    ref=signs[13]                                  # Mittelzelle
    gleich=sum(1 for s in signs if s==ref)
    okt=len({tuple(int(np.sign(math.sin(k*((c+0.5)*h))) ) for c in v) for v in itertools.product((0,-1),repeat=3)})
    t1.append(dict(ebene=n, k=round(k,4), oktanten=okt, gleich=gleich, umgekehrt=27-gleich))
out["T1_schnitte_parität_je_ebene"]=t1
# T2 Spiegel an der Eins je Ebene: Inversion von r=sin(k th) ergibt r=1/sin(k th); Berührung r=1 bei k th = 90°
t2=[]
for n in range(5):
    k=k0*2**n; th=np.linspace(1e-3,math.pi/k-1e-3,2001); r=np.sin(k*th)
    t2.append(dict(ebene=n, inversion_fehler=float(np.max(np.abs(1/r-1/np.sin(k*th)))), beruehrung_bei_grad=round(90/k,4), r_min_aussen=round(float(np.min(1/r)),6)))
out["T2_spiegel_je_ebene"]=t2
# T3 log-Uhr und 90°-Sprung: Lage von d bei log10(d) Umdrehung; Dekaden selbstähnlich
marks=[math.log10(d) for d in range(1,10)]
dek=[[round(math.log10(d*10**n)-n,12) for d in range(1,10)] for n in range(4)]
out["T3_marken"]=[round(m,4) for m in marks]
out["T3_dekaden_identisch"]=all(d==dek[0] for d in dek)
out["T3_7_9_gegen_log6"]=dict(sieben_neuntel=round(7/9,6), log10_6=round(math.log10(6),6), rel_abstand=round(abs(7/9-math.log10(6))/math.log10(6),6))
# 90°-Sprung als Übertrag: Zahl -> (Achse = Dekade, Winkel = Mantisse); 9.999.. bleibt unter 1 Umdrehung
def uhr(x): n=math.floor(math.log10(x)); return n, math.log10(x)-n
out["T3_beispiele"]={str(x):[uhr(x)[0],round(uhr(x)[1],6)] for x in (1,6,9,9.999999,10,60,99.99,100)}
# T4 Benford: multiplikativer Prozess (selbstähnlich) gegen additiver
rng=np.random.default_rng(27)
def erste(x): return (x/10**np.floor(np.log10(x))).astype(int)
mult=np.prod(rng.uniform(0.5,2.0,(100000,30)),axis=1); add=rng.uniform(1,10,100000)
ben=np.array([math.log10(1+1/d) for d in range(1,10)])
def anteil(x): e=erste(x); return np.array([np.mean(e==d) for d in range(1,10)])
am,aa=anteil(mult),anteil(add)
out["T4_benford"]=dict(soll=[round(b,3) for b in ben], multiplikativ=[round(a,3) for a in am], additiv=[round(a,3) for a in aa],
    max_abw_mult=round(float(np.max(np.abs(am-ben))),4), max_abw_add=round(float(np.max(np.abs(aa-ben))),4))
# T5 Phasenverschiebung Feld–Teilchen je Schale: Feldfrequenz verdoppelt sich je Schale (1,2,4,8,16);
#   Teilchen = träges Glied mit Antwortzeit tau (∝ Größe). Phasenverzug phi = atan(w tau), Verlustanteil je Zyklus ∝ sin(phi)·cos(phi)
t5=[]
for n in range(5):
    w=2*math.pi*2**n
    for fall,tau in (("Teilchen gleich groß",0.05),("Teilchen halbiert je Schale",0.05/2**n)):
        phi=math.atan(w*tau); verlust=math.sin(phi)*math.cos(phi)
        t5.append(dict(schale=n, feld_frequenz=2**n, fall=fall, phasenverzug_grad=round(math.degrees(phi),3), verlustanteil=round(verlust,4)))
out["T5_feld_schneller_teilchen_kleiner"]=t5
# T6 6 Tropfen (Flächen) und 8 Tropfen (Ecken): exakte Gewichte des isotropen 6+8-Gitters
w0,w6,w8=Fr(2,9),Fr(1,9),Fr(1,72)
out["T6_gewichte"]=dict(ruhe=str(w0), flaechen_gesamt=str(6*w6), ecken_gesamt=str(8*w8), nachbarn_gesamt=str(6*w6+8*w8),
    summe=str(w0+6*w6+8*w8), verhaeltnis_flaechen_zu_ecken=str((6*w6)/(8*w8)), isotrop=(2*w6+8*w8==3*(8*w8)))
print(json.dumps(out,ensure_ascii=False,indent=1))
