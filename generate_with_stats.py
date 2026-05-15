import os, sys, subprocess, requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

try:
    from asciimatics.renderers import FigletText
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "asciimatics", "-q"])
    from asciimatics.renderers import FigletText

USERNAME = (
    os.environ.get("GITHUB_REPOSITORY_OWNER")
    or os.environ.get("GIT_USERNAME")
    or "pandadoor"
)

W, H, FS, LH, MG = 720, 480, 14, 22, 20
frames = []

total_repos = 0
langs = []
try:
    r = requests.get(f"https://api.github.com/users/{USERNAME}", timeout=8)
    if r.ok: total_repos = r.json().get("public_repos", 0)
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    h = {"Authorization": f"Bearer {tok}"} if tok else {}
    r2 = requests.get(f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=pushed", headers=h, timeout=8)
    if r2.ok:
        lc = {}
        for repo in r2.json():
            l = repo.get("language")
            if l: lc[l] = lc.get(l, 0) + 1
        langs = [l for l, _ in sorted(lc.items(), key=lambda x: -x[1])[:5]]
except: pass

R,G,B,C,M,Y,GR,WX,XX = "\x1b[91m","\x1b[32m","\x1b[36m","\x1b[34m","\x1b[35m","\x1b[93m","\x1b[90m","\x1b[97m","\x1b[0m"

class F:
    def __init__(s):
        s.im = Image.new("RGB", (W, H), (10, 10, 14))
        s.d = ImageDraw.Draw(s.im)
        try: s.f = ImageFont.truetype("DejaVuSansMono.ttf", FS)
        except: s.f = ImageFont.load_default()
        s.y = 14
    def l(s, t, c=(200,200,200)):
        s.d.text((MG, s.y), t, fill=c, font=s.f); s.y += LH; return s
    def g(s): s.y += LH; return s
    def end(s): frames.append(s.im)

def hold(n=6):
    for _ in range(n): frames.append(frames[-1])

def fig(txt, c=(0,200,255)):
    f = F()
    ft = FigletText(txt, font="big")
    for line in str(ft.rendered_text).split("\n"):
        if line.strip(): f.l(line, c)
    return f

fig("PANDADOR", (0,200,255)).l("").end(); hold(10)
fig("PANDADOR", (0,200,255)).l("  >> Booting system...", (0,200,0)).end(); hold(6)
fig("PANDADOR", (0,200,255)).l("  >> Booting system...[OK]", (0,200,0)).l("  >> Loading kernel...[OK]", (0,200,0)).end(); hold(6)
fig("PANDADOR", (0,200,255)).l("  >> Booting system...[OK]", (0,200,0)).l("  >> Loading kernel...[OK]", (0,200,0)).l("  >> Starting services...[OK]", (0,200,0)).end(); hold(6)
fig("PANDADOR", (0,200,255)).l("  >> Booting system...[OK]", (0,200,0)).l("  >> Loading kernel...[OK]", (0,200,0)).l("  >> Starting services...[OK]", (0,200,0)).l("  >> Profile ready.", (0,200,0)).end(); hold(12)

items = [
    ("name     ", "Kim Phillip G. Andador",   (255,255,255)),
    ("handle   ", USERNAME,                   (0,200,255)),
    ("school   ", "PUP Taguig - DIT (2nd)",   (255,255,255)),
    ("location ", "Paranaque City, PH",        (255,255,255)),
    ("email    ", "andadorkimphillip@gmail.com",(0,200,255)),
    ("github   ", f"github.com/{USERNAME}",   (0,200,255)),
]

F().l("  $ cat profile.txt", (0,200,0)).g().end(); hold(5)
for n in range(len(items)):
    f = F().l("  $ cat profile.txt", (0,200,0)).g()
    for j,(k,v,vc) in enumerate(items):
        if j <= n:
            f.d.text((MG, f.y), f"  {k}", fill=(255,200,0), font=f.f)
            kw = f.d.textlength(f"  {k}", font=f.f)
            f.d.text((MG+kw, f.y), v, fill=vc, font=f.f); f.y += LH
        else: f.l("")
    f.end(); hold(4)

f = F().l("  $ cat profile.txt", (0,200,0)).g()
for k,v,vc in items:
    f.d.text((MG, f.y), f"  {k}", fill=(255,200,0), font=f.f)
    kw = f.d.textlength(f"  {k}", font=f.f)
    f.d.text((MG+kw, f.y), v, fill=vc, font=f.f); f.y += LH
f.g().l("  Building software, solving problems, learning daily.", (120,120,120))
f.end(); hold(12)

skills = [
    ("Languages", "C, C++, C#, Java, JavaScript, TypeScript, PHP, COBOL"),
    ("Web      ", "Laravel, HTML, CSS"),
    ("Database ", "PostgreSQL, MySQL"),
    ("Tools    ", "Git, VS Code, Visual Studio, .NET, Node.js"),
    ("Platforms", "Windows, Linux"),
]

F().l("  $ cat skills.txt", (0,200,0)).g().end(); hold(5)
for n in range(len(skills)):
    f = F().l("  $ cat skills.txt", (0,200,0)).g()
    for j,(k,v) in enumerate(skills):
        if j <= n: f.l(f"  {k}  {v}", (255,255,255))
        else: f.l("")
    f.end(); hold(4)

if langs:
    F().l("  Active Languages (from repos):", (255,200,0)).end(); hold(5)
    for n in range(len(langs)):
        f = F().l("  Active Languages (from repos):", (255,200,0))
        for j in range(n+1): f.l(f"    - {langs[j]}", (0,200,255))
        f.end(); hold(4)

fig("CONTACT", (0,200,255)).g().end(); hold(6)
f = fig("CONTACT", (0,200,255)).g()
f.l(f"  GitHub   https://github.com/{USERNAME}", (0,200,255)).end(); hold(4)
f = fig("CONTACT", (0,200,255)).g()
f.l(f"  GitHub   https://github.com/{USERNAME}", (0,200,255))
f.l("  Email    andadorkimphillip@gmail.com", (0,200,255)).end(); hold(4)
f = fig("CONTACT", (0,200,255)).g()
f.l(f"  GitHub   https://github.com/{USERNAME}", (0,200,255))
f.l("  Email    andadorkimphillip@gmail.com", (0,200,255))
f.l("  Location Paranaque City, Philippines", (200,200,200)).end(); hold(4)

dt = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
f = fig("CONTACT", (0,200,255)).g()
f.l(f"  GitHub   https://github.com/{USERNAME}", (0,200,255))
f.l("  Email    andadorkimphillip@gmail.com", (0,200,255))
f.l("  Location Paranaque City, Philippines", (200,200,200)).g()
f.l(f"  Last updated: {dt}", (80,80,80)).g()
f.l("  Thank you for visiting!", (0,200,100))
f.l("  Have a great day!", (0,200,100)).end(); hold(20)

frames[0].save("output.gif", save_all=True, append_images=frames[1:],
    duration=150, loop=0, optimize=False)
print(f"GIF: output.gif ({len(frames)} frames)")
