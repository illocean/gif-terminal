import gifos
from datetime import datetime
import os
import requests

USERNAME = (
    os.environ.get("GITHUB_REPOSITORY_OWNER")
    or os.environ.get("GIT_USERNAME")
    or "pandadoor"
)

try:
    github_stats = gifos.utils.fetch_github_stats(user_name=USERNAME)
    has_stats = github_stats is not None
    if not has_stats:
        print("Warning: Could not fetch GitHub stats")
        print("Configure GITHUB_TOKEN in .env file")
except Exception as e:
    print(f"Warning: Error fetching GitHub stats: {e}")
    print("Using example data...")
    has_stats = False
    github_stats = None

BORDER = "\x1b[90m\u2502\x1b[0m"
SEP = "\x1b[90m\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\x1b[0m"

t = gifos.Terminal(width=700, height=450, xpad=10, ypad=10)

t.set_prompt(f"\x1b[92m{USERNAME}\x1b[0m@\x1b[96mprofile\x1b[0m $ ")

t.gen_text("\x1b[90m\u250c" + "\u2500" * 58 + "\u2510\x1b[0m", row_num=1)
t.gen_text(f"{BORDER}  \x1b[36m  ___  ___  ___ _  _ ___ _   _ ___ ___   ___ ___ ___   ___ ___ ___ _  _ \x1b[0m  {BORDER}", row_num=2)
t.gen_text(f"{BORDER}  \x1b[36m | _ \\/ _ \\| _ \\ \\| |_ _| \\| |_ _/ __| | __|_ _/ _ \\ / __|_ _/ __| \\| |\x1b[0m  {BORDER}", row_num=3)
t.gen_text(f"{BORDER}  \x1b[36m |  _/ (_) |  _/ .` || || .` || | \\__ \\ | _| | | (_) | (__ | |\\__ \\ .` |\x1b[0m  {BORDER}", row_num=4)
t.gen_text(f"{BORDER}  \x1b[36m |_|  \\___/|_| |_|\\_|___|_|\\_|___||___/ |_| |___\\___/ \\___|___|___/_|\\_|\x1b[0m  {BORDER}", row_num=5)
t.gen_text("\x1b[90m\u2514" + "\u2500" * 58 + "\u2518\x1b[0m", row_num=6)

t.clone_frame(30)

t.gen_text(SEP, row_num=7)
t.gen_text(f"{BORDER}  \x1b[32mSYSTEM BOOT\x1b[0m  ", row_num=8)
t.clone_frame(3)
t.gen_text(f"{BORDER}  \u251c\x1b[90m Initializing kernel...\x1b[0m\x1b[32m OK\x1b[0m", row_num=9)
t.clone_frame(3)
t.gen_text(f"{BORDER}  \u251c\x1b[90m Loading profile modules...\x1b[0m\x1b[32m OK\x1b[0m", row_num=10)
t.clone_frame(3)
t.gen_text(f"{BORDER}  \u251c\x1b[90m Fetching GitHub data...\x1b[0m\x1b[32m OK\x1b[0m", row_num=11)
t.clone_frame(3)
t.gen_text(f"{BORDER}  \u2514\x1b[90m Generating visualization...\x1b[0m\x1b[32m OK\x1b[0m", row_num=12)
t.clone_frame(15)

t.gen_text(SEP, row_num=13)
t.gen_text(f"{BORDER}  \x1b[35mPROFILE\x1b[0m", row_num=14)
t.clone_frame(3)

profile_lines = [
    f"{BORDER}  \x1b[33mName\x1b[0m      \x1b[90m:\x1b[0m  \x1b[97mKim Phillip G. Andador\x1b[0m",
    f"{BORDER}  \x1b[33mHandle\x1b[0m    \x1b[90m:\x1b[0m  \x1b[96m{USERNAME}\x1b[0m",
    f"{BORDER}  \x1b[33mRole\x1b[0m      \x1b[90m:\x1b[0m  \x1b[97mJR Software Engineer\x1b[0m",
    f"{BORDER}  \x1b[33mLocation\x1b[0m  \x1b[90m:\x1b[0m  \x1b[97mParanaque City, PH\x1b[0m",
]

if has_stats and github_stats.total_commits_last_year:
    profile_lines.append(f"{BORDER}  \x1b[33mCommits\x1b[0m   \x1b[90m:\x1b[0m  \x1b[97m{github_stats.total_commits_last_year} (last year)\x1b[0m")

if has_stats and github_stats.languages_sorted:
    top_langs = github_stats.languages_sorted[:3]
    langs_str = ", ".join([f"\x1b[93m{lang[0]}\x1b[0m" for lang in top_langs])
    profile_lines.append(f"{BORDER}  \x1b[33mStack\x1b[0m     \x1b[90m:\x1b[0m  {langs_str}")

