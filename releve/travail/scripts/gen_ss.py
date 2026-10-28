import json, sys
sys.path.insert(0,'.')
from calib import X, Y
OUT="/home/user/lavoie-co/releve/travail/extraction/SS.json"
def D(v,src,photo="P1",ref=None,note=None):
    d={"valeur":v,"source":src,"photo":photo if src!="ILLISIBLE" or photo else None}
    if ref: d["ref"]=ref
    if note: d["note"]=note
    return d
def E(px,py): return [X(px,py),Y(py)]
NE="ESTIMÉ : mesuré dans P1 redressé, calibrage par morceaux sur les cotes lues (chaîne des poutres en x, chaîne intérieure 13'-10\"/3'-11\"/12'-3\" en y), correction de perspective linéaire"

# ---------------- COTES ----------------
C=[]
def cote(txt,val,px,empl,mes,alt=None,photo="P1",lect=None):
    c={"id":f"cote-SS-{len(C)+1:03d}","texte_original":txt,"valeur":val,"lecture_1":lect or txt,"lecture_2":None,
       "statut":"provisoire","photo":photo,"px":px,"emplacement":empl,"mesure":mes}
    if alt: c["alternatives"]=alt
    C.append(c); return c["id"]
# arrière (haut de l'image)
cote("38'-0\"",456,[1311,122],"chaîne arrière (haut), rang 3 (hors-tout), ligne la plus éloignée du mur","hors-tout x de la fondation principale, nu ext. mur gauche (mur-SS-004) au nu ext. mur droit (mur-SS-002)")
cote("18'-3\"",219,[915,150],"chaîne arrière, rang 2, 1er segment depuis la gauche","du nu ext. du mur gauche (mur-SS-004) au nu ext. du mur gauche du caveau à légumes (mur-SS-005)")
cote("9'-0\"",108,[1361,140],"chaîne arrière, rang 2, 2e segment (devant le caveau)","largeur hors-tout du caveau à légumes : nu ext. mur-SS-005 au nu ext. mur-SS-007")
cote("10'-9\"",129,[1741,152],"chaîne arrière, rang 2, 3e segment","du nu ext. du mur droit du caveau (mur-SS-007) au nu ext. du mur droit principal (mur-SS-002)")
cote("13'-0\"",156,[798,290],"chaîne arrière, rang 1 (ouvertures), 1er segment depuis la gauche","du nu ext. du mur gauche (mur-SS-004) à l'axe (meneau) de la fenêtre arrière ouv-SS-001")
cote("6'-8\"",80,[1022,310],"chaîne arrière, rang 1, au-dessus de la fenêtre arrière (texte de part et d'autre du trait d'axe)","largeur de la fenêtre arrière ouv-SS-001 (ouverture brute probable)",alt=[{"texte":"6'-3\"","valeur":75,"raison":"confusion 3/8 possible ; la longueur dessinée (~227 px ≈ 73 po) est semblable à celle de la fenêtre avant cotée 6'-3\""}])
cote("10\"",10,[1517,248],"caveau à légumes, mur droit, cote horizontale entre deux points","épaisseur du mur droit du caveau (mur-SS-007)")
cote("22\"",22,[1567,217],"caveau à légumes, côté droit, cote horizontale sur les tiretés de semelle","largeur de la semelle sous le mur droit du caveau (tireté int. au tireté ext.)")
cote("5'-0\"",60,[1587,267],"cote verticale à droite du caveau, entre le nu ext. du mur arrière principal et la ligne d'attache du dos du caveau","saillie du caveau : du nu ext. du mur arrière (mur-SS-003) au nu ext. du mur du fond du caveau (mur-SS-006)")
cote("3'-6\"",42,[1275,300],"à l'intérieur du caveau, texte entre le mur gauche du caveau et une ligne d'attache verticale descendant à l'axe de la porte 2'-6\" ; pas de ligne de cote horizontale visible","DOUTEUX : du nu ext. du mur gauche du caveau (mur-SS-005, x=219) à l'axe de la porte ouv-SS-008 (retenu : écart mesuré en image ≈ 38 po)",alt=[{"texte":"3'-6\" depuis le nu int. du mur gauche du caveau","valeur":42,"raison":"texte placé à l'intérieur du caveau ; ligne de départ non visible ; écart mesuré en image axe-porte / nu int. ≈ 28 po seulement"}])
# gauche
cote("31'-8\"",380,[272,950],"chaîne gauche, rang 3 (hors-tout)","hors-tout y de la fondation principale, nu ext. mur avant (mur-SS-001) au nu ext. mur arrière (mur-SS-003)")
cote("16'-8\"",200,[417,675],"chaîne gauche, rang 2, 1er segment depuis l'arrière","du nu ext. du mur arrière (mur-SS-003) à l'axe de la fenêtre gauche haute ouv-SS-006")
cote("4'-0\"",48,[392,1030],"chaîne gauche, rang 2, 2e segment depuis l'arrière","de l'axe de la fenêtre ouv-SS-006 à la face avant (côté rue) du massif de cheminée (mur-SS-011)")
cote("7'-0\"",84,[382,1240],"chaîne gauche, rang 2, 3e segment depuis l'arrière","de la face avant du massif de cheminée à l'axe de la fenêtre gauche basse ouv-SS-007",alt=[{"texte":"1'-0\"","valeur":12,"raison":"7 écrit comme un 1 ; rejeté : la chaîne ne somme à 31'-8\" qu'avec 7'-0\", et la longueur dessinée ≈ 88 po"}])
cote("4'-0\"",48,[370,1457],"chaîne gauche, rang 2, dernier segment (côté rue)","de l'axe de la fenêtre ouv-SS-007 au nu ext. du mur avant (mur-SS-001)")
cote("3'-0\"",36,[467,965],"chaîne gauche, rang 1, fenêtre haute","largeur de la fenêtre gauche haute ouv-SS-006")
cote("3'-0\"",36,[442,1375],"chaîne gauche, rang 1, fenêtre basse (près de l'évier à lessive)","largeur de la fenêtre gauche basse ouv-SS-007",alt=[{"texte":"1'-0\"","valeur":12,"raison":"1er chiffre peu net ; longueur dessinée ≈ 37 po → 3'-0\""}])
cote("22\"",22,[605,642],"mur gauche, côté intérieur, cote horizontale entre les tiretés de semelle","largeur de la semelle du mur de fondation gauche (tireté ext. au tireté int.)")
cote("10\"",10,[605,686],"mur gauche, côté intérieur, juste sous la cote 22\"","épaisseur du mur de fondation gauche (mur-SS-004)")
# droite
cote("31'-8\"",380,[2172,975],"chaîne droite, rang 3 (hors-tout)","hors-tout y, nu ext. mur avant au nu ext. mur arrière, côté droit")
cote("6'-0\"",72,[2005,465],"chaîne droite, rang 2, 1er segment depuis l'arrière","du nu ext. du mur arrière (mur-SS-003) à l'axe (meneau) de la fenêtre droite haute ouv-SS-003")
cote("10'-8\"",128,[2022,765],"chaîne droite, rang 2, 2e segment","de l'axe de la fenêtre ouv-SS-003 à l'axe de la fenêtre droite basse ouv-SS-004")
cote("8'-9\"",105,[2032,1140],"chaîne droite, rang 2, 3e segment","de l'axe de la fenêtre ouv-SS-004 à l'axe de la porte 2'-8\" ouv-SS-005",alt=[{"texte":"8'-5\"","valeur":101,"raison":"9/5 peu net ; rejeté : la chaîne ne somme à 31'-8\" qu'avec 8'-9\""}])
cote("6'-3\"",75,[2042,1410],"chaîne droite, rang 2, dernier segment (côté rue)","de l'axe de la porte ouv-SS-005 au nu ext. du mur avant (mur-SS-001)")
cote("6'-8\"",80,[1942,580],"chaîne droite, rang 1, fenêtre haute","largeur de la fenêtre droite haute ouv-SS-003",alt=[{"texte":"6'-3\"","valeur":75,"raison":"confusion 3/8 possible ; longueur dessinée ≈ 72 po"}])
cote("3'-0\"",36,[1952,975],"chaîne droite, rang 1, fenêtre basse","largeur de la fenêtre droite basse ouv-SS-004")
# avant
cote("13'-6\"",162,[727,1757],"chaîne avant (bas), rang 3, 1er segment depuis la gauche","du nu ext. du mur gauche au nu ext. du mur gauche de l'excroissance sous le perron (mur-SS-008)")
cote("6'-0\"",72,[1117,1762],"chaîne avant, rang 3, 2e segment","largeur hors-tout de l'excroissance de fondation sous le perron (mur-SS-008 à mur-SS-010)")
cote("12'-4\"",148,[1477,1765],"chaîne avant, rang 3, 3e segment","du nu ext. du mur droit du perron (mur-SS-010) à l'axe (meneau) de la fenêtre avant ouv-SS-002")
cote("6'-2\"",74,[1842,1760],"chaîne avant, rang 3, 4e segment","de l'axe de la fenêtre avant ouv-SS-002 au nu ext. du mur droit (mur-SS-002)")
cote("6'-2\"",74,[1840,1650],"chaîne avant, rang 2 (isolée)","de l'axe de la fenêtre avant ouv-SS-002 au nu ext. du mur droit — doublon de cote-SS-030")
cote("6'-3\"",75,[1715,1572],"chaîne avant, rang 1, sous la fenêtre avant","largeur de la fenêtre avant ouv-SS-002")
cote("4'-0\"",48,[1302,1625],"cote verticale à droite de l'excroissance du perron","saillie de l'excroissance sous le perron : nu ext. mur avant (mur-SS-001) au nu ext. du mur avant du perron (mur-SS-009)")
cote("10\"",10,[1312,1520],"mur avant, cote verticale entre deux points, dans l'axe de la chaîne intérieure","épaisseur du mur de fondation avant (mur-SS-001)")
cote("18\"",18,[1090,1576],"excroissance du perron, cote horizontale dans le coin arrière-gauche","largeur de la semelle sous le mur gauche du perron (tireté ext. au tireté int.)")
cote("6\"",6,[1072,1608],"excroissance du perron, juste sous la cote 18\"","épaisseur du mur gauche du perron (mur-SS-008)",alt=[{"texte":"8\"","valeur":8,"raison":"6/8 ; lu 6 sur P1 et P7"}])
# intérieur, chaîne des poutres (x)
cote("10\"",10,[540,812],"chaîne intérieure horizontale au-dessus de la poutre arrière, 1er segment (mur gauche)","épaisseur du mur gauche (mur-SS-004)")
cote("9'-10\"",118,[765,812],"chaîne intérieure horizontale, 2e segment","du nu int. du mur gauche à la face gauche de la colonne str-SS-C01",alt=[{"texte":"3'-10\"","valeur":46,"raison":"9 écrit comme un 3 ; rejeté : la chaîne ne somme à 38'-0\" qu'avec 9'-10\", longueur dessinée ≈ 120 po"}])
cote("8\"",8,[935,807],"chaîne intérieure horizontale, 3e segment","largeur de la colonne str-SS-C01")
cote("7'-4\"",88,[1080,810],"chaîne intérieure horizontale, 4e segment","de la face droite de str-SS-C01 à la face gauche de str-SS-C02 (entre-colonnes)")
cote("8\"",8,[1225,812],"chaîne intérieure horizontale, 5e segment (sur le pli du papier)","largeur de la colonne str-SS-C02")
cote("7'-4\"",88,[1307,804],"chaîne intérieure horizontale, 6e segment","de la face droite de str-SS-C02 à la face gauche de str-SS-C03")
cote("8\"",8,[1517,805],"chaîne intérieure horizontale, 7e segment","largeur de la colonne str-SS-C03")
cote("9'-10\"",118,[1705,807],"chaîne intérieure horizontale, 8e segment","de la face droite de str-SS-C03 au nu int. du mur droit",alt=[{"texte":"3'-10\"","valeur":46,"raison":"idem cote-SS-038"}])
cote("10\"",10,[1907,810],"chaîne intérieure horizontale, dernier segment (mur droit)","épaisseur du mur droit (mur-SS-002)")
# intérieur vertical
cote("13'-10\"",166,[1312,635],"chaîne intérieure verticale (x ≈ axe de la porte 2'-6\"), 1er segment depuis l'arrière","du nu int. du mur arrière (mur-SS-003) à l'axe de la poutre arrière str-SS-P01",alt=[{"texte":"15'-10\"","valeur":190,"raison":"3/5 ; rejeté : la chaîne 10+13'-10\"+3'-11\"+12'-3\"+10 = 31'-8\""}])
cote("3'-11\"",47,[1312,952],"chaîne intérieure verticale, 2e segment","entre les axes des deux poutres str-SS-P01 et str-SS-P02")
cote("12'-3\"",147,[1316,1300],"chaîne intérieure verticale, 3e segment","de l'axe de la poutre avant str-SS-P02 au nu int. du mur avant (mur-SS-001)")
# ouvertures écrites dans les étiquettes
cote("PORTE 2'-6\"",30,[1408,380],"étiquette de la porte du mur arrière vers le caveau","largeur de la porte ouv-SS-008")
cote("PORTE 2'-8\"",32,[1795,1281],"étiquette de la porte du mur droit","largeur de la porte ouv-SS-005")
cote("@ 20\" c/c",20,[1207,657],"note des solives, ligne 2","entraxe des solives 2\"x10\" (str-SS-S01)",alt=[{"texte":"@ 16\" c/c","valeur":16,"raison":"vérifié retourné : lu 20 sur P1 et P7"}])
cid={i+1:c["id"] for i,c in enumerate(C)}
def ids(*n): return [cid[k] for k in n]

