import json,subprocess,sys,os,numpy as np
from playwright.sync_api import sync_playwright
S=os.path.dirname(os.path.abspath(__file__));SRC=S+'/../voice_clean.wav';FPS=30
CL={
'A1':(30.9,34.7,1,[(0,'مع نوعية شعر بنتي'),(1.6,'الموضوع كان دمار ومرار!')],'before.jpg'),
'A2':(88.3,96.0,1,[(0,'مش بيلزق الشعر خالص'),(2.2,'وبيسرّح الشعر بسهولة'),(4.2,'بيخلي الشعر طري ومفرود')],'after1.jpg'),
'B1':(102.9,109.5,2,[(0,'أول مرة في حياتي'),(1.6,'أجرّب شامبو وبلسم'),(3.6,'ويطلعوا بالتحفة دي!')],'P:shampoo'),
'B2':(123.9,132.7,2,[(0,'بسرّح شعري كل يوم'),(2.0,'ولسه الكريم فيه وريحته فيه'),(5.0,'وناعم حرير ومرطّب')],'P:cream'),
'B3':(140.9,149.1,2,[(0,'أهم حاجة تحطي الكريم'),(2.9,'ويفضل شعرك رطب طول اليوم'),(5.8,'رطب لتالت يوم!')],'after2.jpg'),
'C1':(199.5,203.0,3,[(0,'كنت قلقانة وخايفة'),(1.6,'بس لما استخدمتها.. جميلة جداً')],'P:all'),
'C2':(223.4,231.3,3,[(0,'استخدمت الهير واكس'),(1.8,'رجعت زي ما وديتها الصبح'),(4.7,'ولا شعرة هايشة.. كله نايم')],'P:wax'),
}
def build(name,W,H,seq):
  tl=[];t=0;parts=[]
  def sil(d,f):
    subprocess.run(['ffmpeg','-y','-v','error','-f','lavfi','-t',str(d),'-i','anullsrc=r=44100:cl=mono',f]);parts.append(f)
  for k,item in enumerate(seq):
    if item[0]=='clip':
      a,b,v,caps,vis=CL[item[1]];d=b-a;f=f'{S}/tmp_{name}_{k}.wav'
      subprocess.run(['ffmpeg','-y','-v','error','-ss',str(a),'-i',SRC,'-t',str(d),'-ac','1','-af',f'afade=t=in:d=0.08,afade=t=out:st={d-0.25}:d=0.25',f]);parts.append(f)
      tl.append(dict(type='clip',t0=t,t1=t+d,voice=v,caps=caps,vis=vis));t+=d
      sil(0.35,f'{S}/tmp_{name}_{k}g.wav');t+=0.35
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
JOBS={
'MaJa_Reel_9x16':(1080,1920,[('intro','فويسات حقيقية من عميلاتنا 🎧',2.6),C('A1'),C('B1'),C('C2'),C('B3'),('outro','',3.8)]),
'MaJa_Square_1x1':(1080,1080,[('intro','اسمعي بنفسك 🎧',2.4),C('B1'),C('A2'),C('C1'),C('C2'),('outro','',3.6)]),
'MaJa_Long_9x16':(1080,1920,[('intro','فويسات حقيقية من عميلاتنا 🎧',2.8),C('A1'),C('A2'),('products','منتجات MaJa Care الطبيعية',4.5),C('B1'),C('B2'),C('B3'),C('C1'),C('C2'),('outro','',4.2)]),
}
for k in sys.argv[1:]: build(k,*JOBS[k])
