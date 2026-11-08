# Hex-Register (16 Zustaende, Zaehler z: Zustand z&15, Ring z>>4) gekoppelt an den 7/9-Stabilitaetslauf
import numpy as np, json, math
rng=np.random.default_rng(27); out={}; Rot=np.array([[0,-1],[1,0]]); b=2.0
# A) Spiegel-Operatoren = Kehrwert an der 1 (positiver Raum, Ring k: Abstand 3^-k im log2)
devA=0
for k in range(9):
    s=3.0**-k
    for h in range(2,8):                       # Flaeche: b0 = innen(0)/aussen(1)
        x=b**(s if h&1 else -s); x2=b**(s if (h^1)&1 else -s); devA=max(devA,abs(x*x2-1))
    for h in range(8,16):                      # Achtel: b2b1b0 je Achse innen/aussen
        X=np.array([b**(s if h>>(2-i)&1 else -s) for i in range(3)]); X2=np.array([b**(s if (h^7)>>(2-i)&1 else -s) for i in range(3)])
        devA=max(devA,float(abs(X*X2-1).max()))
out["A_xor1_xor7_gleich_kehrwert_max_abw"]=float('%.1e'%devA)
# B/C/D) Lauf: je Takt Zustand s=z&15: 0 Ablesen, 1 Uebertrag (Ring nach innen), 2..F Feldschritt (90° + Chaos, 7/9 Lenkung)
def lauf(K,ticks,lenkung=True,bitfehler=0.0,resync=False):
    e=np.zeros((K,24,2)); z=0; ring_echt=0; mism=[]; ablese=[]
    for t in range(ticks):
        if bitfehler and rng.random()<bitfehler: z^=1<<int(rng.integers(0,6))   # Bitfehler im Zaehler
        s=z&15
        if s==0:
            ablese.append(float(np.sqrt((e**2).sum(-1)).mean())); mism.append(abs((z>>4)-ring_echt))
        elif s==1:
            e=np.roll(e,1,axis=0); e[0]=0; ring_echt+=1
            if resync: z=(ring_echt<<4)|1            # Ring aus der Struktur (Frequenz 2^k) gelesen, Zaehler nachgefuehrt
        else:
            moved=np.roll(e,1,axis=1)@Rot.T+rng.uniform(-1,1,e.shape)
            e=(2/9)*moved if lenkung else moved
        z+=1
    rms=np.sqrt((e**2).sum(-1))
    return dict(mittel=round(float(rms.mean()),4), max=round(float(rms.max()),4),
                ring_anfang_mitte_ende=[round(float(x),4) for x in rms.mean(1)[[0,K//2,K-1]]],
                ablesung_mittel=round(float(np.mean(ablese)),4), zaehler_ring_gleich_echter_ring_am_ende=bool((z>>4)==ring_echt) if not bitfehler else None,
                max_ringversatz=int(max(mism)), versatz_ende=int(mism[-1]))
for K in (9,27,81): out[f"B_mit_lenkung_K{K}"]=lauf(K,16*K*20)
out["C_ohne_lenkung_K9"]=lauf(9,16*9*20,lenkung=False)
for res in (False,True):
    r=[lauf(9,16*9*20,bitfehler=1e-2,resync=res) for _ in range(10)]
    out[f"D_bitfehler_1e-2_{'mit' if res else 'ohne'}_resync_10laeufe"]=dict(
        versatz_ende=[x["versatz_ende"] for x in r], max_versatz=[x["max_ringversatz"] for x in r], mittel_e=[x["mittel"] for x in r])
x=1.0; n=0
while x>math.exp(-5): x*=2/9; n+=1
out["E_takte_bis_5tau_rest"]=n; out["E_feldschritte_je_registerzyklus"]=14
print(json.dumps(out,ensure_ascii=False,indent=1)); json.dump(out,open('hex_stabil.json','w'),ensure_ascii=False,indent=1)