# ---------------- MURS ----------------
indF=["mur de fondation en béton (hachures de béton au plan)","semelle tiretée dessous","solives 2\"x10\" et poutres 8\"x10\" y prennent appui au dessin (non écrit « porteur »)"]
M=[]
def mur(x1,y1,x2,y2,ep,cl,note,typ="fondation",ind=None):
    M.append({"id":f"mur-SS-{len(M)+1:03d}","type":typ,"porteur":"inconnu","indices_porteur":ind if ind is not None else indF,
              "epaisseur":ep,"x1":x1,"y1":y1,"x2":x2,"y2":y2,"cotes_liees":cl,"note":note})
mur(5,5,451,5,D(10,"LU",ref=cid[34]),ids(27,28,29,30,31,32,34,11,20),"Mur avant (côté rue). Axe à y=5 (DÉDUIT : nu ext. y=0, épaisseur 10\").")
mur(451,5,451,375,D(10,"LU",ref=cid[45]),ids(20,21,22,23,24,25,26,45,1,4,30),"Mur latéral droit. Axe x=451 (DÉDUIT : 38'-0\" − 5).")
mur(451,375,5,375,D(10,"DÉDUIT",note="380 − 10 (mur avant) − 13'-10\" − 3'-11\" − 12'-3\" = 10 ; aucune cote d'épaisseur écrite sur ce mur"),ids(1,2,3,4,5,6,11,20,46,47,48,9),"Mur arrière. Axe y=375 (DÉDUIT : 31'-8\" − 5).")
mur(5,375,5,5,D(10,"LU",ref=cid[19]),ids(11,12,13,14,15,16,17,18,19,37),"Mur latéral gauche (côté cheminée). Axe x=5.")
mur(224,380,224,435,D(10,"ESTIMÉ",note="épaisseur non écrite ; dessinée ≈ comme les murs de 10\""),ids(2,9,10),"Caveau à légumes — mur gauche, contient l'évent grillagé. Nu ext. x=219 (18'-3\" LU) ; part du nu ext. du mur arrière (y=380) jusqu'à l'axe du mur du fond.")
mur(224,435,322,435,D(10,"ESTIMÉ",note="épaisseur non écrite"),ids(9,3),"Caveau à légumes — mur du fond. Nu ext. y=440 (DÉDUIT : 380 + 5'-0\").")
mur(322,435,322,380,D(10,"LU",ref=cid[7]),ids(3,4,7,8,9),"Caveau à légumes — mur droit. Nu ext. x=327 (DÉDUIT : 219 + 9'-0\").")
mur(165,0,165,-45,D(6,"LU",ref=cid[36]),ids(27,33,35,36),"Excroissance de fondation sous le perron avant — mur gauche. Nu ext. x=162 (13'-6\" LU), nu ext. avant y=−48 (4'-0\" LU). Intérieur non nommé (vide ou remblai : non indiqué).")
mur(165,-45,231,-45,D(6,"PRÉSUMÉ",note="même trait que le mur gauche du perron coté 6\""),ids(33,28),"Excroissance du perron — mur avant.")
mur(231,-45,231,0,D(6,"PRÉSUMÉ",note="même trait que le mur gauche du perron coté 6\""),ids(28,29,33),"Excroissance du perron — mur droit. Nu ext. x=234 (DÉDUIT 162 + 6'-0\").")
xc0=X(448,1070); M_ch=round(xc0/2,1)
mur(M_ch,132,M_ch,Y(1036),D(round(-xc0,1),"ESTIMÉ",note=NE+" ; aucune cote de la cheminée"),ids(13,14),
    f"Massif de cheminée en saillie à l'extérieur du mur gauche, représenté comme un segment épais (axe y). Face avant y=132 DÉDUIT (4'-0\"+7'-0\"), face arrière y≈{Y(1036)} ESTIMÉ, saillie ≈ {round(-xc0,1)} po ESTIMÉ. Voir elem-SS-CHEM.",
    ind=["massif de maçonnerie de cheminée ; aucune indication écrite"])

