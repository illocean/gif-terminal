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

t = gifos.Terminal(width=720, height=480, xpad=10, ypad=10)

t.set_prompt(f"{G}{USERNAME}{XX}@{C}profile{XX} $ ")

# ============ SCREEN 1: BOOT ============
t.gen_text(f"{C}", row_num=1)
t.gen_text(f"  {'='*56}  ", row_num=1)
t.gen_text(f"  |  ____  _   _ ____  _        _    __     __  |  ", row_num=2)
t.gen_text(f"  | |  _ \\| \\ | |  _ \\| |      / \\   \\ \\   / /  |  ", row_num=3)
t.gen_text(f"  | | |_) |  \\| | | | | |     / _ \\   \\ \\ / /   |  ", row_num=4)
t.gen_text(f"  | |  __/| |\\  | |_| | |___ / ___ \\   \\ V /    |  ", row_num=5)
t.gen_text(f"  | |_|   |_| \\_|____/|_____/_/   \\_\\   \\_/     |  ", row_num=6)
t.gen_text(f"  |                                                 |  ", row_num=7)
t.gen_text(f"  |  {C}DIT Student @ PUP Taguig{XX}                    |  ", row_num=8)
t.gen_text(f"  {'='*56}  ", row_num=9)
t.gen_text(f"{XX}", row_num=10)
t.clone_frame(40)

t.gen_text(f"  {G}SYSTEM INIT{XX}", row_num=12)
t.clone_frame(2)
t.gen_text(f"  {GR}{'>>'}{XX} Loading kernel........{G}DONE{XX}", row_num=13)
t.clone_frame(2)
t.gen_text(f"  {GR}{'>>'}{XX} Initializing terminal..{G}DONE{XX}", row_num=14)
t.clone_frame(2)
t.gen_text(f"  {GR}{'>>'}{XX} Connecting to GitHub...{G}DONE{XX}", row_num=15)
t.clone_frame(2)
t.gen_text(f"  {GR}{'>>'}{XX} Rendering profile......{G}DONE{XX}", row_num=16)
t.clone_frame(15)

# ============ SCREEN 2: PROFILE (cat profile.txt) ============
t.clear_frame()

t.gen_text(f"{C}", row_num=1)
t.gen_text(f"  {'='*56}  ", row_num=1)
t.gen_text(f"  |  {W} ___  __ _(_)_ __ ___   ___  ___  _   _ _ __ ___ ___ {XX}  |  ", row_num=2)
t.gen_text(f"  |  {W}/ _ \\/ _` | | '_ ` _ \\ / _ \\/ __|| | | | '__/ __/ _ \\{XX}  |  ", row_num=3)
t.gen_text(f"  | {W}|  __/ (_| | | | | | | | (_) \\__ \\| |_| | | | (_|  __/{XX}  |  ", row_num=4)
t.gen_text(f"  |  {W}\\___|\\__,_|_|_| |_| |_|\\___/|___/ \\__,_|_|  \\___\\___|{XX}  |  ", row_num=5)
t.gen_text(f"  {'='*56}  ", row_num=6)
t.gen_text(f"{XX}", row_num=7)
t.clone_frame(10)

t.gen_text(f"  {G}cat profile.txt{XX}", row_num=8)
t.clone_frame(5)

profile_data = [
    (f"{GR}pandadoor@github{XX} {M}~>{XX} {Y}Name{GR}:{XX}", f"{W}Kim Phillip G. Andador{XX}"),
    (f"{GR}pandadoor@github{XX} {M}~>{XX} {Y}Handle{GR}:{XX}", f"{C}{USERNAME}{XX}"),
    (f"{GR}pandadoor@github{XX} {M}~>{XX} {Y}School{GR}:{XX}", f"{W}PUP Taguig - DIT (2nd Year){XX}"),
    (f"{GR}pandadoor@github{XX} {M}~>{XX} {Y}Location{GR}:{XX}", f"{W}Paranaque City, Philippines{XX}"),
    (f"{GR}pandadoor@github{XX} {M}~>{XX} {Y}Email{GR}:{XX}", f"{C}andadorkimphillip@gmail.com{XX}"),
    (f"{GR}pandadoor@github{XX} {M}~>{XX} {Y}GitHub{GR}:{XX}", f"{C}github.com/{USERNAME}{XX}"),
]

for i, (label, value) in enumerate(profile_data):
    t.gen_text(f"  {label} {value}", row_num=9 + i)
    t.clone_frame(3)

t.clone_frame(10)

t.gen_text(f"  {GR}{'>>>'}{XX} {W}Full-stack developer in training.{XX}", row_num=16)
t.clone_frame(2)
t.gen_text(f"  {GR}{'>>>'}{XX} {W}Building software, solving problems, learning daily.{XX}", row_num=17)
t.clone_frame(15)

