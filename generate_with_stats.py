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

R = "\x1b[91m"
G = "\x1b[32m"
Y = "\x1b[93m"
B = "\x1b[34m"
C = "\x1b[36m"
M = "\x1b[35m"
W = "\x1b[97m"
GR = "\x1b[90m"
XX = "\x1b[0m"

def section_line(row_num, t_instance):
    t_instance.gen_text(f"  {GR}{'='*56}{XX}", row_num=row_num)

t = gifos.Terminal(width=720, height=480, xpad=10, ypad=10)

t.set_prompt(f"{G}{USERNAME}{XX}@{C}profile{XX} $ ")

# ============ SCREEN 1: BOOT SEQUENCE ============
t.gen_text(f"{C}", row_num=1)
t.gen_text(f"  {'='*56}  ", row_num=1)
t.gen_text(f"  |  ____  _   _ ____  _        _    __     __  |  ", row_num=2)
t.gen_text(f"  | |  _ \\| \\ | |  _ \\| |      / \\   \\ \\   / /  |  ", row_num=3)
t.gen_text(f"  | | |_) |  \\| | | | | |     / _ \\   \\ \\ / /   |  ", row_num=4)
t.gen_text(f"  | |  __/| |\\  | |_| | |___ / ___ \\   \\ V /    |  ", row_num=5)
t.gen_text(f"  | |_|   |_| \\_|____/|_____/_/   \\_\\   \\_/     |  ", row_num=6)
t.gen_text(f"  |                                                 |  ", row_num=7)
t.gen_text(f"  |  {Y}JR Software Engineer & DIT Student{XX}           |  ", row_num=8)
t.gen_text(f"  |  {GR}Polytechnic University of the Philippines{XX}    |  ", row_num=9)
t.gen_text(f"  {'='*56}  ", row_num=10)
t.gen_text(f"{XX}", row_num=11)
t.clone_frame(40)

section_line(12, t)
t.gen_text(f"  {G}SYSTEM INIT{XX}", row_num=13)
t.clone_frame(2)
t.gen_text(f"  {GR}{'>>'}{XX} Loading kernel modules......{G}DONE{XX}", row_num=14)
t.clone_frame(2)
t.gen_text(f"  {GR}{'>>'}{XX} Initializing terminal........{G}DONE{XX}", row_num=15)
t.clone_frame(2)
t.gen_text(f"  {GR}{'>>'}{XX} Connecting to GitHub API......{G}DONE{XX}", row_num=16)
t.clone_frame(2)
t.gen_text(f"  {GR}{'>>'}{XX} Fetching profile data.........{G}DONE{XX}", row_num=17)
t.clone_frame(2)
t.gen_text(f"  {GR}{'>>'}{XX} Rendering visualization.......{G}DONE{XX}", row_num=18)
t.clone_frame(10)

# ============ SCREEN 2: SYSTEM INFO (neofetch style) ============
section_line(20, t)
t.gen_text(f"  {M}SYSTEM INFORMATION{XX}", row_num=21)
section_line(22, t)
t.clone_frame(5)

sysinfo = [
    f"  {GR}OS{XX}          {W}GitHub Profile v1.0{XX}",
    f"  {GR}User{XX}        {C}{USERNAME}{XX}",
    f"  {GR}Host{XX}        {W}Kim Phillip G. Andador{XX}",
    f"  {GR}Role{XX}        {Y}JR Software Engineer{XX}",
    f"  {GR}Education{XX}   {W}DIT @ PUP Taguig{XX}",
    f"  {GR}Location{XX}    {W}Paranaque City, Philippines{XX}",
    f"  {GR}Shell{XX}       {W}/bin/zsh{XX}",
]

for i, line in enumerate(sysinfo):
    t.gen_text(line, row_num=23 + i)
    t.clone_frame(2)

t.clone_frame(15)

# ============ SCREEN 3: GITHUB STATS ============
t.clear_frame()

t.gen_text(f"{C}", row_num=1)
t.gen_text(f"  {'='*56}  ", row_num=1)
t.gen_text(f"  |  {W} __ _  _  __ _  _ __   ___ __ _(_)_(_)___ __ _{XX}  |  ", row_num=2)
t.gen_text(f"  |  {W} / _`| || / _` || '_ \\ / __/ _` | | __/ _ \\ '_ \\{XX}  |  ", row_num=3)
t.gen_text(f"  |  {W}| (_| \\ V / (_| | | | | (_| (_| | | ||  __/ | | |{XX}  |  ", row_num=4)
t.gen_text(f"  |  {W} \\__, |\\_/ \\__, |_| |_|\\___\\__,_|_|\\__\\___|_| |_|{XX}  |  ", row_num=5)
t.gen_text(f"  |  {W} |___/     |___/                                 {XX}  |  ", row_num=6)
t.gen_text(f"  {'='*56}  ", row_num=7)
t.gen_text(f"{XX}", row_num=8)
t.clone_frame(10)