# ---------------- OUVERTURES ----------------
O=[]
def ouv(typ,op,mur_id,pos,larg,txt,note,sens=None):
    O.append({"id":f"ouv-SS-{len(O)+1:03d}","type":typ,"operation":op,"mur_id":mur_id,"position":pos,"largeur":larg,
              "hauteur":D(None,"ILLISIBLE",photo=None,note="non indiquée au plan"),"allege":D(None,"ILLISIBLE",photo=None,note="non indiquée au plan"),
              "sens":sens,"texte_original":txt,"note":note})
ouv("fenetre",None,"mur-SS-003",D(295,"DÉDUIT",note="axe x=156 (13'-0\" LU) ; position = 451 − 156"),D(80,"LU",ref=cid[6],note="alternative 6'-3\" (75) — voir cote-SS-006"),"6'-8\"","Fenêtre de sous-sol du mur arrière, dessinée à deux châssis (meneau au centre). Opération non indiquée.")
ouv("fenetre",None,"mur-SS-001",D(377,"DÉDUIT",note="axe x=382 (38'-0\" − 6'-2\" ; = 13'-6\"+6'-0\"+12'-4\") ; position = 382 − 5"),D(75,"LU",ref=cid[32]),"6'-3\"","Fenêtre du mur avant, deux châssis (meneau au centre).")
ouv("fenetre",None,"mur-SS-002",D(303,"DÉDUIT",note="axe y=380−72=308 (6'-0\" LU) ; position = 308 − 5"),D(80,"LU",ref=cid[25],note="alternative 6'-3\" (75)"),"6'-8\"","Fenêtre du mur droit (haute, côté arrière), deux châssis.")
ouv("fenetre",None,"mur-SS-002",D(175,"DÉDUIT",note="axe y=308−128=180 (10'-8\" LU) ; position = 180 − 5"),D(36,"LU",ref=cid[26]),"3'-0\"","Fenêtre du mur droit (basse).")
ouv("porte",None,"mur-SS-002",D(70,"DÉDUIT",note="axe y=75 (6'-3\" LU depuis nu ext. avant ; = 180 − 8'-9\") ; position = 75 − 5"),D(32,"LU",ref=cid[50]),"PORTE 2'-8\"","Porte dans le mur de fondation droit, dessinée comme un rectangle barré d'un X dans l'épaisseur du mur ; aucun arc d'ouverture dessiné → opération et sens inconnus. Symbole « 3W » + petit symbole (interrupteur ?) à côté, côté intérieur.",sens=None)
ouv("fenetre",None,"mur-SS-004",D(195,"DÉDUIT",note="axe y=380−200=180 (16'-8\" LU) ; position depuis (5,375) = 375 − 180"),D(36,"LU",ref=cid[16]),"3'-0\"","Fenêtre du mur gauche (haute, près de la fournaise).")
ouv("fenetre",None,"mur-SS-004",D(327,"DÉDUIT",note="axe y=48 (4'-0\" LU) ; position = 375 − 48"),D(36,"LU",ref=cid[17]),"3'-0\"","Fenêtre du mur gauche (basse, au-dessus de l'évier à lessive).")
ouv("porte",None,"mur-SS-003",D(190,"DÉDUIT",note="axe x=261 = 219 (18'-3\") + 42 (3'-6\", point de départ douteux) ; position = 451 − 261 ; ESTIMÉ en image x≈258 ; alternative axe x=271 si le 3'-6\" part du nu int. (ép. 10\" ESTIMÉE)"),D(30,"LU",ref=cid[49]),"PORTE 2'-6\"","Porte entre le sous-sol et le caveau à légumes, dans le mur arrière ; rectangle barré d'un X ; aucun arc d'ouverture identifiable (la courbe sous l'étiquette est un renvoi de texte) → sens inconnu. Symbole d'interrupteur « $ » à gauche, côté sous-sol ; petit symbole non identifié (« Ꭿ » surmonté de « 3/ ») dans l'ouverture.",sens=None)

