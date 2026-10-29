import sys, json
from PIL import Image, ImageDraw
S='/tmp/claude-0/-home-user-lavoie-co/a2f554a7-a4f7-5946-bdd4-2eb9d5a22192/scratchpad'
R='/home/user/lavoie-co/releve/travail/prep/redresse/'
OUT='/home/user/lavoie-co/releve/travail/qc/preuves/'
K=5100/1088
TF={'SS':(220.135,540.979),'RDC':(218.21,538.479)}
SVGPNG={'SS':S+'/A-100_sous-sol.png','RDC':S+'/A-101_rdc.png'}
def svgcrop(niv,x0,y0,x1,y1):
    ox,oy=TF[niv]; im=Image.open(SVGPNG[niv]).convert('RGB')
    box=(int((ox+x0)*K),int((oy-y1)*K),int((ox+x1)*K),int((oy-y0)*K))
    return im.crop(box)
def photocrop(p,x0,y0,x1,y1,thumb=True):
    im=Image.open(R+p+'.jpg').convert('RGB')
    f=im.size[0]/1900 if thumb else 1
    return im.crop((int(x0*f),int(y0*f),int(x1*f),int(y1*f)))
def pair(name,a,b,h=900):
    a=a.copy(); b=b.copy()
    a=a.resize((int(a.size[0]*h/a.size[1]),h)); b=b.resize((int(b.size[0]*h/b.size[1]),h))
    W=a.size[0]+b.size[0]+20; im=Image.new('RGB',(W,h),'white'); im.paste(a,(0,0)); im.paste(b,(a.size[0]+20,0))
    im.save(OUT+name+'.jpg',quality=88); print(OUT+name+'.jpg', im.size)
if __name__=='__main__':
    a=json.loads(sys.argv[1])
    pair(a['name'], photocrop(a['p'],*a['pb'],thumb=a.get('thumb',True)), svgcrop(a['niv'],*a['hb']), a.get('h',900))