section_line(9, t)
t.gen_text(f"  {M}GITHUB STATISTICS{XX}", row_num=10)
section_line(11, t)
t.clone_frame(5)

commits_count = github_stats.total_commits_last_year if has_stats and github_stats.total_commits_last_year else 0
stars_count = github_stats.total_stargazers if has_stats and github_stats.total_stargazers else 0
prs_count = github_stats.total_pull_requests_made if has_stats and github_stats.total_pull_requests_made else 0
issues_count = github_stats.total_issues if has_stats and github_stats.total_issues else 0
repos_count = github_stats.total_repo_contributions if has_stats and github_stats.total_repo_contributions else 0
followers_count = github_stats.total_followers if has_stats and github_stats.total_followers else 0

stats_display = [
    f"  {Y}Commits (1yr){GR}:{XX}  {W}{commits_count}{XX}",
    f"  {Y}Repositories{GR}:{XX}   {W}{repos_count}{XX}",
    f"  {Y}Pull Requests{GR}:{XX}  {W}{prs_count}{XX}",
    f"  {Y}Issues{GR}:{XX}         {W}{issues_count}{XX}",
    f"  {Y}Stars Earned{GR}:{XX}   {W}{stars_count}{XX}",
    f"  {Y}Followers{GR}:{XX}      {W}{followers_count}{XX}",
]

for i, line in enumerate(stats_display):
    t.gen_text(line, row_num=12 + i)
    t.clone_frame(2)

t.clone_frame(8)

if has_stats and github_stats.languages_sorted:
    t.gen_text(f"  {GR}{'-'*56}{XX}", row_num=12 + len(stats_display))
    t.gen_text(f"  {M}TOP LANGUAGES{XX}", row_num=13 + len(stats_display))
    t.clone_frame(3)
    top_langs = github_stats.languages_sorted[:6]
    bar_max = 30
    for idx, (lang, pct) in enumerate(top_langs):
        bar_len = max(1, int((pct / 100.0) * bar_max))
        bar = f"{G}{'#' * bar_len}{XX}"
        t.gen_text(f"  {C}{lang:12s}{GR}:{XX} {bar} {W}{pct:.1f}%{XX}", row_num=14 + len(stats_display) + idx)
        t.clone_frame(2)

t.clone_frame(20)

# ============ SCREEN 4: EXPERIENCE & EDUCATION ============
t.clear_frame()

t.gen_text(f"{C}", row_num=1)
t.gen_text(f"  {'='*56}  ", row_num=1)
t.gen_text(f"  |  {W} ___   ___   ___   ___   ___  ___   ___   _  |{XX}  |  ", row_num=2)
t.gen_text(f"  |  {W}| _ \\ / _ \\ / __| | _ \\ | _ \\/ _ \\ / __| | | |{XX}  |  ", row_num=3)
t.gen_text(f"  |  {W}|  _/| (_) | (__  |   / |  _/ (_) | (__  |_| |{XX}  |  ", row_num=4)
t.gen_text(f"  |  {W}|_|   \\___/ \\___| |_|_\\ |_|  \\___/ \\___| (_) |{XX}  |  ", row_num=5)
t.gen_text(f"  {'='*56}  ", row_num=6)
t.gen_text(f"{XX}", row_num=7)
t.clone_frame(10)

section_line(8, t)
t.gen_text(f"  {M}JOURNEY{XX}", row_num=9)
section_line(10, t)
t.clone_frame(5)

timeline = [
    f"  {Y}2026{GR}:{XX}  {W}2nd Year{GR} -{XX} {C}DIT @ PUP Taguig{XX}",
    f"  {Y}2024{GR}:{XX}  {W}ICT Graduate{GR} -{XX} {C}Moreh Academy{XX}",
    f"  {Y}2023{GR}:{XX}  {W}IT Intern{GR} -{XX} {C}Moreh Academy IT Dept{XX}",
    f"  {Y}2024{GR}:{XX}  {W}PUPCET Qualifier{GR} -{XX} {C}PUP Admissions Test{XX}",
]

for i, line in enumerate(timeline):
    t.gen_text(line, row_num=11 + i)
    t.clone_frame(3)

t.clone_frame(10)

section_line(16, t)
t.gen_text(f"  {M}ACHIEVEMENTS{XX}", row_num=17)
section_line(18, t)
t.clone_frame(3)

achievements = [
    f"  {GR}*{XX} {W}Developed campus ledger system with Laravel & PostgreSQL{XX}",
    f"  {GR}*{XX} {W}Built COBOL inventory management with indexed file handling{XX}",
    f"  {GR}*{XX} {W}Created PowerPoint VSTO add-in for font/color cleanup (C#){XX}",
    f"  {GR}*{XX} {W}Developed scientific calculator with Java Swing + FlatLaf{XX}",
    f"  {GR}*{XX} {W}Published Spicetify extensions (TypeScript, JavaScript){XX}",
]

