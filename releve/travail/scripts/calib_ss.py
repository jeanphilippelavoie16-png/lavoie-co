import numpy as np
# bord ext gauche / droit de la fondation principale (px redressé P1) selon py
L=np.array([(300,541),(822,522),(1500,497),(1774,481)]); R=np.array([(300,1909),(822,1922),(1774,1957)])
aL=np.polyfit(L[:,0],L[:,1],1); aR=np.polyfit(R[:,0],R[:,1],1)
xl=lambda py: np.polyval(aL,py); xr=lambda py: np.polyval(aR,py)
# chaîne des poutres (py≈822) -> u normalisé -> pouces (cotes lues)
U=[(0,0)]+[((px-522)/1400,v) for px,v in [(554,10),(932,132),(1232,228),(1520,324),(1892,446)]]+[(1,456)]
def X(px,py):
    u=(px-xl(py))/(xr(py)-xl(py)); us,vs=zip(*U)
    if u<0: return round(u*456,1)
    if u>1: return round(456+(u-1)*456,1)
    return round(float(np.interp(u,us,vs)),1)
# axe vertical central (px py -> pouces y) d'après cotes lues
Yp=[(160,440),(338,380),(370,370),(880,204),(1025,157),(1505,10),(1536,0),(1697,-48)]
def Y(py):
    ps,vs=zip(*Yp); return round(float(np.interp(py,ps,vs)),1)
if __name__=="__main__":
    for n,(px,py) in {"fen arr centre":(1015,300),"fen avant centre":(1717,1536),"caveau g ext":(1203,200),"cheminee ext":(448,1070),"conduit":(470,1070),"conduit2":(494,1070)}.items():
        print(n,X(px,py),Y(py))
    print("chem y",Y(1036),Y(1105),"flue y",Y(1052),Y(1090))