# ---------------- PIECES ----------------
P=[{"id":"piece-SS-PRINC","nom":"Sous-sol — espace principal (non nommé au plan)","nom_original":None,
    "polygone":[[10,10],[446,10],[446,370],[10,370]],
    "superficie":D(round(436*360/144,1),"DÉDUIT",photo=None,note="436 × 360 po (nu int., cotes 38'-0\", 31'-8\", murs 10\") ; escalier, colonnes et appareils non déduits"),
    "hauteur_plafond":D(None,"ILLISIBLE",photo=None,note="aucune hauteur écrite"),
    "dimensions":{"x":D(436,"DÉDUIT",note="38'-0\" − 2×10\""),"y":D(360,"DÉDUIT",note="13'-10\"+3'-11\"+12'-3\"")},
    "note":"Aucune cloison intérieure dessinée : espace unique contenant fournaise, chauffe-eau, évier à lessive, réservoir à l'huile, escalier."},
   {"id":"piece-SS-LEG","nom":"Caveau à légumes","nom_original":"LEGUMES",
    "polygone":[[229,380],[317,380],[317,430],[229,430]],
    "superficie":D(round(88*50/144,1),"DÉDUIT",photo=None,note="88 × 50 po : 9'-0\" − 10\" (LU) − 10\" (ESTIMÉ) ; 5'-0\" − 10\" (ESTIMÉ) ; dépend d'épaisseurs estimées"),
    "hauteur_plafond":D(None,"ILLISIBLE",photo=None,note="aucune hauteur écrite"),
    "dimensions":{"x":D(88,"DÉDUIT",note="dépend de l'ép. ESTIMÉE du mur gauche du caveau"),"y":D(50,"DÉDUIT",note="dépend de l'ép. ESTIMÉE du mur du fond")},
    "note":"Hors du rectangle principal, derrière le mur arrière ; accès par ouv-SS-008 ; évent grillagé dans le mur gauche ; un luminaire (⊕) dessiné."}]

