import cv2,numpy as np,math,json
g=cv2.imread('/home/user/lavoie-co/releve/travail/prep/redresse/P5.jpg',0).astype(float)
# arrow shaft: darkest x per row, robust fit
pts=[]
for y in range(720,1395,3):
    row=g[y,1380:1700]; x=int(np.argmin(row))
    if row[x]<70: pts.append((1380+x,y))
P=np.array(pts,float)
for it in range(5):
    a,b=np.polyfit(P[:,1],P[:,0],1); r=np.abs(P[:,0]-(a*P[:,1]+b)); P=P[r<3]
a,b=np.polyfit(P[:,1],P[:,0],1)
print('shaft n',len(P),'a',a,'b',b,'ymin',P[:,1].min(),'ymax',P[:,1].max())
# tip: topmost dark pixel near line
tipy=None
for y in range(600,720):
    xe=a*y+b; seg=g[y,int(xe)-6:int(xe)+7]
    if seg.min()<80: tipy=y; break
tail=(a*1392+b,1392.0); tip=(a*tipy+b,float(tipy))
print('tip',tip,'tail',tail)
# facade line: front wall row, darkest y per column x 650..1025 excluding projection 765-842
fp=[]
for x in list(range(650,760,2))+list(range(850,1025,2)):
    col=g[1215:1255,x]; y=int(np.argmin(col)); fp.append((x,1215+y))
F=np.array(fp,float)
for it in range(4):
    c,d=np.polyfit(F[:,0],F[:,1],1); r=np.abs(F[:,1]-(c*F[:,0]+d)); F=F[r<2.5]
c,d=np.polyfit(F[:,0],F[:,1],1)
print('facade slope',c,'n',len(F))
# rear wall line too
rp=[]
for x in list(range(650,805,2)):
    col=g[890:920,x]; y=int(np.argmin(col)); rp.append((x,890+y))
R=np.array(rp,float); c2,d2=np.polyfit(R[:,0],R[:,1],1); print('rear slope',c2)
# right side wall col x approx 1030; left 643
def side(x0):
    sp=[]
    for y in range(930,1210,3):
        row=g[y,x0-12:x0+12]; sp.append((x0-12+int(np.argmin(row)),y))
    S=np.array(sp,float); e,f=np.polyfit(S[:,1],S[:,0],1); return e
print('left wall dx/dy',side(643),'right wall dx/dy',side(1031))
# image coords: x right, y down. Facade direction vector (left->right): (1,c). "Vers l'arriere" = perpendicular pointing up (toward rear, smaller y): rotate facade dir by -90 deg in image (y down) -> (c,-1)
back=np.array([c,-1.0]); back/=np.linalg.norm(back)
north=np.array([tip[0]-tail[0],tip[1]-tail[1]]); north/=np.linalg.norm(north)
# clockwise angle on screen (y down) from back to north: atan2(cross,dot) with cross = bx*ny - by*nx (positive = clockwise in y-down coords)
cross=back[0]*north[1]-back[1]*north[0]; dot=back@north
ang=math.degrees(math.atan2(cross,dot))
print('angle back->north clockwise deg',ang)
# alt using side walls mean direction
e=(side(643)+side(1031))/2; back2=np.array([-e,-1.0]); back2/=np.linalg.norm(back2)
cross=back2[0]*north[1]-back2[1]*north[0]; print('angle using side walls',math.degrees(math.atan2(cross,back2@north)))
json.dump({'tip':tip,'tail':tail,'facade_slope':c,'rear_slope':c2,'angle':ang},open('nord.json','w'))
