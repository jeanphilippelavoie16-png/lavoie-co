import sys,re
from lxml import etree
from PIL import ImageFont
from shapely.geometry import box, Polygon, Point
from shapely import affinity
F={False:'/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',True:'/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'}
NS='{http://www.w3.org/2000/svg}'
def bb(el):
    s=''.join(el.itertext()); fs=float(el.get('font-size')); b=el.get('font-weight')=='bold'
    w=ImageFont.truetype(F[b],100).getlength(s)*fs/100
    x=float(el.get('x')); y=float(el.get('y')); a=el.get('text-anchor','start')
    x0={'start':x,'middle':x-w/2,'end':x-w}[a]
    g=box(x0,y-0.72*fs,x0+w,y+0.2*fs)
    tr=el.get('transform')
    if tr:
        m=re.match(r'rotate\(([-\d.]+) ([-\d.]+) ([-\d.]+)\)',tr); g=affinity.rotate(g,float(m.group(1)),origin=(float(m.group(2)),float(m.group(3))))
    return s,g
def poly(d):
    nums=[float(v) for v in re.findall(r'-?\d+\.?\d*',d)]
    return Polygon(list(zip(nums[0::2],nums[1::2])))
for f in sys.argv[1:]:
    t=etree.parse(f); P={}
    for g in t.iter(NS+'g'):
        if (g.get('id') or '').startswith('piece-'):
            p=g.find(NS+'path'); P[g.get('id')]=(g,poly(p.get('d')))
    print(f)
    for pid,(g,pl) in P.items():
        texts=[bb(e) for e in g.findall(NS+'text')]
        dot=g.find(NS+'circle'); 
        dotin=None
        if dot is not None: dotin=pl.buffer(0.01).contains(Point(float(dot.get('cx')),float(dot.get('cy'))))
        for s,b in texts[:1]:
            inside_own=b.intersection(pl).area/b.area
            others=[(q,round(b.intersection(ql).area/b.area,2)) for q,(gg,ql) in P.items() if q!=pid and b.intersection(ql).area/b.area>0.2]
            flag='' if inside_own>0.8 or (dotin and not others) else '  <<< '
            print(f'  {pid:16s} "{s}" dans sa pièce {inside_own:.0%} renvoi={dotin} ; texte dans autre pièce: {others}{flag}')
