import json,subprocess,sys,os,numpy as np
from playwright.sync_api import sync_playwright
S=os.path.dirname(os.path.abspath(__file__));SRC=S+'/../voice_clean.wav';FPS=30
CL={
'A1':(30.7,35.3,1,[(0,'مع نوعية شعر بنتي'),(1.6,'الموضوع كان دمار ومرار!')],['before.jpg','after1.jpg']),
'A2':(88.1,96.3,1,[(0,'مش بيلزق الشعر خالص'),(2.2,'وبيسرّح الشعر بسهولة'),(4.2,'بيخلي الشعر طري ومفرود')],['after1.jpg','after2.jpg']),
'B1':(101.8,118.0,2,[(0,'أول مرة في حياتي'),(2.7,'أجرّب شامبو وبلسم'),(4.7,'ويطلعوا بالتحفة دي!'),(7.8,'مفيش شامبو كان ماشي على شعرنا'),(13.1,'أول مرة أجرّب حاجة وتطلع حلوة')],['after1.jpg','P:shampoo','after2.jpg']),
'B2':(123.0,133.0,2,[(0,'بسرّح شعري كل يوم'),(2.0,'ولسه الكريم فيه وريحته فيه'),(5.0,'وناعم حرير ومرطّب')],['after2.jpg','P:cream']),
'B3':(140.5,151.5,2,[(0,'أهم حاجة تحطي الكريم'),(3.6,'ويفضل شعرك رطب طول اليوم'),(6.2,'رطب لتالت يوم!')],['after2.jpg','before.jpg','after1.jpg']),
'C1':(199.3,203.6,3,[(0,'كنت قلقانة وخايفة'),(1.6,'بس لما استخدمتها.. جميلة جداً')],['after2.jpg','P:all']),
'C2':(223.2,231.5,3,[(0,'استخدمت الهير واكس'),(1.8,'رجعت زي ما وديتها الصبح'),(4.7,'ولا شعرة هايشة.. كله نايم')],['after1.jpg','ba2.jpg']),
'D1':(186.8,196.3,3,[(0,'جبت كل الكريمات'),(2.5,'حتى الغالية والمستوردة'),(7.1,'وما جابتش نتيجة!')],['before.jpg','ba3.jpg']),
'D2':(132.9,140.2,2,[(0,'مش محتاجة أحط كريم كل يوم'),(5.6,'ما شاء الله.. بيكفي')],['after2.jpg','P:cream']),
'D3':(75.9,82.4,1,[(0,'بحميها بالشامبو والبلسم'),(3.4,'ريحة تحفة تطلع من الحمام')],['after1.jpg','P:shampoo']),
'D4':(95.9,99.0,1,[(0,'ومش قادرة أقولك على الواكس والفرشة!')],['after1.jpg','P:wax']),
'D5':(15.8,21.0,1,[(0,'شعر بنتي كان معذّبني'),(3.5,'معذّبني بجد')],['before.jpg']),
'D6':(40.4,50.0,1,[(0,'لا كحكة ولا تسريحات'),(6.2,'ولا حتى ديل حصان.. أبداً')],['before.jpg','after1.jpg']),
'H1':(101.8,109.5,2,[(0,'أول مرة في حياتي'),(2.7,'أجرّب شامبو وبلسم'),(4.7,'ويطلعوا بالتحفة دي!')],['after1.jpg','after2.jpg']),
'H2':(109.4,118.0,2,[(0,'مفيش شامبو كان ماشي على شعرنا'),(5.4,'أول مرة أجرّب حاجة وتطلع حلوة')],['after2.jpg','before.jpg']),
}
FULLCAP={1:[(2.6,'السلام عليكم.. إزيك يا حبيبتي'),(5.8,'بعد أسبوعين.. مرتين بس استخدمت حاجات شعر بنتي'),(11.1,'قلت لازم أقولك بجد'),(16.0,'شعر بنتي كان معذّبني'),(21.5,'والمشكلة إنها بتروح الحضانة كل يوم'),(27.8,'والبرفان والتسريحة وكده'),(31.2,'مع نوعية شعر بنتي الموضوع كان دمار ومرار'),(38.4,'مهما تعملي.. شعرها مش بيمشي'),(40.6,'لا كحكة ولا تسريحات'),(46.7,'ولا حتى ديل حصان.. أبداً'),(56.3,'أنا مهتمة جداً بنضافتها'),(61.8,'والشعر الناشف ده بيبقى صعب خالص'),(67.8,'البنت دلوقتي ريحة شعرها جميلة'),(76.2,'بحميها بالشامبو والبلسم'),(79.4,'ريحة تحفة تطلع من الحمام'),(86.5,'ما شاء الله.. ممتاز'),(88.5,'مش بيلزق الشعر خالص'),(90.5,'وبيسرّح الشعر بسهولة'),(92.6,'بيخلي الشعر طري ومفرود'),(96.2,'ومش قادرة أقولك على الواكس والفرشة!')],
2:[(102.0,'أول مرة في حياتي'),(104.7,'أجرّب شامبو وبلسم ويطلعوا بالتحفة دي'),(109.6,'مفيش شامبو كان ماشي على شعرنا'),(114.9,'أول مرة أجرّب حاجة وتطلع حلوة'),(119.0,'غاسلة شعري من 3 أيام'),(123.3,'وبسرّح شعري كل يوم'),(126.1,'ولسه الكريم فيه وريحته فيه'),(129.0,'وناعم حرير ومرطّب'),(133.1,'مش محتاجة أحط كريم كل يوم'),(138.6,'ما شاء الله.. بيكفي'),(140.7,'أهم حاجة تحطي الكريم'),(144.1,'ويفضل شعرك رطب طول اليوم'),(146.7,'رطب لتالت يوم!')],
3:[(178.1,'ربنا يبارك لك.. كل حاجة تحفة'),(183.1,'بأمانة.. مجرّب'),(187.0,'جبت كل الكريمات.. حتى الغالية'),(193.9,'وما جابتش نتيجة'),(199.6,'كنت قلقانة وخايفة'),(201.2,'بس لما استخدمتها.. جميلة جداً'),(206.0,'بنتي استخدمت الكريم'),(208.0,'وشعرها بقى ناعم'),(223.5,'استخدمت الهير واكس'),(225.0,'رجعت زي ما وديتها الصبح'),(228.1,'ولا شعرة هايشة.. كله نايم')]}
def full(k,a,b,v,vis):
  c=[(max(0,x-a),y) for x,y in FULLCAP[v] if a-0.5<=x<b]
  CL[k]=(a,b,v,c,vis)