# ---------------- ELEMENTS ----------------
EL=[]
def el(i,typ,nom,no,pos,dims,txt,note,extra=None):
    e={"id":i,"type":typ,"nom":nom,"nom_original":no,"position":pos,"dimensions":dims,"texte_original":txt,"note":note}
    if extra: e.update(extra); 
    EL.append(e)
def box(x0,y0,x1,y1):
    a,b=E(x0,y1),E(x1,y0)  # (gauche,avant) (droite,arrière)
    cx,cy=round((a[0]+b[0])/2,1),round((a[1]+b[1])/2,1)
    return {"x":cx,"y":cy,"rotation_deg":0},{"longueur":D(round(b[0]-a[0],1),"ESTIMÉ",note=NE+" (sens x)"),"largeur":D(round(b[1]-a[1],1),"ESTIMÉ",note=NE+" (sens y)")}
p,d=box(1370,496,1485,870)
el("elem-SS-ESC","escalier","Escalier vers le rez-de-chaussée",None,p,d,"14 C.M. / RAMPE / 3W",
   "Volée droite dans la travée arrière, pied (côté rue) contre l'axe de la poutre arrière, haut à ≈3 pi du mur arrière (ESTIMÉ). 13 girons dessinés (cohérent avec 14 contremarches). Aucune marche dansante dessinée. Largeur non cotée. RAMPE : ligne tiretée du côté gauche (−x) de l'escalier. « 3W » écrit près du haut, côté gauche : interprété comme interrupteur 3 voies (3-way) — même mention près de la porte 2'-8\" — et non comme 3 marches dansantes (girons tous parallèles). Texte retourné au pied de l'escalier lu « E 14 » / « W ‡ » (illisible, probablement interrupteur 3 voies du bas).",
   {"escalier":{"nb_contremarches":D(14,"LU",ref=None,note="« 14 C.M. » = 14 contremarches"),"fleche":"MONTE","direction":"+y",
                "texte_original":"14 C.M.","note":"flèche dessinée vers l'arrière (+y) sans le mot MONTE ; sens montant présumé (accès au RDC)",
                "largeur":D(p and d["longueur"]["valeur"],"ESTIMÉ",note="non cotée ; "+NE),"rampe":{"texte_original":"RAMPE","cote":"gauche (−x)"},
                "nb_girons_dessines":13}})
p,d=box(690,890,795,1018)
el("elem-SS-FOUR","fournaise","Fournaise","FOURNAISE",p,d,"FOURNAISE","Rectangle entre les deux poutres, près du mur gauche. Tracés tiretés la reliant à la cheminée (voir elem-SS-TUYAU).")
cx,cy=E(590,1186); 
el("elem-SS-CE","chauffe-eau","Chauffe-eau","EAU CHAUDE",{"x":cx,"y":cy,"rotation_deg":0},{"longueur":D(round(72/3.2,1),"ESTIMÉ",note="diamètre du cercle dessiné ; "+NE),"largeur":D(round(72/3.2,1),"ESTIMÉ",note="cercle")},"EAU CHAUDE","Cercle contre le mur gauche, devant (côté rue) la cheminée.")
p,d=box(536,1300,608,1442)
el("elem-SS-EVIER","bac-lavage","Évier à lessive","EVIER À LESSIVE",p,d,"EVIER À LESSIVE","Contre le mur gauche, sous la fenêtre basse ouv-SS-007.")
p,d=box(695,1432,932,1497)
el("elem-SS-HUILE","reservoir-huile","Réservoir à l'huile","RESERVOIR À L'HUILE",p,d,"RESERVOIR À L'HUILE","Rectangle contre le mur avant, à gauche de l'excroissance du perron.")
xa,xb=X(448,1070),0
el("elem-SS-CHEM","cheminee","Cheminée (base, avec conduit)",None,{"x":round(xa/2,1),"y":round((132+Y(1036))/2,1),"rotation_deg":0},
   {"longueur":D(round(-xa,1),"ESTIMÉ",note="saillie hors du nu ext. du mur gauche ; "+NE),"largeur":D(round(Y(1036)-132,1),"ESTIMÉ",note="sens y ; face avant y=132 DÉDUIT")},None,
   f"Massif en saillie hors du mur gauche (mur-SS-011), conduit rectangulaire dessiné à l'intérieur (≈ x {X(470,1070)} à {X(494,1070)}, y {Y(1090)} à {Y(1052)}, ESTIMÉ). Semelle tiretée autour. Aucun texte « CHEMINÉE » ; identifié par la porte de ramonage et la virole.")
el("elem-SS-RAMO","trappe","Porte de ramonage","PORTE DE RAMONAGE",{"x":E(546,1060)[0],"y":E(546,1060)[1],"rotation_deg":0},None,"PORTE DE RAMONAGE","Flèche vers la jonction cheminée / mur gauche, face intérieure. Position ESTIMÉE (pointe de flèche).")
el("elem-SS-VIROLE","autre","Virole (raccord du tuyau à fumée dans la cheminée)","VÉROLE",{"x":E(560,1080)[0],"y":E(560,1080)[1],"rotation_deg":0},None,"VÉROLE",
   "Lu « VÉROLE » ; interprété comme « virole » (bague de raccordement du tuyau de fumée). Alternative de lecture : « VÉNOLE ». Flèche vers la cheminée.")
el("elem-SS-TUYAU","autre","Tuyau à fumée (interprétation)",None,{"x":E(650,1060)[0],"y":E(650,1060)[1],"rotation_deg":0},None,None,
   f"Doubles tracés tiretés allant de la cheminée vers la droite (jusqu'à x≈{X(738,1065)}) puis vers le haut jusqu'au bas de la fournaise (y≈{Y(1018)}). Non légendé ; interprété comme tuyau à fumée / conduit. ESTIMÉ.")
