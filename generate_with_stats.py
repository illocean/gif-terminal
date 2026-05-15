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

t.set_prompt(f"\x1b[91m{USERNAME}\x1b[0m@\x1b[93mgithub\x1b[0m ~> ")

t.gen_text("Initializing terminal...", row_num=1)
t.clone_frame(5)
t.gen_text("\x1b[32m[OK]\x1b[0m System ready", row_num=2)
t.clone_frame(10)

t.gen_prompt(row_num=3)
t.gen_typing_text("cat profile.txt", row_num=3, contin=True, speed=1)
t.clone_frame(5)

t.gen_text("", row_num=4)
t.gen_text(f"\x1b[96m=== {USERNAME} ===\x1b[0m", row_num=5)
t.clone_frame(3)

if has_stats:
    account_name = github_stats.account_name or USERNAME
    stats_lines = [
        f"\x1b[93mName:\x1b[0m        Kim Phillip G. Andador",
        f"\x1b[93mRole:\x1b[0m        JR Software Engineer",
        f"\x1b[93mCommits:\x1b[0m     {github_stats.total_commits_last_year} (last year)",
    ]
    if github_stats.languages_sorted:
        top_langs = github_stats.languages_sorted[:3]
        langs_str = ", ".join([f"{lang[0]} ({lang[1]}%)" for lang in top_langs])
        stats_lines.append(f"\x1b[93mTop Langs:\x1b[0m   {langs_str}")
else:
    stats_lines = [
        "\x1b[93mName:\x1b[0m        Kim Phillip G. Andador",
        "\x1b[93mRole:\x1b[0m        JR Software Engineer",
    ]

for i, line in enumerate(stats_lines):
    t.gen_text(line, row_num=6+i)
    t.clone_frame(3)

t.clone_frame(10)
t.gen_text("\x1b[96m================================\x1b[0m", row_num=6+len(stats_lines))
t.clone_frame(15)

t.gen_prompt(row_num=7+len(stats_lines))
t.gen_typing_text("clear", row_num=7+len(stats_lines), contin=True, speed=1)
t.clone_frame(5)
t.clear_frame()

t.gen_prompt(row_num=1)
t.gen_typing_text("cat skills.txt", row_num=1, contin=True, speed=1)
t.clone_frame(5)

t.gen_text("", row_num=2)
t.gen_text("\x1b[96m=== Skills ===\x1b[0m", row_num=3)
t.clone_frame(3)

skills = [
    ("\x1b[94mLanguages:\x1b[0m  ", "C, C++, C#, Java, JavaScript, TypeScript"),
    ("\x1b[94mWeb:\x1b[0m        ", "PHP, Laravel, HTML, CSS"),
    ("\x1b[94mDatabase:\x1b[0m   ", "PostgreSQL, MySQL, SQL"),
    ("\x1b[94mTools:\x1b[0m      ", "Git, VS Code, Visual Studio"),
    ("\x1b[94mPlatforms:\x1b[0m  ", "Windows, .NET, Node.js"),
    ("\x1b[94mOther:\x1b[0m      ", "COBOL, VB.NET, Tcl, Technical Support"),
]

for i, (label, value) in enumerate(skills):
    t.gen_text(f"{label}{value}", row_num=4+i)
    t.clone_frame(2)

t.clone_frame(10)
t.gen_text("\x1b[96m================================\x1b[0m", row_num=4+len(skills))
t.clone_frame(5)

final_row = 5 + len(skills)
t.gen_prompt(row_num=final_row)
t.gen_typing_text("echo 'Thanks for visiting!'", row_num=final_row, contin=True, speed=1)
t.clone_frame(5)
t.gen_text("\x1b[92mThanks for visiting!\x1b[0m", row_num=final_row+1)
t.clone_frame(40)

t.gen_gif()

print("\n GIF generated: output.gif")
print("\nTo use in your README.md:")
print('![Terminal GIF](./output.gif)')
