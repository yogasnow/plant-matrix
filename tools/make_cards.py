from PIL import Image,ImageDraw,ImageFont,ImageFilter
from pathlib import Path
import math,random
P=Path(__file__).resolve().parent.parent / "cards"
W,H=1024,1536
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(n,b=False):return ImageFont.truetype(B if b else F,n)
def txt(d,xy,s,size=30,fill='#173f32',bold=False,anchor=None):d.text(xy,s,font=font(size,bold),fill=fill,anchor=anchor)
def linewrap(d,s,width,size,bold=False):
 out=[]; cur=''
 for word in s.split():
  trial=(cur+' '+word).strip()
  if d.textbbox((0,0),trial,font=font(size,bold))[2]>width and cur:out.append(cur);cur=word
  else:cur=trial
 if cur:out.append(cur)
 return out
def para(d,s,x,y,w,size=27,leading=1.36,fill='#25463d',bold=False):
 for row in linewrap(d,s,w,size,bold):txt(d,(x,y),row,size,fill,bold);y+=int(size*leading)
 return y
def rr(d,box,fill,outline='#d9b36a',rad=28,width=3):d.rounded_rectangle(box,radius=rad,fill=fill,outline=outline,width=width)
def star(d,x,y,r=15,col='#f4c558'):
 d.polygon([(x,y-r),(x+r*.25,y-r*.25),(x+r,y),(x+r*.25,y+r*.25),(x,y+r),(x-r*.25,y+r*.25),(x-r,y),(x-r*.25,y-r*.25)],fill=col)
def sprout(d,x,y,k=1):
 d.line((x,y+30*k,x,y+2*k),fill='#3c6d41',width=int(8*k))
 d.ellipse((x-34*k,y-18*k,x+1*k,y+7*k),fill='#5c9a56',outline='#27663e',width=2)
 d.ellipse((x-1*k,y-24*k,x+36*k,y+4*k),fill='#86bb66',outline='#27663e',width=2)
 d.ellipse((x-8*k,y-39*k,x+8*k,y-13*k),fill='#45b7ee',outline='#f7ffff',width=2)
def coin(d,x,y):
 d.ellipse((x-65,y-65,x+65,y+65),fill='#d68e20',outline='#fff2ad',width=5)
 d.ellipse((x-54,y-54,x+54,y+54),fill='#ffda63',outline='#a96d1b',width=4)
 d.polygon([(x,y-39),(x+27,y),(x,y+39),(x-27,y)],fill='#fff2ba',outline='#ae6819')
 d.polygon([(x,y-39),(x+27,y),(x,y)],fill='#fff9d8')
 d.polygon([(x,y),(x+27,y),(x,y+39)],fill='#e8a83b')
def key(d,x,y):
 d.ellipse((x-17,y-45,x+31,y+3),fill='#e4a534',outline='#925b17',width=3)
 d.ellipse((x-6,y-34,x+20,y-8),fill='#fff8df')
 d.line((x+14,y-2,x-29,y+50),fill='#dc9b24',width=17)
 d.line((x-27,y+44,x-8,y+57),fill='#dc9b24',width=12)
def arrow(d,x,y):
 d.line((x-22,y,x+18,y),fill='#6d9e68',width=9)
 d.polygon([(x+26,y),(x+10,y-13),(x+10,y+13)],fill='#6d9e68')
def molecule(d,cx,cy,scale=1):
 pts=[(-130,-50),(-35,-115),(65,-80),(135,25),(30,110),(-100,90)]
 for a,b in [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0),(1,4)]:
  p,q=pts[a],pts[b];d.line((cx+p[0]*scale,cy+p[1]*scale,cx+q[0]*scale,cy+q[1]*scale),fill='#af8bc5',width=int(13*scale))
 colors=['#34a6d8','#e18877','#8359b6','#e4aa54','#43a67e','#e98bb5']
 for (px,py),co in zip(pts,colors):
  r=28*scale;d.ellipse((cx+px*scale-r,cy+py*scale-r,cx+px*scale+r,cy+py*scale+r),fill=co,outline='#fff9f3',width=4)
