import gifos
import os, glob, requests
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageChops
from gifos.utils.convert_ansi_escape import ConvertAnsiEscape

ConvertAnsiEscape.ANSI_ESCAPE_MAP_TXT_COLOR.update({
    "39": "#F2F2F2", "31": "#CC0000", "32": "#4EAA25",
    "33": "#C4A000", "34": "#3465A4", "35": "#75507B",
    "36": "#06989A", "37": "#D3D7CF", "91": "#EF2929",
    "92": "#8AE234", "93": "#FCE94F", "94": "#729FCF",
    "95": "#AD7FA8", "96": "#34E2E2", "97": "#EEEEEC",
})

USERNAME = (
    os.environ.get("GITHUB_REPOSITORY_OWNER")
    or os.environ.get("GIT_USERNAME")
    or "pandadoor"
)

GIF_W, GIF_H  = 740, 540
WIN_X, WIN_Y  = 20, 20
WIN_W         = 700
TITLE_H       = 28
MENU_H        = 22
HEADER_H      = TITLE_H + MENU_H
WIN_H         = HEADER_H + 450
TERMINAL_X    = WIN_X
TERMINAL_Y    = WIN_Y + HEADER_H
CORNER_RADIUS = 6
BG            = (8, 8, 10)
FRAMES_DIR    = "./frames"
FRAME_BASE    = "frame_"
OUTPUT_GIF    = "output.gif"
GIFOS_FPS     = 18

GIT_TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""
HDR = {"Authorization": f"Bearer {GIT_TOKEN}", "Accept": "application/vnd.github+json"} if GIT_TOKEN else {}
HDR2 = {"Accept": "application/vnd.github+json"}

