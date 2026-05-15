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

t = gifos.Terminal(width=700, height=450, xpad=10, ypad=10)

t.set_prompt(f"\x1b[92m{USERNAME}\x1b[0m@\x1b[96mprofile\x1b[0m $ ")
t.gen_text("\x1b[36m", row_num=1)
t.gen_text("  .------------------------------------------------------------.  ", row_num=1)
t.gen_text("  |   ___  ___  ___ _  _ ___ _   _ ___ ___   ___ ___ ___      |  ", row_num=2)
t.gen_text("  |  | _ \\/ _ \\| _ \\\\| |_ _| \\| |_ _/ __| | __|_ _/ _ \\     |  ", row_num=3)
t.gen_text("  |  |  _/ (_) |  _/ .` || || .` || | \\__ \\ | _| | | (_) |    |  ", row_num=4)
t.gen_text("  |  |_|  \\___/|_| |_|\\_|___|_|\\_|___||___/ |_| |___\\___/     |  ", row_num=5)
t.gen_text("  '------------------------------------------------------------'  ", row_num=6)
t.gen_text("\x1b[0m", row_num=7)
t.clone_frame(30)

t.gen_text("\x1b[32m  SYSTEM BOOT\x1b[0m", row_num=8)
t.clone_frame(3)
t.gen_text("  +-- \x1b[90mInitializing kernel...\x1b[0m \x1b[32mOK\x1b[0m", row_num=9)
t.clone_frame(3)
t.gen_text("  +-- \x1b[90mLoading profile modules...\x1b[0m \x1b[32mOK\x1b[0m", row_num=10)
t.clone_frame(3)
t.gen_text("  +-- \x1b[90mFetching GitHub data...\x1b[0m \x1b[32mOK\x1b[0m", row_num=11)
t.clone_frame(3)
t.gen_text("  +-- \x1b[90mGenerating visualization...\x1b[0m \x1b[32mOK\x1b[0m", row_num=12)
t.clone_frame(15)

t.gen_text("\x1b[35m  PROFILE\x1b[0m", row_num=14)
t.clone_frame(3)

if has_stats and github_stats.languages_sorted:
    top_langs = github_stats.languages_sorted[:3]
    langs_str = ", ".join([f"\x1b[93m{lang[0]}\x1b[97m" for lang in top_langs])
else:
    langs_str = "\x1b[90m---\x1b[97m"

commits_str = str(github_stats.total_commits_last_year) + " (last year)" if has_stats and github_stats.total_commits_last_year else "\x1b[90m---\x1b[97m"

profile_lines = [
    f"  \x1b[33mName\x1b[90m:\x1b[97m      Kim Phillip G. Andador",
    f"  \x1b[33mHandle\x1b[90m:\x1b[97m    {USERNAME}",
    f"  \x1b[33mRole\x1b[90m:\x1b[97m      JR Software Engineer",
    f"  \x1b[33mLocation\x1b[90m:\x1b[97m  Paranaque City, PH",
    f"  \x1b[33mCommits\x1b[90m:\x1b[97m   {commits_str}",
    f"  \x1b[33mStack\x1b[90m:\x1b[97m     {langs_str}",
]

for i, line in enumerate(profile_lines):
    t.gen_text(line, row_num=15 + i)
    t.clone_frame(2)

t.clone_frame(10)

t.clear_frame()

t.gen_text("\x1b[35m  ------- TECHNOLOGIES -------\x1b[0m", row_num=1)
t.clone_frame(5)

skills_data = [
    ("\x1b[33mLanguages\x1b[90m:\x1b[97m", "  C, C++, C#, Java, JavaScript, TypeScript"),
    ("\x1b[33mWeb\x1b[90m:\x1b[97m", "       PHP, Laravel, HTML, CSS"),
    ("\x1b[33mDatabase\x1b[90m:\x1b[97m", "   PostgreSQL, MySQL, SQL"),
    ("\x1b[33mTools\x1b[90m:\x1b[97m", "     Git, VS Code, Visual Studio, .NET, Node.js"),
    ("\x1b[33mPlatforms\x1b[90m:\x1b[97m", "  Windows"),
    ("\x1b[33mAlso\x1b[90m:\x1b[97m", "      COBOL, VB.NET, Tcl, Technical Support"),
]

for i, (label, value) in enumerate(skills_data):
    t.gen_text(f"  {label}{value}", row_num=2 + i)
    t.clone_frame(2)

t.clone_frame(10)

t.clear_frame()

t.gen_text("\x1b[36m", row_num=1)
t.gen_text("  .----------------------------------------------------------.  ", row_num=1)
t.gen_text("  |  ___ _   _ ___ ___ ___ ___ ___   ___ __  __   _   _ __ |  ", row_num=2)
t.gen_text("  | |_ _| \\| / __|_ _/ __| __/ _ \\ / _ \\\\ \\/ /  /_\\ | _ \\|  |  ", row_num=3)
t.gen_text("  |  | || .\` \\__ \\| | (__| _| (_) | (_) |>  <  / _ \\|   /|  |  ", row_num=4)
t.gen_text("  | |___|_|\\_\\___/___\\___|___\\___/ \\___/_/\\_\\ /_/ \\_\\_|_\\|  |  ", row_num=5)
t.gen_text("  '----------------------------------------------------------'  ", row_num=6)
t.gen_text("\x1b[0m", row_num=7)
t.clone_frame(3)

t.gen_text(f"  \x1b[90mProfile\x1b[0m  \x1b[90m:\x1b[0m  \x1b[96mhttps://github.com/{USERNAME}\x1b[0m", row_num=7)
t.clone_frame(2)
t.gen_text(f"  \x1b[90mEmail\x1b[0m   \x1b[90m:\x1b[0m  \x1b[96mandadorkimphillip@gmail.com\x1b[0m", row_num=8)
t.clone_frame(2)
t.gen_text(f"  \x1b[90mUpdated\x1b[0m \x1b[90m:\x1b[0m  \x1b[97m{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\x1b[0m", row_num=9)
t.clone_frame(2)

t.gen_text("", row_num=10)
t.clone_frame(2)
t.gen_text("  \x1b[92mThanks for stopping by!\x1b[0m", row_num=11)
t.clone_frame(2)
t.gen_text("  \x1b[92mHave a great day!\x1b[0m", row_num=12)
t.clone_frame(50)

t.gen_gif()

print("\nGIF generated: output.gif")
print("\nTo use in your README.md:")
print('![Terminal GIF](./output.gif)')