def cell(d,cx,cy,r=215,detail=True):
 d.ellipse((cx-r,cy-r,cx+r,cy+r),fill='#bde9f6',outline='#4a83ad',width=13)
 d.ellipse((cx-r+17,cy-r+17,cx+r-17,cy+r-17),outline='#f8ffff',width=7)
 d.ellipse((cx-85,cy-90,cx+90,cy+85),fill='#a476d4',outline='#713ca6',width=9)
 d.ellipse((cx-28,cy-34,cx+37,cy+31),fill='#eab7f5',outline='#8044ad',width=5)
 if detail:
  for ox,oy in [(-105,100),(105,-80),(130,100)]:
   d.ellipse((cx+ox-42,cy+oy-24,cx+ox+42,cy+oy+24),fill='#f3a14e',outline='#a7552c',width=5)
   d.arc((cx+ox-28,cy+oy-15,cx+ox+28,cy+oy+15),0,300,fill='#ffdc84',width=5)
  for ox,oy in [(-130,-15),(-40,140),(65,130),(110,-140)]:d.ellipse((cx+ox-10,cy+oy-10,cx+ox+10,cy+oy+10),fill='#d45a96')
def draw_figure(d,kind):
 if kind=='atom':
  cx,cy=512,603
  for a in [-35,35,90]:d.ellipse((cx-245,cy-90,cx+245,cy+90),outline='#62a9cb',width=8) if a==90 else None
  for a in [-55,55]:
   pts=[]
   for t in range(361):
    q=t*math.pi/180;xx=230*math.cos(q);yy=90*math.sin(q);rad=a*math.pi/180;pts.append((cx+xx*math.cos(rad)-yy*math.sin(rad),cy+xx*math.sin(rad)+yy*math.cos(rad)))
   d.line(pts,fill='#68a5c7',width=7)
  d.ellipse((cx-72,cy-72,cx+72,cy+72),fill='#8f65bc',outline='#e9c9ff',width=7)
  for x,y in [(280,600),(750,600),(490,385)]:d.ellipse((x-18,y-18,x+18,y+18),fill='#f6bb55',outline='white',width=4)
  txt(d,(512,860),'ЯДРО: ПРОТОНЫ И НЕЙТРОНЫ',30,anchor='mm',bold=True)
  txt(d,(512,906),'ЭЛЕКТРОНЫ — ВОКРУГ ЯДРА',29,anchor='mm')
 elif kind=='molecule':
  molecule(d,512,600,1.35)
  txt(d,(512,875),'АТОМЫ СОЕДИНЯЮТСЯ СВЯЗЯМИ',30,anchor='mm',bold=True)
  txt(d,(512,925),'Пример: вода H₂O = 2H + O',31,anchor='mm')
 elif kind=='cell':
  cell(d,512,620,245)
  txt(d,(512,900),'МЕМБРАНА • ЦИТОПЛАЗМА • ЯДРО',29,anchor='mm',bold=True)
 elif kind=='tissue':
  for row in range(3):
   for col in range(4):
    x=270+col*160+(row%2)*32;y=460+row*150
    d.ellipse((x-68,y-60,x+68,y+60),fill='#a9dae2',outline='#548a9c',width=7)
    d.ellipse((x-23,y-24,x+23,y+24),fill='#9167bd')
  txt(d,(512,900),'МНОГО КЛЕТОК + МЕЖКЛЕТОЧНАЯ СРЕДА',26,anchor='mm',bold=True)
 elif kind=='membrane':
  for row,y in enumerate([520,655]):
   for x in range(135,900,52):
    d.ellipse((x-17,y-17,x+17,y+17),fill='#63b3da',outline='#326e99',width=3)
    if row==0:d.line((x-7,y+18,x-7,y+100),fill='#eab856',width=7);d.line((x+7,y+18,x+7,y+100),fill='#eab856',width=7)
  rr(d,(452,480,574,714),'#945cbd','#59398d',35,5)
  rr(d,(487,496,539,697),'#dff3ff','#7142a4',20,2)
  d.ellipse((475,400,550,475),fill='#f5ae56',outline='#a76331',width=4)
  arrow(d,512,770)
  txt(d,(512,865),'БЕЛОК-ПЕРЕНОСЧИК',32,anchor='mm',bold=True)
  txt(d,(512,915),'помогает глюкозе пересечь мембрану',27,anchor='mm')
 elif kind=='structure':
  cell(d,512,630,245)
  for x,y,label in [(265,425,'мембрана'),(735,460,'ядро'),(775,740,'митохондрия'),(270,775,'цитоплазма')]:
   rr(d,(x-115,y-27,x+115,y+27),'#fffdf4','#98b681',15,2);txt(d,(x,y),label,20,anchor='mm',bold=True)
 elif kind=='ribosome':
  d.ellipse((160,465,430,735),fill='#ab7bd2',outline='#70459c',width=8)
  d.ellipse((240,550,350,660),fill='#dcb0ef',outline='#70459c',width=5)
  txt(d,(295,765),'ЯДРО',26,anchor='mm',bold=True)
  for i in range(8):
   x=410+i*53;y=610+int(24*math.sin(i*.7))
   d.line((x,y,x+44,y),fill='#f2ab51',width=10)
   d.ellipse((x+10,y-10,x+28,y+8),fill=['#d25991','#57a7cb','#8d74bb'][i%3])
  d.ellipse((605,563,799,660),fill='#d6a3df',outline='#70459c',width=6)
  d.ellipse((630,652,774,717),fill='#995dc1',outline='#70459c',width=5)
  txt(d,(702,765),'РИБОСОМА',25,anchor='mm',bold=True)
  txt(d,(512,865),'РНК НЕСЁТ ИНСТРУКЦИЮ',28,anchor='mm',bold=True)
  txt(d,(512,915),'РИБОСОМА СОБИРАЕТ БЕЛОК',28,anchor='mm')
 elif kind=='dna':
  cell(d,512,600,230,False)
  for i in range(7):
   y=540+i*20;x1=485+35*math.sin(i*.65);x2=540-35*math.sin(i*.65)
   d.line((x1,y,x2,y),fill='#f7c36b',width=6)
   d.ellipse((x1-7,y-7,x1+7,y+7),fill='#258fd3')
   d.ellipse((x2-7,y-7,x2+7,y+7),fill='#d85ea3')
  txt(d,(512,875),'ДНК УПАКОВАНА В ХРОМАТИН',28,anchor='mm',bold=True)
  txt(d,(512,923),'ГЕН — УЧАСТОК ДНК',30,anchor='mm')