for line in profile_lines:
    t.gen_text(line, row_num=15 + profile_lines.index(line))
    t.clone_frame(2)

t.clone_frame(10)
t.gen_text(SEP, row_num=15 + len(profile_lines))
t.clone_frame(5)

t.clear_frame()

t.gen_text("\x1b[90m\u250c" + "\u2500" * 58 + "\u2510\x1b[0m", row_num=1)
t.gen_text(f"{BORDER}  \x1b[35mTECHNOLOGIES\x1b[0m" + " " * 37 + f"{BORDER}", row_num=2)
t.gen_text("\x1b[90m\u251c" + "\u2500" * 58 + "\u2524\x1b[0m", row_num=3)
t.clone_frame(5)

skills_data = [
    ("\x1b[33mLanguages\x1b[0m", "C, C++, C#, Java, JavaScript, TypeScript"),
    ("\x1b[33mWeb Dev\x1b[0m", "PHP, Laravel, HTML, CSS"),
    ("\x1b[33mDatabase\x1b[0m", "PostgreSQL, MySQL, SQL"),
    ("\x1b[33mDev Tools\x1b[0m", "Git, VS Code, Visual Studio, .NET, Node.js"),
    ("\x1b[33mPlatforms\x1b[0m", "Windows"),
    ("\x1b[33mAlso\x1b[0m", "COBOL, VB.NET, Tcl, Technical Support"),
]

for i, (label, value) in enumerate(skills_data):
    row = 4 + i
    t.gen_text(f"{BORDER}  {label}\x1b[90m:\x1b[0m  \x1b[97m{value}\x1b[0m" + " " * max(1, 50 - len(label) - len(value)) + f"{BORDER}", row_num=row)
    t.clone_frame(2)

t.clone_frame(8)
t.gen_text("\x1b[90m\u2514" + "\u2500" * 58 + "\u2518\x1b[0m", row_num=4 + len(skills_data))
t.clone_frame(10)

t.clear_frame()

t.gen_text("\x1b[90m\u250c" + "\u2500" * 58 + "\u2510\x1b[0m", row_num=1)
t.gen_text(f"{BORDER}  \x1b[36m  ___ _   _ ___ ___ ___ ___ ___   ___ __  __   _   _ ___ ___ ___ \x1b[0m  {BORDER}", row_num=2)
t.gen_text(f"{BORDER}  \x1b[36m |_ _| \\| / __|_ _/ __| __/ _ \\ / _ \\\\ \\/ /  /_\\ | _ \\_ _/ __|\x1b[0m  {BORDER}", row_num=3)
t.gen_text(f"{BORDER}  \x1b[36m  | || .\` \\__ \\| | (__| _| (_) | (_) |>  <  / _ \\|   /| |\\__ \\\x1b[0m  {BORDER}", row_num=4)
t.gen_text(f"{BORDER}  \x1b[36m |___|_|\\_\\___/___\\___|___\\___/ \\___/_/\\_\\ /_/ \\_\\_|_\\___||___/\x1b[0m  {BORDER}", row_num=5)
t.gen_text("\x1b[90m\u2514" + "\u2500" * 58 + "\u2518\x1b[0m", row_num=6)

t.clone_frame(3)

t.gen_text(f"{BORDER}  \x1b[90mProfile\x1b[0m  \x1b[90m:\x1b[0m  \x1b[96mhttps://github.com/{USERNAME}\x1b[0m" + " " * 15 + f"{BORDER}", row_num=7)
t.clone_frame(2)
t.gen_text(f"{BORDER}  \x1b[90mEmail\x1b[0m   \x1b[90m:\x1b[0m  \x1b[96mandadorkimphillip@gmail.com\x1b[0m" + " " * 10 + f"{BORDER}", row_num=8)
t.clone_frame(2)
t.gen_text(f"{BORDER}  \x1b[90mUpdated\x1b[0m \x1b[90m:\x1b[0m  \x1b[97m{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\x1b[0m" + " " * 5 + f"{BORDER}", row_num=9)
t.clone_frame(2)

t.gen_text(f"{BORDER}" + " " * 58 + f"{BORDER}", row_num=10)
t.clone_frame(2)
t.gen_text(f"{BORDER}  \x1b[92m  Thanks for stopping by!  \x1b[0m" + " " * 28 + f"{BORDER}", row_num=11)
t.clone_frame(2)
t.gen_text(f"{BORDER}  \x1b[92m  Have a great day!        \x1b[0m" + " " * 28 + f"{BORDER}", row_num=12)
t.gen_text("\x1b[90m\u2514" + "\u2500" * 58 + "\u2518\x1b[0m", row_num=13)
t.clone_frame(50)

t.gen_gif()

print("\nGIF generated: output.gif")
print("\nTo use in your README.md:")
print('![Terminal GIF](./output.gif)')