el("elem-SS-EVENT","event","Évent grillagé (caveau)","EVENT GRILLAGÉ",{"x":224,"y":Y(282),"rotation_deg":90},
   {"longueur":D(round(Y(263)-Y(300),1)*-1 if Y(263)<Y(300) else round(Y(263)-Y(300),1),"ESTIMÉ",note="dimension le long du mur ; "+NE),"largeur":D(10,"ESTIMÉ",note="épaisseur du mur")},"EVENT GRILLAGÉ","Dans le mur gauche du caveau (mur-SS-005).",{"mur_id":"mur-SS-005"})
rx,ry=E(1692,330)
el("elem-SS-ROB1","robinet-exterieur","Robinet d'arrosage (arrière)","ROBINET D'ARROSAGE",{"x":rx,"y":380,"rotation_deg":0},None,"ROBINET D'ARROSAGE",f"Symbole sur le nu ext. du mur arrière, à droite du caveau ; x ESTIMÉ ({rx}).",{"mur_id":"mur-SS-003"})
rx,ry=E(1530,1550)
el("elem-SS-ROB2","robinet-exterieur","Robinet (avant)","ROBINET",{"x":rx,"y":0,"rotation_deg":0},None,"ROBINET",f"Symbole sur le nu ext. du mur avant, à droite du perron ; x ESTIMÉ ({rx}).",{"mur_id":"mur-SS-001"})
# symboles électriques
lum=[(1370,247,"caveau"),(948,617,"travée arrière gauche"),(1683,606,"travée arrière droite"),(1371,948,"entre les poutres, près du pied de l'escalier"),(938,1228,"travée avant gauche"),(1648,1236,"travée avant droite")]
for k,(px,py,w) in enumerate(lum,1):
    x,y=E(px,py)
    el(f"elem-SS-LUM{k}","autre","Sortie d'éclairage au plafond (symbole ⊕, interprétation)",None,{"x":x,"y":y,"rotation_deg":0},None,None,f"Cercle barré ⊕ — {w}. Pas de légende ; reliée par arcs tiretés (filage) à des interrupteurs. ESTIMÉ.")
sym=[("elem-SS-INT1","Interrupteur « $ » près de la porte du caveau",1263,393,"$"),("elem-SS-INT2","Interrupteur « $ » sur la colonne avant gauche",932,985,"$"),
     ("elem-SS-INT3","Interrupteur 3 voies probable, porte 2'-8\"",1877,1220,"3W"),("elem-SS-PRI1","Symbole sur la colonne arrière gauche (prise ? interprétation)",935,905,None),
     ("elem-SS-PRI2","Symbole sur la colonne avant droite (prise ? interprétation)",1517,1000,None),("elem-SS-PRI3","Symbole « Θ » à droite de la colonne avant droite (interprétation : prise/sortie)",1562,1015,None)]
for i,n,px,py,t in sym:
    x,y=E(px,py)
    el(i,"autre",n,None,{"x":x,"y":y,"rotation_deg":0},None,t,"Symbole électrique sans légende ; interprétation à valider. ESTIMÉ.")
ABS=["drain de plancher : non dessiné","panneau électrique : non dessiné","laveuse / sécheuse : non dessinées","toilette / douche : non dessinées","cloisons intérieures : aucune dessinée","perron lui-même (dalle, marches) : non dessiné sur cette feuille, seule l'excroissance de fondation"]

# ---------------- STRUCTURE ----------------
S=[]
S.append({"id":"str-SS-P01","type":"poutre","dimension":{"texte_original":"POUTRE 8\"x10\"","valeur":"8x10","source":"LU","photo":"P1"},"sens":"x",
  "geometrie":{"x1":10,"y1":204,"x2":446,"y2":204},"cotes_liees":ids(46,47,48),
  "note":"Poutre arrière ; axe y=204 DÉDUIT (10 + 12'-3\" + 3'-11\" = 370 − 13'-10\"). Trait unique d'un mur à l'autre ; appuis dans les murs non détaillés. Repose sur str-SS-C01 à C03. Matériau non écrit (« COL. BOIS » pour les colonnes seulement)."})
S.append({"id":"str-SS-P02","type":"poutre","dimension":{"texte_original":"POUTRE 8\"x10\"","valeur":"8x10","source":"LU","photo":"P1"},"sens":"x",
  "geometrie":{"x1":10,"y1":157,"x2":446,"y2":157},"cotes_liees":ids(47,48),
  "note":"Poutre avant ; axe y=157 DÉDUIT (10 + 12'-3\"). Repose sur str-SS-C04 à C06."})
cols=[(132,204,"DÉDUIT","x : 10 + 9'-10\" + 4 (chaîne des poutres)"),(228,204,"DÉDUIT","x : 136 + 7'-4\" + 8 + 4 ; = milieu de 456"),(324,204,"DÉDUIT","x : 232 + 7'-4\" + 4 ; = 456 − 10 − 9'-10\" − 4"),
      (132,157,"ESTIMÉ","x non coté pour la rangée avant : alignée au dessin sur C01"),(228,157,"ESTIMÉ","alignée au dessin sur C02"),(324,157,"ESTIMÉ","alignée au dessin sur C03")]
for k,(x,y,src,n) in enumerate(cols,1):
    S.append({"id":f"str-SS-C{k:02d}","type":"colonne","dimension":{"texte_original":"COL. BOIS, 8\"x8\"","valeur":"8x8","source":"LU","photo":"P1"},"sens":None,
      "geometrie":{"x":x,"y":y,"largeur":8,"profondeur":8},"position_source":src,"cotes_liees":ids(37,38,39,40,41,42,43,44,45) if k<=3 else ids(47,48),
      "note":f"Colonne de bois 8\"x8\" (une seule étiquette pour toutes). {n}. Dessinée : carré hachuré dans un carré plus grand (≈14 po ESTIMÉ, probablement base/semelle de colonne — non écrit)."})
