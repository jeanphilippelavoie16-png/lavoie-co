import json,sys,os
from PIL import Image, ImageDraw, ImageFont
J=os.environ.get('QCJ','/tmp/claude-0/-home-user-lavoie-co/a2f554a7-a4f7-5946-bdd4-2eb9d5a22192/scratchpad/snap/releve/livrables/donnees/maison.json')
R='/home/user/lavoie-co/releve/travail/prep/redresse/'
OUT=os.environ.get('QCOUT','/home/user/lavoie-co/releve/travail/qc/preuves/')
MAP={'P2':'P1','P3':'P7','P4':'P3','P5':'P4','P6':'P6','P1':'P2','P7':'P5'}
d=json.load(open(J))
C={}
for n in d['niveaux']:
    for c in n['cotes']: C[c['id']]=c
ids=sys.argv[2].split(','); name=sys.argv[1]
W,H=360,170; cols=3
rows=(len(ids)+cols-1)//cols
sheet=Image.new('RGB',(cols*W,rows*(H+40)),'white'); dr=ImageDraw.Draw(sheet)
try: f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
except: f=None
cache={}
for i,cid in enumerate(ids):
    c=C[cid]; p=MAP[c['photo']]
    if p not in cache: cache[p]=Image.open(R+p+'.jpg').convert('RGB')
    im=cache[p]; x,y=c['px']
    cr=im.crop((x-W//2*0.75,y-H//2*0.75,x+W//2*0.75,y+H//2*0.75)).resize((W,H))
    X=(i%cols)*W; Y=(i//cols)*(H+40)
    sheet.paste(cr,(X,Y+40))
    dr.text((X+4,Y+2),f"{cid} [{c['photo']}]",fill='black',font=f)
    dr.text((X+4,Y+20),f"JSON: {c['texte_original']} = {c['valeur']}",fill='red',font=f)
sheet.save(OUT+name+'.jpg',quality=85); print(OUT+name+'.jpg',sheet.size)