def build(name,W,H,seq):
  tl=[];t=0;parts=[]
  def sil(d,f):
    subprocess.run(['ffmpeg','-y','-v','error','-f','lavfi','-t',str(d),'-i','anullsrc=r=44100:cl=mono',f]);parts.append(f)
  for k,item in enumerate(seq):
    if item[0]=='clip':
      a,b,v,caps,vis=CL[item[1]];d=b-a;f=f'{S}/tmp_{name}_{k}.wav'
      subprocess.run(['ffmpeg','-y','-v','error','-ss',str(a),'-i',SRC,'-t',str(d),'-ac','1','-af',f'afade=t=in:d=0.25:curve=qsin,afade=t=out:st={d-0.6}:d=0.6:curve=qsin',f]);parts.append(f)
      tl.append(dict(type='clip',t0=t,t1=t+d,voice=v,caps=caps,vis=vis));t+=d
      sil(0.5,f'{S}/tmp_{name}_{k}g.wav');t+=0.5
    else:
      d=item[2];sil(d,f'{S}/tmp_{name}_{k}.wav');tl.append(dict(type=item[0],t0=t,t1=t+d,text=item[1]));t+=d
  lst=f'{S}/tmp_{name}.txt';open(lst,'w').write(''.join(f"file '{p}'\n" for p in parts))
  vo=f'{S}/{name}_voice.wav';subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',lst,'-ar','44100',vo])
  # music bed: soft chords
  mus=f'{S}/{name}_mix.wav'
  expr="0.05*(sin(2*PI*220*t)+sin(2*PI*277.2*t)+sin(2*PI*329.6*t))*(0.6+0.4*sin(2*PI*0.25*t))*(1+0.0*t)"
  subprocess.run(['ffmpeg','-y','-v','error','-i',vo,'-f','lavfi','-t',str(t),'-i',f"aevalsrc='{expr}':s=44100",'-filter_complex',
   '[1]lowpass=f=1200,volume=0.35,afade=t=in:d=1.5,afade=t=out:st=%f:d=1.5[m];[m][0]sidechaincompress=threshold=0.03:ratio=6:release=400[md];[0]volume=1.0[v];[v][md]amix=inputs=2:normalize=0,loudnorm=I=-15:TP=-1.5'%(t-1.5),'-ar','44100','-ac','2',mus])
  x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',vo,'-f','s16le','-ac','1','-ar','44100','-'],capture_output=True).stdout,np.int16).astype(float)/32768
  n=int(t*FPS);hop=44100//FPS;amp=[float(min(1,np.sqrt(np.mean(x[i*hop:(i+1)*hop]**2+1e-9))*6)) for i in range(n)]
  with sync_playwright() as p:
    br=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg=br.new_page(viewport={'width':W,'height':H});pg.goto(f'file://{S}/tpl.html');pg.wait_for_timeout(2500)
    pg.evaluate('d=>init(d)',dict(W=W,H=H,tl=tl,amp=amp,T=t));pg.wait_for_timeout(800)
    out=f'{S}/{name}.mp4'
    ff=subprocess.Popen(['ffmpeg','-y','-v','error','-f','image2pipe','-r',str(FPS),'-i','-','-i',mus,'-map','0:v','-map','1:a','-c:v','libx264','-pix_fmt','yuv420p','-crf','20','-preset','fast','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',out],stdin=subprocess.PIPE)
    for i in range(n):
      pg.evaluate(f'render({i/FPS})');ff.stdin.write(pg.screenshot(type='jpeg',quality=90))
      if i%150==75: pg.screenshot(path=f'{S}/snap_{name}_{i}.png')
    ff.stdin.close();ff.wait()
  print(name,round(t,1))
C=lambda k:('clip',k)
full('F1',1.9,99.2,1,['before.jpg','after1.jpg','after2.jpg','ba3.jpg','before.jpg','after1.jpg']);full('F2',99.4,156.0,2,['after1.jpg','P:shampoo','after2.jpg','P:cream','before.jpg']);full('F3',177.6,210.5,3,['before.jpg','after2.jpg','P:all']);full('F4',223.1,231.6,3,['after1.jpg','ba2.jpg'])
JOBS={
'MaJa_1_Shampoo_9x16':(1080,1920,[C('H1'),C('A1'),C('D1'),C('B2'),C('B3'),('outro','',3.4)]),
'MaJa_1_Shampoo_1x1':(1080,1080,[C('H1'),C('A1'),C('D1'),C('B2'),C('B3'),('outro','',3.4)]),
'MaJa_2_Cream_9x16':(1080,1920,[C('D3'),C('D5'),C('A2'),C('D2'),C('B3'),('outro','',3.4)]),
'MaJa_3_School_9x16':(1080,1920,[C('C1'),C('D6'),C('C2'),C('H2'),C('D4'),('outro','',3.4)]),
}
for k in sys.argv[1:]: build(k,*JOBS[k])
