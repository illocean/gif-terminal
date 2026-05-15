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
BG_COLOR      = (12, 14, 15)
FRAMES_DIR    = "./frames"
FRAME_BASE    = "frame_"
OUTPUT_GIF    = "output.gif"
GIFOS_FPS     = 20

total_repos = 0
github_stats = None
has_stats = False
try:
    r = requests.get(f"https://api.github.com/users/{USERNAME}", timeout=10)
    if r.status_code == 200:
        total_repos = r.json().get("public_repos", 0)
    github_stats = gifos.utils.fetch_github_stats(user_name=USERNAME)
    has_stats = github_stats is not None
except Exception as e:
    print(f"Warning: {e}")

def _blend(base, overlay):
    return Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB")

def _font(size=11):
    try: return ImageFont.load_default(size=size)
    except TypeError: return ImageFont.load_default()

def chroma_mask(frame):
    bg = Image.new("RGB", frame.size, BG_COLOR)
    diff = ImageChops.difference(frame, bg)
    r, g, b = diff.split()
    m = ImageChops.lighter(ImageChops.lighter(r, g), b)
    return m.point(lambda p: 255 if p > 0 else 0)

def prepare_layers():
    bg = Image.new("RGB", (GIF_W, GIF_H), (16, 16, 22))
    shadow = Image.new("RGBA", (GIF_W, GIF_H), (0,0,0,0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        [(WIN_X+3, WIN_Y+3), (WIN_X+WIN_W+3, WIN_Y+WIN_H+3)],
        radius=CORNER_RADIUS, fill=(0,0,0,120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=8))
    base = _blend(bg, shadow)

    def glass(reg, blur, tint):
        bl = reg.filter(ImageFilter.GaussianBlur(radius=blur))
        return _blend(bl, Image.new("RGBA", bl.size, tint))

    tr = bg.crop((WIN_X, WIN_Y, WIN_X+WIN_W, WIN_Y+TITLE_H))
    mr = bg.crop((WIN_X, WIN_Y+TITLE_H, WIN_X+WIN_W, WIN_Y+HEADER_H))
    cr = bg.crop((TERMINAL_X, TERMINAL_Y, TERMINAL_X+WIN_W, TERMINAL_Y+450))

    ft = glass(tr, 4, (20,20,28,230))
    fm = glass(mr, 3, (24,24,32,220))
    fc = glass(cr, 6, (10,10,16,225))

    win = Image.new("RGB", (WIN_W, WIN_H))
    win.paste(ft, (0,0))
    win.paste(fm, (0,TITLE_H))
    win.paste(fc, (0,HEADER_H))

    mask = Image.new("L", (WIN_W, WIN_H), 0)
    ImageDraw.Draw(mask).rounded_rectangle([(0,0),(WIN_W-1,WIN_H-1)], radius=CORNER_RADIUS, fill=255)
    base.paste(win, (WIN_X, WIN_Y), mask)

    chrome = Image.new("RGBA", (GIF_W, GIF_H), (0,0,0,0))
    d = ImageDraw.Draw(chrome)
    d.rounded_rectangle([(WIN_X,WIN_Y),(WIN_X+WIN_W-1,WIN_Y+WIN_H-1)],
        radius=CORNER_RADIUS, outline=(100,100,120,60), width=1)
    d.line([(WIN_X+CORNER_RADIUS,WIN_Y+TITLE_H),(WIN_X+WIN_W-CORNER_RADIUS,WIN_Y+TITLE_H)],
        fill=(100,100,120,30), width=1)
    d.line([(WIN_X+CORNER_RADIUS,WIN_Y+HEADER_H),(WIN_X+WIN_W-CORNER_RADIUS,WIN_Y+HEADER_H)],
        fill=(100,100,120,25), width=1)

    tf = _font(11)
    d.text((WIN_X+10, WIN_Y+(TITLE_H-11)//2), f"{USERNAME}@debian: ~",
        fill=(180,180,190,230), font=tf)

    br, by = 7, WIN_Y + TITLE_H//2
    cx = WIN_X + WIN_W - 14
    mx = cx - 22
    nx = mx - 22
    d.ellipse([(cx-br, by-br), (cx+br, by+br)], fill=(200,30,30,235), outline=(240,60,60,180))
    d.ellipse([(mx-br, by-br), (mx+br, by+br)], fill=(55,55,60,210), outline=(90,90,95,160))
    d.ellipse([(nx-br, by-br), (nx+br, by+br)], fill=(55,55,60,210), outline=(90,90,95,160))

    mf = _font(10)
    mx2, my2 = WIN_X+8, WIN_Y+TITLE_H+(MENU_H-10)//2
    for item in ["File","Edit","View","Search","Terminal","Help"]:
        d.text((mx2, my2), item, fill=(160,160,170,220), font=mf)
        mx2 += len(item)*6 + 12

    return base, chrome

def post_process(base, chrome):
    files = sorted(glob.glob(f"{FRAMES_DIR}/{FRAME_BASE}*.png"),
        key=lambda x: int(os.path.splitext(os.path.basename(x))[0].split("_")[1]))
    print(f"Processing {len(files)} frames...")
    for fp in files:
        tf = Image.open(fp).convert("RGB")
        c = base.copy()
        c.paste(tf, (TERMINAL_X, TERMINAL_Y), chroma_mask(tf))
        c = Image.alpha_composite(c.convert("RGBA"), chrome).convert("RGB")
        c.save(fp, "PNG")

t = gifos.Terminal(width=WIN_W, height=450, xpad=10, ypad=10)
t.set_prompt(f"\x1b[92m{USERNAME}\x1b[0m@\x1b[91mdebian\x1b[0m:\x1b[94m~\x1b[0m$ ")

t.gen_text("\x1b[92m[  OK  ]\x1b[0m Reached target Graphical Interface.", row_num=1)
t.clone_frame(6)
t.gen_text("\x1b[92m[  OK  ]\x1b[0m Created user slice for pandadoor.", row_num=2)
t.clone_frame(6)
t.gen_text("\x1b[92m[  OK  ]\x1b[0m Started GitHub Profile Service.", row_num=3)
t.clone_frame(6)
t.gen_text("\x1b[92m[  OK  ]\x1b[0m Ready.", row_num=4)
t.clone_frame(14)

t.gen_prompt(row_num=5)
t.gen_typing_text("./github-stats --user " + USERNAME, row_num=5, contin=True, speed=1)
t.clone_frame(6)

t.gen_text("", row_num=6)
t.gen_text(f"\x1b[96m--- GitHub Overview for {USERNAME} ---\x1b[0m", row_num=7)
t.clone_frame(4)

if has_stats:
    rc = total_repos if total_repos else github_stats.total_repo_contributions
    sl = [
        f"\x1b[93mName:\x1b[0m        {github_stats.account_name or USERNAME}",
        f"\x1b[93mRepos:\x1b[0m       {rc}",
        f"\x1b[93mCommits:\x1b[0m     {github_stats.total_commits_last_year} (last year)",
        f"\x1b[93mStars:\x1b[0m       {github_stats.total_stargazers}",
        f"\x1b[93mPRs:\x1b[0m         {github_stats.total_pull_requests_made}",
        f"\x1b[93mIssues:\x1b[0m      {github_stats.total_issues}",
        f"\x1b[93mFollowers:\x1b[0m   {github_stats.total_followers}",
    ]
    if github_stats.languages_sorted:
        top3 = github_stats.languages_sorted[:3]
        ls = ", ".join([f"{l[0]} ({l[1]:.0f}%)" for l in top3])
        sl.append(f"\x1b[93mTop Langs:\x1b[0m   {ls}")
else:
    sl = [
        f"\x1b[93mName:\x1b[0m        Kim Phillip G. Andador",
        f"\x1b[93mRepos:\x1b[0m       {total_repos}",
        "\x1b[93mCommits:\x1b[0m     --",
        "\x1b[93mStars:\x1b[0m       --",
        "\x1b[93mPRs:\x1b[0m         --",
        "\x1b[93mIssues:\x1b[0m      --",
        "\x1b[93mFollowers:\x1b[0m   --",
    ]

for i, line in enumerate(sl):
    t.gen_text(line, row_num=8+i)
    t.clone_frame(3)

t.clone_frame(12)
t.gen_text(f"\x1b[96m--- end ---\x1b[0m", row_num=8+len(sl))
t.clone_frame(8)

bot = 9 + len(sl)
t.gen_prompt(row_num=bot)
t.gen_typing_text("cat skills.txt", row_num=bot, contin=True, speed=1)
t.clone_frame(5)
t.clear_frame()

t.gen_prompt(row_num=1)
t.gen_typing_text("cat skills.txt", row_num=1, contin=True, speed=1)
t.clone_frame(6)

t.gen_text("", row_num=2)
t.gen_text("\x1b[96m--- Tech Stack ---\x1b[0m", row_num=3)
t.clone_frame(4)

skills = [
    ("\x1b[94mLanguages:\x1b[0m  ", "C, C++, C#, Java, JavaScript, TypeScript, PHP, COBOL"),
    ("\x1b[94mWeb:\x1b[0m        ", "Laravel, HTML, CSS"),
    ("\x1b[94mDatabase:\x1b[0m   ", "PostgreSQL, MySQL"),
    ("\x1b[94mTools:\x1b[0m      ", "Git, VS Code, Visual Studio, .NET, Node.js"),
    ("\x1b[94mPlatforms:\x1b[0m  ", "Windows, Linux"),
    ("\x1b[94mDomains:\x1b[0m    ", "Software Dev, IT Support, Troubleshooting"),
]

for i, (label, value) in enumerate(skills):
    t.gen_text(f"{label}{value}", row_num=4+i)
    t.clone_frame(2)

t.clone_frame(12)
t.gen_text(f"\x1b[96m--- end ---\x1b[0m", row_num=4+len(skills))
t.clone_frame(6)

fr = 5 + len(skills)
t.gen_prompt(row_num=fr)
t.gen_typing_text("echo 'Thanks for visiting!'", row_num=fr, contin=True, speed=1)
t.clone_frame(6)
t.gen_text("\x1b[92mThanks for visiting!\x1b[0m", row_num=fr+1)
t.clone_frame(50)

base_canvas, chrome = prepare_layers()
post_process(base_canvas, chrome)
t.gen_gif()

_SIZE_HINTS = [
    (180,24,24),(239,41,41),(78,170,37),(138,226,52),(196,160,0),(252,233,79),
    (52,101,164),(114,159,207),(117,80,123),(173,127,168),(6,152,154),(52,226,226),
    (211,215,207),(238,238,236),(242,242,242),(55,55,60),(180,180,190),(160,160,170),
]

if not os.path.exists(OUTPUT_GIF):
    print("Assembling GIF with PIL...")
    files = sorted(glob.glob(f"{FRAMES_DIR}/{FRAME_BASE}*.png"),
        key=lambda x: int(os.path.splitext(os.path.basename(x))[0].split("_")[1]))
    n = len(_SIZE_HINTS)
    hint = Image.new("RGB", (n, 8))
    for i, c in enumerate(_SIZE_HINTS):
        for y in range(8): hint.putpixel((i, y), c)
    first = Image.open(files[0]).convert("RGB")
    hinted = first.copy()
    hinted.paste(hint, (0, 0))
    pal = hinted.quantize(colors=250, method=Image.Quantize.FASTOCTREE, dither=0)
    fq = []
    for f in files:
        fq.append(Image.open(f).convert("RGB").quantize(palette=pal, dither=1))
    dms = max(1, round(1000 / GIFOS_FPS))
    fq[0].save(OUTPUT_GIF, save_all=True, append_images=fq[1:], loop=0, duration=dms, optimize=False)
    print(f"GIF saved: {OUTPUT_GIF} ({len(files)} frames)")