cards=[
 ('01-atom','atom','АТОМ','Из чего состоит вещество','Элемент → атом → частицы','Узнай протоны, нейтроны и электроны. Различи атомы углерода, кислорода, водорода и азота.','Атом и клетка — одно и то же?','Нет. Клетка состоит из множества молекул и атомов.'),
 ('02-molecule','molecule','МОЛЕКУЛА','Атомы объединяются','Атомы → химическая связь → молекула','Сравни воду, глюкозу и аминокислоту. Их строение и функции различаются.','Из атомов могут образоваться молекулы?','Да. Например, вода состоит из водорода и кислорода.'),
 ('03-cell','cell','КЛЕТКА','Живая система','Молекулы → структуры → процессы жизни','Найди границу клетки и её внутреннюю среду. Клетка обменивается веществами, использует энергию и хранит информацию.','Клетка — это просто одна молекула?','Нет. Это организованная система из множества молекул.'),
 ('04-tissue','tissue','ТКАНЬ','Клетки работают вместе','Клетки + межклеточная среда → ткань','Узнай четыре основные группы тканей животных: эпителиальная, соединительная, мышечная, нервная.','Ткань состоит только из клеток?','Нет. В ней есть и межклеточная среда.'),
 ('05-membrane','membrane','МЕМБРАНА','Граница и обмен','Липидный бислой + белки → избирательный обмен','Различи свободный проход небольших молекул и перенос через белки. Рецепторы принимают сигналы.','Глюкоза входит в мышечную клетку через ядро?','Нет. Ей помогают белки-переносчики в мембране.'),
 ('06-structure','structure','СТРОЕНИЕ КЛЕТКИ','Знакомимся с частями','Мембрана → цитоплазма → органеллы','Найди ядро, рибосомы, митохондрии и лизосомы. Каждая структура выполняет свои задачи.','Где находится большинство органелл?','В цитоплазме, внутри мембраны клетки.'),
 ('07-nucleus-dna','dna','ЯДРО И ДНК','Где хранится информация','Ядро → ДНК → ген → РНК → белок*','Большая часть ДНК человека находится в ядре, немного — в митохондриях. Не каждый ген кодирует белок.','Где находится большая часть ДНК клетки?','В ядре. *Белок синтезируется по некоторым РНК.'),
 ('08-rna-ribosome','ribosome','РНК И РИБОСОМА','Как собирается белок','ДНК → РНК → рибосома → белок','РНК создаётся по участку ДНК. Рибосома читает матричную РНК и соединяет аминокислоты в цепь белка.','Рибосома читает ДНК напрямую?','Нет. При синтезе белка она читает матричную РНК.'),
]
for num,kind,title,subtitle,chain,lesson,question,answer in cards:
 im=Image.new('RGB',(W,H));pix=im.load()
 for y in range(H):
  t=y/H; c=(int(238-22*t),int(244-13*t),int(225-17*t))
  for x in range(W):pix[x,y]=c
 d=ImageDraw.Draw(im)
 rr(d,(14,14,1010,1522),'#fff8e9','#a46d2d',50,10)
 rr(d,(28,28,996,1510),'#fffaf0','#efd093',43,5)
 rr(d,(48,45,976,145),'#f8edd4','#d3a559',26,4)
 sprout(d,115,99,.9);sprout(d,905,99,.9)
 txt(d,(512,84),'PLANT MATRIX',46,'#57330f',True,'mm')
 txt(d,(512,128),'ЗНАНИЯ СОЗДАЮТ БОЛЬШОЕ',20,'#7d5528',False,'mm')
 txt(d,(68,177),f'ОСНОВНОЙ ПУТЬ  •  {num[:2]} / 08',23,'#78502c',True)
 txt(d,(68,221),title,56,'#153e32',True)
 txt(d,(70,287),subtitle,30,'#6e4830')
 rr(d,(48,334,976,1023),'#edf9f3','#96b9a5',36,4)
 rr(d,(82,359,942,985),'#e1f4fb','#a2c8de',28,3)
 draw_figure(d,kind)
 rr(d,(48,1043,976,1230),'#f2f7e8','#b5c68a',28,3)
 txt(d,(76,1067),'УЧЕБНАЯ ЦЕПОЧКА',22,'#775326',True)
 para(d,chain,76,1105,860,27,1.24,'#153f37',True)
 para(d,lesson,76,1150,860,22,1.3)
 rr(d,(48,1252,976,1367),'#fffdf5','#d6b467',28,3)
 txt(d,(76,1270),'ПРОВЕРЬ СЕБЯ',24,'#81572c',True)
 para(d,question,76,1310,850,27,1.2,'#193e35',True)
 rr(d,(48,1385,976,1493),'#f8edce','#cb9a44',31,4)
 coin(d,123,1438);key(d,892,1432)
 for x,y in [(810,1413),(953,1407),(953,1472)]:star(d,x,y,14)
 txt(d,(235,1420),'НАГРАДА: РОМБ + КЛЮЧ',24,'#79501c',True)
 txt(d,(235,1456),'Ответ — в подписи к карточке',20,'#7d6b46')
 im.save(P/(num+'.png'),optimize=True)
print('created',len(cards),'cards')