# ============ SCREEN 3: TECH STACK ============
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

t.gen_text(f"  {G}cat skills.txt{XX}", row_num=9)
t.clone_frame(5)

tech = [
    (f"{Y}Languages{GR}:{XX}",  f"{W}C, C++, C#, Java, JavaScript, TypeScript, COBOL, VB.NET{XX}"),
    (f"{Y}Web{GR}:{XX}",        f"{W}PHP, Laravel, HTML, CSS{XX}"),
    (f"{Y}Database{GR}:{XX}",   f"{W}PostgreSQL, MySQL, SQL{XX}"),
    (f"{Y}Tools{GR}:{XX}",      f"{W}Git, VS Code, Visual Studio, .NET, Node.js{XX}"),
    (f"{Y}Platforms{GR}:{XX}",  f"{W}Windows, Linux{XX}"),
    (f"{Y}Domains{GR}:{XX}",    f"{W}Software Dev, IT Support, Troubleshooting{XX}"),
]

for i, (label, value) in enumerate(tech):
    t.gen_text(f"  {label} {value}", row_num=10 + i)
    t.clone_frame(2)

t.clone_frame(20)

# ============ SCREEN 4: LIVE CODING PREVIEW ============
t.clear_frame()

t.gen_text(f"{C}", row_num=1)
t.gen_text(f"  {'='*56}  ", row_num=1)
t.gen_text(f"  |  {W}  _     ___     ___   ___   _     ___   ___  {XX}  |  ", row_num=2)
t.gen_text(f"  |  {W} | |   / _ \\   / __| | _ \\ | |   / _ \\ / __| {XX}  |  ", row_num=3)
t.gen_text(f"  |  {W} | |__| (_) | | (__  |   / | |__| (_) | (__  {XX}  |  ", row_num=4)
t.gen_text(f"  |  {W} |____|\\___/   \\___| |_|_\\ |____|\\___/ \\___| {XX}  |  ", row_num=5)
t.gen_text(f"  {'='*56}  ", row_num=6)
t.gen_text(f"{XX}", row_num=7)
t.clone_frame(10)

t.gen_text(f"  {G}$ ./projects --list{XX}", row_num=8)
t.clone_frame(5)

projects = [
    f"  {GR}1.{XX} {C}crm{XX}              {GR}-{XX} {W}Customer relationship management{XX}",
    f"  {GR}2.{XX} {C}Scientific-Calculator{XX}  {GR}-{XX} {W}Java DSA final project{XX}",
    f"  {GR}3.{XX} {C}Basic-Campus-Ledger{XX}    {GR}-{XX} {W}Laravel + PostgreSQL info system{XX}",
    f"  {GR}4.{XX} {C}Inventory-Management{XX}   {GR}-{XX} {W}COBOL indexed file handling{XX}",
    f"  {GR}5.{XX} {C}MorphosPowerPointAddIn{XX} {GR}-{XX} {W}C# VSTO add-in{XX}",
    f"  {GR}6.{XX} {C}System-Cleaner{XX}         {GR}-{XX} {W}Interactive terminal UI cleaner{XX}",
    f"  {GR}7.{XX} {C}marketplace{XX}            {GR}-{XX} {W}Spicetify extension marketplace{XX}",
    f"  {GR}8.{XX} {C}Php-mysql-crud{XX}         {GR}-{XX} {W}PHP CRUD implementation{XX}",
]

for i, line in enumerate(projects):
    t.gen_text(line, row_num=9 + i)
    t.clone_frame(2)

t.clone_frame(20)

# ============ SCREEN 5: FOOTER ============
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

t.gen_text(f"  {GR}{'-'*56}{XX}", row_num=8)
t.clone_frame(3)

contact_info = [
    f"  {Y}GitHub{GR}:{XX}     {C}https://github.com/{USERNAME}{XX}",
    f"  {Y}Email{GR}:{XX}      {C}andadorkimphillip@gmail.com{XX}",
    f"  {Y}Location{GR}:{XX}   {W}Paranaque City, Philippines{XX}",
    f"  {Y}Updated{GR}:{XX}    {W}{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}{XX}",
]

for i, line in enumerate(contact_info):
    t.gen_text(f"  {line}", row_num=9 + i)
    t.clone_frame(3)

t.clone_frame(8)

t.gen_text(f"  {C}{'~'*56}{XX}", row_num=14)
t.clone_frame(2)
t.gen_text(f"  {G}  Thanks for stopping by!{XX}", row_num=15)
t.clone_frame(2)
t.gen_text(f"  {G}  Have a great day!{XX}", row_num=16)
t.gen_text(f"  {C}{'~'*56}{XX}", row_num=17)
t.clone_frame(50)

t.gen_gif()

print("\nGIF generated: output.gif")
print("Profile README is now live with the new terminal GIF!")
