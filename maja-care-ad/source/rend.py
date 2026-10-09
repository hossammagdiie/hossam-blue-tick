import sys,subprocess
from playwright.sync_api import sync_playwright
FPS=30;D=32.4;S=sys.argv[1]
with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
  pg=b.new_page(viewport={'width':1080,'height':1920})
  pg.goto('file://'+S+'/ad.html');pg.wait_for_timeout(2500);pg.evaluate('document.fonts.ready')
  ff=subprocess.Popen(['ffmpeg','-y','-v','error','-f','image2pipe','-r',str(FPS),'-i','-','-i',S+'/ad_voice.wav','-c:v','libx264','-pix_fmt','yuv420p','-crf','20','-c:a','aac','-b:a','192k','-shortest',S+'/MaJa_Care_ad.mp4'],stdin=subprocess.PIPE)
  for i in range(int(D*FPS)):
    pg.evaluate(f'render({i/FPS})');ff.stdin.write(pg.screenshot(type='jpeg',quality=92))
    if i in(60,200,500,780,940): pg.screenshot(path=f'{S}/f{i}.png')
  ff.stdin.close();ff.wait()