S.append({"id":"str-SS-S01","type":"solives","dimension":{"texte_original":"SOLIVES 2\"x10\" @ 20\" c/c","valeur":"2x10 @ 20 c/c","source":"LU","photo":"P1"},"sens":"y",
  "geometrie":{"x1":10,"y1":10,"x2":446,"y2":370},"espacement":D(20,"LU",ref=cid[51]),"cotes_liees":ids(51),
  "note":"Note et flèche à deux pointes dessinées dans la travée arrière gauche (entre mur arrière et poutre str-SS-P01) : solives parallèles à y, appuyées sur les murs avant/arrière et les poutres. Même solivage PRÉSUMÉ dans les autres travées (non répété au plan)."})
S.append({"id":"str-SS-S02","type":"solives","sous_type":"solives doubles","dimension":{"texte_original":"SOLIVES DOUBLES SOUS LES CLOISONS PARALLÈLES","valeur":None,"source":"LU","photo":"P1"},"sens":"y",
  "geometrie":{"x1":X(951,600),"y1":204,"x2":X(951,600),"y2":370},
  "note":"Note générale sans renvoi précis. Un double trait vertical est dessiné à x≈"+str(X(951,600))+" (ESTIMÉ, ≈ axe de la colonne C01) du mur arrière à la poutre arrière — interprété comme solives doubles sous une cloison du RDC. Position des cloisons à confirmer avec la feuille RDC."})
for k,(py,pxe) in enumerate([(537,1008),(707,1012),(1262,1109)],1):
    S.append({"id":f"str-SS-X{k:02d}","type":"solives","sous_type":"croix de Saint-André (entretoisement)","dimension":{"texte_original":"CROIX ST ANDRÉ" if k>1 else "CROIX STANDRÉ","valeur":None,"source":"LU","photo":"P1"},"sens":"x",
      "geometrie":{"x1":10,"y1":Y(py),"x2":X(pxe,py),"y2":Y(py)},
      "note":"Rangée d'entretoises en croix, perpendiculaire aux solives ; y ESTIMÉ ("+NE+"). Trait dessiné seulement dans la moitié gauche (jusqu'à x≈"+str(X(pxe,py))+") ; présence dans la moitié droite non indiquée."+(" Rangées 1-2 ≈ aux tiers de la portée arrière (166 po)." if k<3 else " Rangée ≈ mi-portée de la travée avant (147 po).")})
S.append({"id":"str-SS-F01","type":"semelle","dimension":{"texte_original":"22\"","valeur":"22 (largeur)","source":"LU","photo":"P1"},"sens":None,"geometrie":{"x1":0,"y1":0,"x2":456,"y2":380},"cotes_liees":ids(18),
  "note":"Semelle tiretée sous le périmètre principal, largeur 22\" cotée au mur gauche ; présumée identique ailleurs. Épaisseur non indiquée. Débord ext./int. non coté (≈6 po ext. au dessin)."})
S.append({"id":"str-SS-F02","type":"semelle","dimension":{"texte_original":"22\"","valeur":"22 (largeur)","source":"LU","photo":"P1"},"sens":None,"geometrie":{"x1":219,"y1":380,"x2":327,"y2":440},"cotes_liees":ids(8),"note":"Semelle sous les murs du caveau, 22\" cotée au mur droit."})
S.append({"id":"str-SS-F03","type":"semelle","dimension":{"texte_original":"18\"","valeur":"18 (largeur)","source":"LU","photo":"P1"},"sens":None,"geometrie":{"x1":162,"y1":-48,"x2":234,"y2":0},"cotes_liees":ids(35),"note":"Semelle sous les murs de 6\" de l'excroissance du perron, 18\" cotée au mur gauche."})

# ---------------- NOTES ----------------
N=[]
def note(t,i,px,photo="P1"):
    N.append({"id":f"note-SS-{len(N)+1:02d}","texte_original":t,"interpretation":i,"photo":photo,"px":px})
note("O FONDATIONS & SOUS-SOL O","Titre de la feuille : Fondations et sous-sol.",[2310,1697])
note("ECHELLE: 1/4\" = 1'-0\"","Échelle 1/4 po = 1 pi (1:48). Dessin non fidèle à l'échelle : les cotes écrites priment.",[2330,1762])
note("SOLIVES 2\"x10\" @ 20\" c/c","Solives de plancher du RDC en 2×10 espacées de 20 po centre à centre, portant dans le sens y (flèche).",[1170,650])
note("SOLIVES DOUBLES SOUS LES CLOISONS PARALLÈLES","Doubler les solives sous les cloisons du RDC parallèles aux solives.",[1086,1110])
note("CROIX STANDRÉ / CROIX ST ANDRÉ (3 fois)","Entretoises en croix de Saint-André entre solives (3 rangées, moitié gauche).",[795,527])
note("POUTRE 8\"x10\" (2 fois)","Deux poutres maîtresses de 8×10 po, sens x.",[1087,867])
note("COL. BOIS, 8\"x8\"","Colonnes de bois 8×8 po sous les poutres.",[1110,940])
note("FOURNAISE","Fournaise (appareil de chauffage central).",[749,955])
note("EAU CHAUDE","Chauffe-eau.",[590,1186])
note("EVIER À LESSIVE","Évier (bac) à lessive.",[572,1371])
note("RESERVOIR À L'HUILE","Réservoir à mazout.",[835,1460])
note("PORTE DE RAMONAGE","Porte de ramonage de la cheminée.",[900,1158])
note("VÉROLE","Probablement « virole » : raccord du tuyau de fumée dans la cheminée (lecture incertaine ; alt. « VÉNOLE »).",[770,1186])
note("EVENT GRILLAGÉ","Évent grillagé (ventilation du caveau), mur gauche du caveau.",[1040,245])
note("LEGUMES","Caveau à légumes (chambre froide).",[1385,290])
note("ROBINET D'ARROSAGE","Robinet extérieur d'arrosage, mur arrière.",[1800,310])
note("ROBINET","Robinet extérieur, mur avant.",[1470,1550])
note("PORTE 2'-6\"","Porte de 30 po vers le caveau.",[1408,380])
note("PORTE 2'-8\"","Porte de 32 po dans le mur de fondation droit.",[1795,1281])
note("14 C.M.","14 contremarches (escalier).",[1435,757])
note("RAMPE","Main courante, côté gauche de l'escalier.",[1432,682])
note("3W (dans l'escalier, près du haut)","Probablement interrupteur 3 voies (« 3-way »). Alternative évoquée : 3 marches dansantes — non soutenue par le dessin (girons parallèles).",[1392,640])
note("3W (près de la porte 2'-8\", avec petit symbole)","Probablement interrupteur 3 voies, relié par un tireté au luminaire près du pied de l'escalier.",[1852,1212])
note("« E 14 » / « W ‡ » (texte retourné au pied de l'escalier)","ILLISIBLE ; peut-être un autre « 3W » (interrupteur du bas de l'escalier).",[1435,848])
note("« $ », « ⊕ », « Θ » (symboles sans légende)","Symboles électriques : $ = interrupteur, ⊕ = sortie d'éclairage au plafond, Θ / demi-cercles sur colonnes = prises probables ; arcs tiretés = filage. Interprétation.",[1060,735])
note("marques à peine visibles dans le coin supérieur gauche de la feuille","ILLISIBLE (peut-être un numéro de feuille ou une date).",[60,95])