STATS = {"name": "", "repos": 0, "commits": 0, "stars": 0, "prs": 0, "issues": 0, "followers": 0, "langs": []}
try:
    u = requests.get(f"https://api.github.com/users/{USERNAME}", headers=HDR, timeout=10).json()
    STATS["name"] = u.get("name") or USERNAME
    STATS["repos"] = u.get("public_repos", 0)
    STATS["followers"] = u.get("followers", 0)

    repos = requests.get(f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=updated", headers=HDR2, timeout=15).json() or []
    lc = {}
    for r in repos:
        l = r.get("language")
        if l: lc[l] = lc.get(l, 0) + 1
        STATS["stars"] += r.get("stargazers_count", 0)
        STATS["issues"] += r.get("open_issues_count", 0)
    STATS["langs"] = [l for l,_ in sorted(lc.items(), key=lambda x: -x[1])[:4]]

    try:
        c_hdr = dict(HDR2)
        c_hdr["Accept"] = "application/vnd.github.cloak-preview"
        cq = f"author:{USERNAME}"
        cs = requests.get(f"https://api.github.com/search/commits?q={cq}&per_page=1", headers=c_hdr, timeout=10).json()
        if "total_count" in cs:
            STATS["commits"] = cs["total_count"]
    except:
        pass

    pq = f"is:pr author:{USERNAME} is:merged"
    pr = requests.get(f"https://api.github.com/search/issues?q={pq}&per_page=1", headers=HDR2, timeout=10).json()
    STATS["prs"] = pr.get("total_count", 0)

    print(f"Stats: name='{STATS['name']}' repos={STATS['repos']} commits={STATS['commits']} stars={STATS['stars']} prs={STATS['prs']} issues={STATS['issues']} followers={STATS['followers']} langs={STATS['langs']}")
    has_stats = True
except Exception as e:
    print(f"Stats fetch error: {e}, repos count: {STATS['repos']}")
    has_stats = False

def _blend(b, o):
    return Image.alpha_composite(b.convert("RGBA"), o).convert("RGB")
def _f(s=11):
    try: return ImageFont.load_default(size=s)
    except: return ImageFont.load_default()

def chrome_mask(fr):
    r, g, b = ImageChops.difference(fr, Image.new("RGB", fr.size, BG)).split()
    return ImageChops.lighter(ImageChops.lighter(r, g), b).point(lambda p: 255 if p > 0 else 0)

def prep():
    bgi = Image.new("RGB", (GIF_W, GIF_H), (14, 14, 20))
    sh = Image.new("RGBA", (GIF_W, GIF_H), (0,0,0,0))
    ImageDraw.Draw(sh).rounded_rectangle([(WIN_X+3,WIN_Y+3),(WIN_X+WIN_W+3,WIN_Y+WIN_H+3)],
        radius=CORNER_RADIUS, fill=(0,0,0,100))
    sh = sh.filter(ImageFilter.GaussianBlur(radius=6))
    base = _blend(bgi, sh)

    def fr(reg, bl, tint):
        return _blend(reg.filter(ImageFilter.GaussianBlur(radius=bl)),
            Image.new("RGBA", reg.size, tint))

    tr = bgi.crop((WIN_X,WIN_Y,WIN_X+WIN_W,WIN_Y+TITLE_H))
    mr = bgi.crop((WIN_X,WIN_Y+TITLE_H,WIN_X+WIN_W,WIN_Y+HEADER_H))
    cr = bgi.crop((TERMINAL_X,TERMINAL_Y,TERMINAL_X+WIN_W,TERMINAL_Y+450))

    win = Image.new("RGB", (WIN_W, WIN_H))
    win.paste(fr(tr, 3, (16,16,24,235)), (0,0))
    win.paste(fr(mr, 2, (18,18,26,225)), (0,TITLE_H))
    win.paste(fr(cr, 4, (8,8,14,230)), (0,HEADER_H))

    mk = Image.new("L", (WIN_W, WIN_H), 0)
    ImageDraw.Draw(mk).rounded_rectangle([(0,0),(WIN_W-1,WIN_H-1)], radius=CORNER_RADIUS, fill=255)
    base.paste(win, (WIN_X, WIN_Y), mk)

    ch = Image.new("RGBA", (GIF_W, GIF_H), (0,0,0,0))
    d = ImageDraw.Draw(ch)
    d.rounded_rectangle([(WIN_X,WIN_Y),(WIN_X+WIN_W-1,WIN_Y+WIN_H-1)],
        radius=CORNER_RADIUS, outline=(120,120,140,50), width=1)
    d.line([(WIN_X+8,WIN_Y+TITLE_H),(WIN_X+WIN_W-8,WIN_Y+TITLE_H)], fill=(120,120,140,25), width=1)
    d.line([(WIN_X+8,WIN_Y+HEADER_H),(WIN_X+WIN_W-8,WIN_Y+HEADER_H)], fill=(120,120,140,20), width=1)

    tf = _f(11)
    d.text((WIN_X+10, WIN_Y+(TITLE_H-11)//2), f"{USERNAME}@pandadoor: ~",
        fill=(160,160,175,230), font=tf)

    br, by = 7, WIN_Y + TITLE_H//2
    cx = WIN_X + WIN_W - 14
    mx = cx - 22; nx = mx - 22
    d.ellipse([(cx-br,by-br),(cx+br,by+br)], fill=(200,28,28,235), outline=(240,55,55,170))
    d.ellipse([(mx-br,by-br),(mx+br,by+br)], fill=(50,50,56,210), outline=(85,85,92,150))
    d.ellipse([(nx-br,by-br),(nx+br,by+br)], fill=(50,50,56,210), outline=(85,85,92,150))

    mf = _f(10)
    x2, y2 = WIN_X+8, WIN_Y+TITLE_H+(MENU_H-10)//2
    for it in ["File","Edit","View","Search","Terminal","Help"]:
        d.text((x2, y2), it, fill=(150,150,162,220), font=mf)
        x2 += len(it)*6 + 12

    return base, ch

def post(base, ch):
    files = sorted(glob.glob(f"{FRAMES_DIR}/{FRAME_BASE}*.png"),
        key=lambda x: int(os.path.splitext(os.path.basename(x))[0].split("_")[1]))
    print(f"Processing {len(files)} frames...")
    for fp in files:
        tf = Image.open(fp).convert("RGB")
        c = base.copy()
        c.paste(tf, (TERMINAL_X, TERMINAL_Y), chrome_mask(tf))
        c = _blend(c, ch)
        c.save(fp, "PNG")

t = gifos.Terminal(width=WIN_W, height=450, xpad=10, ypad=10)
t.set_prompt(f"\x1b[92m{USERNAME}\x1b[0m@\x1b[96mpandadoor\x1b[0m $ ")

t.gen_text("\x1b[92m[OK]\x1b[0m Reached target.", row_num=1)
t.clone_frame(2)
t.gen_text("\x1b[92m[OK]\x1b[0m Session ready.", row_num=2)
t.clone_frame(2)
t.gen_text("\x1b[92m[OK]\x1b[0m Profile service started.", row_num=3)
t.clone_frame(5)

t.gen_prompt(row_num=4)
t.gen_typing_text("stats --user " + USERNAME, row_num=4, contin=True, speed=2)
t.clone_frame(2)

t.gen_text("", row_num=5)
t.gen_text(f"\x1b[96m--- {USERNAME} ---\x1b[0m", row_num=6)
t.clone_frame(2)

if has_stats:
    sl = [
        f"\x1b[93mName:\x1b[0m      {STATS['name']}",
        f"\x1b[93mRepos:\x1b[0m     {STATS['repos']}",
        f"\x1b[93mCommits:\x1b[0m   {STATS['commits']}",
        f"\x1b[93mStars:\x1b[0m     {STATS['stars']}",
        f"\x1b[93mPRs:\x1b[0m       {STATS['prs']}",
        f"\x1b[93mIssues:\x1b[0m    {STATS['issues']}",
        f"\x1b[93mFollowers:\x1b[0m {STATS['followers']}",
    ]
    if STATS['langs']:
        sl.append(f"\x1b[93mLangs:\x1b[0m     {', '.join(STATS['langs'])}")
else:
    sl = [
        f"\x1b[93mName:\x1b[0m      Kim Phillip G. Andador",
        f"\x1b[93mRepos:\x1b[0m     {STATS['repos'] if STATS['repos'] else '--'}",
        f"\x1b[93mFollowers:\x1b[0m {STATS['followers'] if STATS['followers'] else '--'}",
    ]

for l in sl:
    t.gen_text(l, row_num=7+sl.index(l))
    t.clone_frame(1)

t.clone_frame(3)
t.gen_text("\x1b[96m---\x1b[0m", row_num=7+len(sl))
t.clone_frame(2)

b = 8 + len(sl)
t.gen_prompt(row_num=b)
t.gen_typing_text("clear", row_num=b, contin=True, speed=2)
t.clone_frame(2)
t.clear_frame()

t.gen_prompt(row_num=1)
t.gen_typing_text("cat skills.txt", row_num=1, contin=True, speed=2)
t.clone_frame(2)

t.gen_text("", row_num=2)
t.gen_text("\x1b[96m--- Tech Stack ---\x1b[0m", row_num=3)
t.clone_frame(2)

SKILL_LABELS = [
    ("Languages", "C, C++, C#, Java, JavaScript, TypeScript, PHP, COBOL"),
    ("Web",       "Laravel, HTML, CSS"),
    ("Database",  "PostgreSQL, MySQL"),
    ("Tools",     "Git, VS Code, Visual Studio, .NET, Node.js"),
    ("Platforms", "Windows, Linux"),
]
for i, (lb, vl) in enumerate(SKILL_LABELS):
    sp = " " * max(1, 12 - len(lb))
    t.gen_text(f"\x1b[94m{lb}:{sp}\x1b[0m {vl}", row_num=4+i)
    t.clone_frame(1)

t.clone_frame(3)
t.gen_text("\x1b[96m---\x1b[0m", row_num=4+5)
t.clone_frame(5)

base_c, ch = prep()
post(base_c, ch)
t.gen_gif()

PAL = [
    (200,28,28),(240,55,55),(50,50,56),(85,85,92),(150,150,162),(160,160,175),
    (204,0,0),(239,41,41),(78,170,37),(196,160,0),(52,101,164),(117,80,123),
    (6,152,154),(211,215,207),(238,238,236),(242,242,242),
]

if not os.path.exists(OUTPUT_GIF):
    print("PIL assembly...")
    fs = sorted(glob.glob(f"{FRAMES_DIR}/{FRAME_BASE}*.png"),
        key=lambda x: int(os.path.splitext(os.path.basename(x))[0].split("_")[1]))
    n = len(PAL)
    h = Image.new("RGB", (n, 8))
    for i,c in enumerate(PAL):
        for y in range(8): h.putpixel((i,y), c)
    fi = Image.open(fs[0]).convert("RGB")
    hi = fi.copy(); hi.paste(h, (0,0))
    pa = hi.quantize(colors=250, method=Image.Quantize.FASTOCTREE, dither=0)
    q = [Image.open(f).convert("RGB").quantize(palette=pa, dither=1) for f in fs]
    dm = max(1, round(1000/GIFOS_FPS))
    q[0].save(OUTPUT_GIF, save_all=True, append_images=q[1:], loop=0, duration=dm)

print(f"Done: {OUTPUT_GIF}")
