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
LH = 22
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

def hold(n=8):
    for _ in range(n):
        frames.append(frames[-1])

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

# ============ BOOT SEQUENCE (line by line, visible) ============
f = Frame()
f.fig("PANDADOR")
f.l("  DIT Student @ PUP Taguig", c=(100, 100, 120))
f.end()
hold(10)

f = Frame()
f.fig("PANDADOR")
f.l("", c=(50, 50, 50))
f.l("  >> Booting system...", c=(0, 200, 0))
f.end()
hold(8)

f = Frame()
f.fig("PANDADOR")
f.l("", c=(50, 50, 50))
f.l("  >> Booting system... [OK]", c=(0, 200, 0))
f.l("  >> Loading kernel modules...", c=(0, 200, 0))
f.end()
hold(8)

f = Frame()
f.fig("PANDADOR")
f.l("", c=(50, 50, 50))
f.l("  >> Booting system... [OK]", c=(0, 200, 0))
f.l("  >> Loading kernel modules... [OK]", c=(0, 200, 0))
f.l("  >> Initializing display...", c=(0, 200, 0))
f.end()
hold(8)

f = Frame()
f.fig("PANDADOR")
f.l("", c=(50, 50, 50))
f.l("  >> Booting system... [OK]", c=(0, 200, 0))
f.l("  >> Loading kernel modules... [OK]", c=(0, 200, 0))
f.l("  >> Initializing display... [OK]", c=(0, 200, 0))
f.l("  >> Fetching GitHub data...", c=(0, 200, 0))
f.end()
hold(8)

f = Frame()
f.fig("PANDADOR")
f.l("", c=(50, 50, 50))
f.l("  >> Booting system... [OK]", c=(0, 200, 0))
f.l("  >> Loading kernel modules... [OK]", c=(0, 200, 0))
f.l("  >> Initializing display... [OK]", c=(0, 200, 0))
f.l("  >> Fetching GitHub data... [OK]", c=(0, 200, 0))
f.l("  >> Profile loaded. Ready.", c=(0, 200, 0))
f.end()
hold(15)

# ============ PROFILE (line by line typing) ============
items = [
    ("name     ", "Kim Phillip G. Andador",    (255, 255, 255)),
    ("handle   ", USERNAME,                   (0, 200, 255)),
    ("school   ", "PUP Taguig - DIT (2nd)",   (255, 255, 255)),
    ("location ", "Paranaque City, PH",        (255, 255, 255)),
    ("email    ", "andadorkimphillip@gmail.com", (0, 200, 255)),
    ("github   ", f"github.com/{USERNAME}",   (0, 200, 255)),
]

f = Frame()
f.l("  $ cat profile.txt", c=(0, 200, 0))
f.g()
f.end()
hold(6)

for n in range(len(items)):
    f = Frame()
    f.l("  $ cat profile.txt", c=(0, 200, 0))
    f.g()
    for j, (k, v, vc) in enumerate(items):
        if j <= n:
            f.kv(f"  {k}", v, vc)
        else:
            f.l("")
    f.end()
    hold(5)

f = Frame()
f.l("  $ cat profile.txt", c=(0, 200, 0))
f.g()
for k, v, vc in items:
    f.kv(f"  {k}", v, vc)
f.g()
f.l("  Building software, solving problems, learning daily.", c=(120, 120, 120))
f.end()
hold(15)

# ============ SKILLS (line by line typing) ============
skills = [
    ("Languages", "C, C++, C#, Java, JavaScript, TypeScript, COBOL, VB.NET"),
    ("Web      ", "PHP, Laravel, HTML, CSS"),
    ("Database ", "PostgreSQL, MySQL, SQLite"),
    ("Tools    ", "Git, VS Code, Visual Studio, .NET, Node.js"),
    ("Platforms", "Windows, Linux"),
]

f = Frame()
f.l("  $ cat skills.txt", c=(0, 200, 0))
f.g()
f.end()
hold(6)

for n in range(len(skills)):
    f = Frame()
    f.l("  $ cat skills.txt", c=(0, 200, 0))
    f.g()
    for j, (k, v) in enumerate(skills):
        if j <= n:
            f.kv(f"  {k}", v, (255, 255, 255))
        else:
            f.l("")
    f.end()
    hold(4)

hold(8)

# ============ LIVE LANGUAGES ============
if stats.get("langs"):
    f = Frame()
    f.l("  $ cat skills.txt", c=(0, 200, 0))
    f.g()
    f.l("  Active Languages (from repos):", c=(255, 200, 0))
    f.end()
    hold(6)
    for lang in stats["langs"]:
        f = Frame()
        f.l("  $ cat skills.txt", c=(0, 200, 0))
        f.g()
        f.l("  Active Languages (from repos):", c=(255, 200, 0))
        idx = stats["langs"].index(lang)
        for i, l2 in enumerate(stats["langs"]):
            if i <= idx:
                f.l(f"    - {l2}", c=(0, 200, 255))
        f.end()
        hold(5)
    hold(10)

# ============ CONTACT ============
f = Frame()
f.fig("CONTACT", c=(0, 200, 255))
f.g()
f.end()
hold(8)

f = Frame()
f.fig("CONTACT", c=(0, 200, 255))
f.g()
f.kv("  GitHub   ", f"https://github.com/{USERNAME}", (0, 200, 255))
f.end()
hold(5)

f = Frame()
f.fig("CONTACT", c=(0, 200, 255))
f.g()
f.kv("  GitHub   ", f"https://github.com/{USERNAME}", (0, 200, 255))
f.kv("  Email    ", "andadorkimphillip@gmail.com", (0, 200, 255))
f.end()
hold(5)

f = Frame()
f.fig("CONTACT", c=(0, 200, 255))
f.g()
f.kv("  GitHub   ", f"https://github.com/{USERNAME}", (0, 200, 255))
f.kv("  Email    ", "andadorkimphillip@gmail.com", (0, 200, 255))
f.kv("  Location ", "Paranaque City, Philippines", (255, 255, 255))
f.end()
hold(5)

dt = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
f = Frame()
f.fig("CONTACT", c=(0, 200, 255))
f.g()
f.kv("  GitHub   ", f"https://github.com/{USERNAME}", (0, 200, 255))
f.kv("  Email    ", "andadorkimphillip@gmail.com", (0, 200, 255))
f.kv("  Location ", "Paranaque City, Philippines", (255, 255, 255))
f.g()
f.l(f"  Last updated: {dt}", c=(80, 80, 80))
f.g()
f.l("  Thank you for visiting!", c=(0, 200, 100))
f.l("  Have a great day!", c=(0, 200, 100))
f.end()
hold(20)

# ============ EXPORT GIF ============
DUR_MS = 180
frames[0].save("output.gif", save_all=True, append_images=frames[1:],
    duration=DUR_MS, loop=0, optimize=False)

print(f"GIF generated: output.gif ({len(frames)} frames)")
print(f"Duration per frame: {DUR_MS}ms")
print(f"Total duration: ~{len(frames) * DUR_MS / 1000:.1f}s")