# ---------------- OBSERVATIONS ----------------
OBS=[
 "Sommes vérifiées par code : arrière 18'-3\"+9'-0\"+10'-9\" = 38'-0\" ✓ ; avant 13'-6\"+6'-0\"+12'-4\"+6'-2\" = 38'-0\" ✓ ; gauche 16'-8\"+4'-0\"+7'-0\"+4'-0\" = 31'-8\" ✓ ; droite 6'-0\"+10'-8\"+8'-9\"+6'-3\" = 31'-8\" ✓ ; intérieur x 10+9'-10\"+8+7'-4\"+8+7'-4\"+8+9'-10\"+10 = 38'-0\" ✓ ; intérieur y 10+13'-10\"+3'-11\"+12'-3\"+10 = 31'-8\" ✓. Ces sommes ne tiennent qu'avec les lectures 7'-0\" (et non 1'-0\"), 9'-10\" (et non 3'-10\"), 8'-9\" (et non 8'-5\"), 13'-10\" (et non 15'-10\").",
 "Fenêtres arrière (cote-SS-006) et droite haute (cote-SS-025) lues « 6'-8\" » (8 fermé), mais dessinées de la même longueur que la fenêtre avant cotée 6'-3\" (≈72–74 po à l'échelle locale). Confusion 3/8 possible ; aucune chaîne fermée ne permet de trancher.",
 "Cote 3'-6\" du caveau (cote-SS-010) : point de départ non dessiné (nu int. ou ext. du mur gauche du caveau) ; la position de la porte 2'-6\" (ouv-SS-008) en dépend (axe x=261 retenu provisoirement — nu ext., plus proche de l'image ≈258 —, alt. 271 si nu int., qui dépendrait en plus de l'épaisseur ESTIMÉE 10\" du mur gauche du caveau).",
 "Épaisseurs non écrites : mur gauche et mur du fond du caveau (ESTIMÉ 10\"), mur arrière principal (DÉDUIT 10\"), murs avant/droit du perron (PRÉSUMÉ 6\").",
 "Cheminée : aucune cote (saillie et profondeur ESTIMÉES ≈ 20 × 21 po) ; seule sa face avant est cotée (y=132).",
 "Escalier : largeur non cotée (≈37 po ESTIMÉ) ; mot MONTE absent (flèche seule) ; 13 girons dessinés pour 14 C.M. (cohérent). Pied de l'escalier au droit de la poutre arrière (y≈204) : vérifier l'échappée sous la poutre sur place.",
 "Colonnes de la rangée avant (C04–C06) : x non coté, alignement visuel seulement.",
 "Croix de Saint-André dessinées seulement dans la moitié gauche ; aucune dans la travée entre poutres.",
 "Portes 2'-6\" et 2'-8\" : aucun arc d'ouverture → sens et type de battant inconnus. La porte 2'-8\" est dans un mur de fondation extérieur (accès extérieur latéral ?) — à confirmer avec la feuille RDC.",
 "« 3W » : interprété comme interrupteur 3 voies, pas comme marches dansantes (aucune marche dansante dessinée).",
 "Hauteur de plafond du sous-sol : non écrite sur la feuille.",
 "Photo P1 en légère perspective (bord ext. gauche passe de x≈541 px en haut à ≈481 px en bas) et pli central du papier vers x≈1230 px (colonne C02, cote 8\" centrale) : coordonnées ESTIMÉES corrigées linéairement, précision ±3 po environ.",
 "Le centre de la fenêtre gauche haute (y=180) et celui de la fenêtre droite basse (y=180) coïncident ; la cote 2e « 6'-2\" » (rang 2 avant) est un doublon de la chaîne hors-tout.",
 "P7 est une vue quasi identique de la même feuille (même cadrage) : toutes les cotes douteuses re-vérifiées sur P7, aucune contradiction trouvée.",
 "Éléments non dessinés : "+" ; ".join(ABS)+"."]

niv={"id":"SS","nom":"Sous-sol","feuille":"A-100","photos_sources":["P1","P7"],
     "hauteur_plafond":D(None,"ILLISIBLE",photo=None,note="aucune hauteur de plafond écrite sur la feuille FONDATIONS & SOUS-SOL"),
     "murs":M,"ouvertures":O,"pieces":P,"elements":EL,"structure":S,"cotes":C,"notes":N,"observations":OBS,
     "elements_absents":ABS,
     "calibrage":{"methode":NE,"photo":"P1","fichier":"prep/redresse/P1.jpg"}}
json.dump(niv,open(OUT,"w"),ensure_ascii=False,indent=1)
print(len(M),len(O),len(P),len(EL),len(S),len(C),len(N))