for i, line in enumerate(achievements):
    t.gen_text(line, row_num=19 + i)
    t.clone_frame(2)

t.clone_frame(15)

# ============ SCREEN 5: TECH STACK ============
t.clear_frame()

t.gen_text(f"{C}", row_num=1)
t.gen_text(f"  {'='*56}  ", row_num=1)
t.gen_text(f"  |  {W} _____  ___ ___  ___   _     ___  ___  ___{XX}  |  ", row_num=2)
t.gen_text(f"  |  {W}|_   _|/ __/ __|/ _ \\ | |   / _ \\| _ \\/ __|{XX}  |  ", row_num=3)
t.gen_text(f"  |  {W}  | || (__\\__ \\ (_) || |__| (_) |   /\\__ \\{XX}  |  ", row_num=4)
t.gen_text(f"  |  {W}  |_| \\___|___/\\___( )____|\\___/|_|_\\|___/{XX}  |  ", row_num=5)
t.gen_text(f"  |  {W}                   |/                          {XX}  |  ", row_num=6)
t.gen_text(f"  {'='*56}  ", row_num=7)
t.gen_text(f"{XX}", row_num=8)
t.clone_frame(10)

section_line(9, t)
t.gen_text(f"  {M}SKILLS & TECHNOLOGIES{XX}", row_num=10)
section_line(11, t)
t.clone_frame(5)

tech_categories = [
    (f"{Y}Languages{GR}:{XX}", "  C, C++, C#, Java, JavaScript, TypeScript, COBOL, VB.NET, Tcl"),
    (f"{Y}Web{GR}:{XX}", "       PHP, Laravel, HTML, CSS"),
    (f"{Y}Database{GR}:{XX}", "   PostgreSQL, MySQL, SQL"),
    (f"{Y}Tools{GR}:{XX}", "     Git, VS Code, Visual Studio, .NET SDK, Node.js"),
    (f"{Y}Frameworks{GR}:{XX}", "  Laravel, Windows Forms, .NET Framework"),
    (f"{Y}Platforms{GR}:{XX}", "  Windows, Linux (WSL)"),
    (f"{Y}Expertise{GR}:{XX}", "  Software Dev, Technical Support, Troubleshooting, IT Support"),
]

for i, (label, value) in enumerate(tech_categories):
    t.gen_text(f"  {label}{value}", row_num=12 + i)
    t.clone_frame(2)

t.clone_frame(15)

# ============ SCREEN 6: CONTACT / FOOTER ============
t.clear_frame()

t.gen_text(f"{C}", row_num=1)
t.gen_text(f"  {'='*56}  ", row_num=1)
t.gen_text(f"  |  {W}  ___ ___  _  _ _____ ___ ___ ___ ___  ___{XX}  |  ", row_num=2)
t.gen_text(f"  |  {W} / __/ _ \\| \\| |_   _|_ _/ __| __/ _ \\|   \\{XX}  |  ", row_num=3)
t.gen_text(f"  |  {W}| (_| (_) | .\` | | |  | | (__| _| (_) | |) |{XX}  |  ", row_num=4)
t.gen_text(f"  |  {W} \\___\\___/|_|\\_| |_| |___\\___|___\\___/|___/{XX}  |  ", row_num=5)
t.gen_text(f"  {'='*56}  ", row_num=6)
t.gen_text(f"{XX}", row_num=7)
t.clone_frame(15)

section_line(8, t)
t.gen_text(f"  {M}CONTACT{XX}", row_num=9)
section_line(10, t)
t.clone_frame(3)

contact = [
    f"  {GR}GitHub{XX}   {C}https://github.com/{USERNAME}{XX}",
    f"  {GR}Email{XX}    {C}andadorkimphillip@gmail.com{XX}",
    f"  {GR}Location{XX} {W}Paranaque City, NCR, Philippines{XX}",
]

for i, line in enumerate(contact):
    t.gen_text(line, row_num=11 + i)
    t.clone_frame(3)

t.clone_frame(8)

timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
t.gen_text(f"  {GR}Last updated{XX}  {W}{timestamp}{XX}", row_num=15)
t.clone_frame(5)

t.gen_text(f"", row_num=17)
t.gen_text(f"  {C}{'~'*56}{XX}", row_num=18)
t.clone_frame(2)
t.gen_text(f"  {G}  Thanks for visiting my profile!{XX}", row_num=19)
t.gen_text(f"  {G}  Have an amazing day!{XX}", row_num=20)
t.gen_text(f"  {C}{'~'*56}{XX}", row_num=21)
t.clone_frame(50)

t.gen_gif()

print("\nGIF generated: output.gif")
print("Profile README is now live with the new terminal GIF!")
