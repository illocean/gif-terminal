import os, sys, subprocess, requests
from datetime import datetime

try:
    from asciimatics.renderers import FigletText
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "asciimatics", "-q"])
    from asciimatics.renderers import FigletText

from PIL import Image, ImageDraw, ImageFont

USERNAME = (
    os.environ.get("GITHUB_REPOSITORY_OWNER")
    or os.environ.get("GIT_USERNAME")
    or "pandadoor"
)

W = 720
H = 480
FS = 14
LH = 20
MG = 20

frames = []

class Frame:
    def __init__(self):
        self.img = Image.new("RGB", (W, H), (8, 8, 12))
        self.d = ImageDraw.Draw(self.img)
        try:
            self.f = ImageFont.truetype("DejaVuSansMono.ttf", FS)
        except:
            self.f = ImageFont.load_default()
        self.y = 14

    def l(self, txt, c=(200, 200, 200)):
        self.d.text((MG, self.y), txt, fill=c, font=self.f)
        self.y += LH
        return self

    def g(self):
        self.y += LH
        return self

    def kv(self, k, v, vc=(200, 200, 200)):
        self.d.text((MG, self.y), k, fill=(255, 200, 0), font=self.f)
        kw = self.d.textlength(k, font=self.f)
        self.d.text((MG + kw, self.y), v, fill=vc, font=self.f)
        self.y += LH
        return self

    def fig(self, txt, c=(0, 200, 255)):
        ft = FigletText(txt, font="big")
        for line in str(ft.rendered_text).split("\n"):
            if line.strip():
                self.d.text((MG, self.y), line, fill=c, font=self.f)
                self.y += LH
        return self

    def end(self):
        frames.append(self.img)

stats = {}
try:
    r = requests.get(f"https://api.github.com/users/{USERNAME}", timeout=10)
    if r.ok:
        d = r.json()
        stats["repos"] = d.get("public_repos", 0)
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    hdrs = {"Authorization": f"Bearer {tok}"} if tok else {}
    r2 = requests.get(f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=pushed", headers=hdrs, timeout=10)
    if r2.ok:
        lc = {}
        for repo in r2.json():
            l = repo.get("language")
            if l:
                lc[l] = lc.get(l, 0) + 1
        stats["langs"] = [l for l, _ in sorted(lc.items(), key=lambda x: -x[1])[:5]]
except:
    pass

for _ in range(4):
    f = Frame()
    f.fig("PANDADOR")
    f.l("  DIT Student @ PUP Taguig", c=(100, 100, 120))
    f.end()

f = Frame()
f.fig("PANDADOR")
f.l("  >> SYSTEM READY", c=(0, 200, 0))
f.l("     Loading modules...... OK", c=(80, 180, 80))
f.l("     Connecting to GitHub... OK", c=(80, 180, 80))
f.l("     Profile loaded.", c=(80, 180, 80))
f.end()

for n in range(5):
    f = Frame()
    f.l("  $ cat profile.txt", c=(0, 200, 0))
    f.g()
    items = [
        ("name     ", "Kim Phillip G. Andador",    (255, 255, 255)),
        ("handle   ", USERNAME,                   (0, 200, 255)),
        ("school   ", "PUP Taguig - DIT (2nd)",   (255, 255, 255)),
        ("location ", "Paranaque City, PH",        (255, 255, 255)),
        ("email    ", "andadorkimphillip@gmail.com", (0, 200, 255)),
        ("github   ", f"github.com/{USERNAME}",   (0, 200, 255)),
    ]
    for j, (k, v, vc) in enumerate(items):
        if j <= n:
            f.kv(f"  {k}", v, vc)
    f.end()

f = Frame()
f.l("  $ cat profile.txt", c=(0, 200, 0))
f.g()
for k, v, vc in items:
    f.kv(f"  {k}", v, vc)
f.g()
f.l("  Building software, solving problems, learning daily.", c=(120, 120, 120))
f.end()

for _ in range(4):
    frames.append(frames[-1])

for n in range(5):
    f = Frame()
    f.l("  $ cat skills.txt", c=(0, 200, 0))
    f.g()
    skills = [
        ("Languages", "C, C++, C#, Java, JavaScript, TypeScript, COBOL, VB.NET"),
        ("Web      ", "PHP, Laravel, HTML, CSS"),
        ("Database ", "PostgreSQL, MySQL, SQLite"),
        ("Tools    ", "Git, VS Code, Visual Studio, .NET, Node.js"),
        ("Platforms", "Windows, Linux"),
    ]
    for j, (k, v) in enumerate(skills):
        if j <= n:
            f.kv(f"  {k}", v, (255, 255, 255))
    f.end()

for _ in range(4):
    frames.append(frames[-1])

if stats.get("langs"):
    f = Frame()
    f.l("  $ cat skills.txt", c=(0, 200, 0))
    f.g()
    f.l("  Active Languages:", c=(255, 200, 0))
    for lang in stats["langs"]:
        f.l(f"    - {lang}", c=(0, 200, 255))
    f.end()
    for _ in range(4):
        frames.append(frames[-1])

f = Frame()
f.fig("CONTACT", c=(0, 200, 255))
f.g()
f.kv("  GitHub   ", f"https://github.com/{USERNAME}", (0, 200, 255))
f.kv("  Email    ", "andadorkimphillip@gmail.com", (0, 200, 255))
f.kv("  Location ", "Paranaque City, Philippines", (255, 255, 255))
f.g()
dt = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
f.l(f"  Last updated: {dt}", c=(80, 80, 80))
f.g()
f.l("  Thank you for visiting!", c=(0, 200, 100))
f.l("  Have a great day!", c=(0, 200, 100))
f.end()

for _ in range(10):
    frames.append(frames[-1])

frames[0].save("output.gif", save_all=True, append_images=frames[1:],
    duration=100, loop=0, optimize=False)

print(f"GIF generated: output.gif ({len(frames)} frames)")
