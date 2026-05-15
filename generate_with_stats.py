import gifos
from datetime import datetime
import os

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
    has_stats = False
    github_stats = None

G = "\x1b[32m"
Y = "\x1b[93m"
C = "\x1b[36m"
M = "\x1b[35m"
W = "\x1b[97m"
GR = "\x1b[90m"
R = "\x1b[91m"
XX = "\x1b[0m"

t = gifos.Terminal(width=720, height=480, xpad=10, ypad=10)
t.set_prompt(f"{G}{USERNAME}{XX}@{C}pandadoor{XX} $ ")

def sep(row, t_instance=t):
    t_instance.gen_text(f"  {GR}{'.'*60}{XX}", row_num=row)

# ========== SCREEN 1: WELCOME ==========
t.gen_text(f"{C}", row_num=1)
t.gen_text(f"  {'.'*60}", row_num=1)
t.gen_text(f"  .                        {W}WELCOME{XX}{C}                        .", row_num=2)
t.gen_text(f"  .{'.'*58}.", row_num=3)
t.gen_text(f"{XX}", row_num=4)
t.clone_frame(30)

t.gen_text(f"  {G}SYSTEM READY{XX}", row_num=5)
t.clone_frame(2)
t.gen_text(f"  {GR}>{XX} Loading modules......{G}OK{XX}", row_num=6)
t.clone_frame(2)
t.gen_text(f"  {GR}>{XX} Initializing display..{G}OK{XX}", row_num=7)
t.clone_frame(2)
t.gen_text(f"  {GR}>{XX} Fetching profile......{G}OK{XX}", row_num=8)
t.clone_frame(2)
t.gen_text(f"  {GR}>{XX} Rendering............{G}OK{XX}", row_num=9)
t.clone_frame(15)

# ========== SCREEN 2: PROFILE ==========
t.clear_frame()

t.gen_text(f"{C}", row_num=1)
t.gen_text(f"  {'.'*60}", row_num=1)
t.gen_text(f"  .{'.'*58}.", row_num=2)
t.gen_text(f"  .        {W}  P R O F I L E  {XX}{C}          .", row_num=3)
t.gen_text(f"  .{'.'*58}.", row_num=4)
t.gen_text(f"{XX}", row_num=5)
t.clone_frame(8)

t.gen_text(f"  {G}$ cat profile.txt{XX}", row_num=6)
t.clone_frame(5)

pf = [
    f"  {GR}pandadoor@github{XX} {Y}name{GR}:{XX}     {W}Kim Phillip G. Andador{XX}",
    f"  {GR}pandadoor@github{XX} {Y}handle{GR}:{XX}   {C}{USERNAME}{XX}",
    f"  {GR}pandadoor@github{XX} {Y}school{GR}:{XX}   {W}PUP Taguig - DIT (2nd Year){XX}",
    f"  {GR}pandadoor@github{XX} {Y}loc{GR}:{XX}      {W}Paranaque City, Philippines{XX}",
    f"  {GR}pandadoor@github{XX} {Y}email{GR}:{XX}    {C}andadorkimphillip@gmail.com{XX}",
    f"  {GR}pandadoor@github{XX} {Y}github{GR}:{XX}   {C}github.com/{USERNAME}{XX}",
]

for i, line in enumerate(pf):
    t.gen_text(line, row_num=7 + i)
    t.clone_frame(3)

t.clone_frame(8)

t.gen_text(f"  {GR}>>>{XX} {W}Full-stack developer in training.{XX}", row_num=14)
t.clone_frame(2)
t.gen_text(f"  {GR}>>>{XX} {W}Building software, solving problems, learning daily.{XX}", row_num=15)
t.clone_frame(15)

# ========== SCREEN 3: TECHNOLOGIES ==========
t.clear_frame()

t.gen_text(f"{C}", row_num=1)
t.gen_text(f"  {'.'*60}", row_num=1)
t.gen_text(f"  .{'.'*58}.", row_num=2)
t.gen_text(f"  .      {W}  T E C H N O L O G I E S  {XX}{C}     .", row_num=3)
t.gen_text(f"  .{'.'*58}.", row_num=4)
t.gen_text(f"{XX}", row_num=5)
t.clone_frame(8)

t.gen_text(f"  {G}$ cat skills.txt{XX}", row_num=6)
t.clone_frame(5)

skills = [
    f"  {Y}Languages{GR}:{XX}  {W}C, C++, C#, Java, JavaScript, TypeScript, COBOL, VB.NET{XX}",
    f"  {Y}Web{GR}:{XX}       {W}PHP, Laravel, HTML, CSS{XX}",
    f"  {Y}Database{GR}:{XX}  {W}PostgreSQL, MySQL, SQLite{XX}",
    f"  {Y}Tools{GR}:{XX}     {W}Git, VS Code, Visual Studio, .NET, Node.js{XX}",
    f"  {Y}Platforms{GR}:{XX} {W}Windows, Linux{XX}",
    f"  {Y}Domains{GR}:{XX}   {W}Software Dev, IT Support, Troubleshooting{XX}",
]

for i, (line) in enumerate(skills):
    t.gen_text(line, row_num=7 + i)
    t.clone_frame(2)

t.clone_frame(20)

# ========== SCREEN 4: PROJECTS ==========
t.clear_frame()

t.gen_text(f"{C}", row_num=1)
t.gen_text(f"  {'.'*60}", row_num=1)
t.gen_text(f"  .{'.'*58}.", row_num=2)
t.gen_text(f"  .       {W}  P R O J E C T S  {XX}{C}         .", row_num=3)
t.gen_text(f"  .{'.'*58}.", row_num=4)
t.gen_text(f"{XX}", row_num=5)
t.clone_frame(8)

t.gen_text(f"  {G}$ ls -la projects/{XX}", row_num=6)
t.clone_frame(5)

proj = [
    f"  {GR}1.{XX}  {C}crm{XX}                 {W}Customer relationship management{XX}",
    f"  {GR}2.{XX}  {C}Scientific-Calculator{XX} {W}Java DSA final project{XX}",
    f"  {GR}3.{XX}  {C}Basic-Campus-Ledger{XX}   {W}Laravel + PostgreSQL{XX}",
    f"  {GR}4.{XX}  {C}Inventory-Management{XX}  {W}COBOL file handling{XX}",
    f"  {GR}5.{XX}  {C}MorphosPowerPointAddIn{XX} {W}C# VSTO add-in{XX}",
    f"  {GR}6.{XX}  {C}System-Cleaner{XX}        {W}Terminal UI cleaner{XX}",
    f"  {GR}7.{XX}  {C}marketplace{XX}           {W}Spicetify marketplace{XX}",
    f"  {GR}8.{XX}  {C}Php-mysql-crud{XX}        {W}PHP CRUD{XX}",
]

for i, line in enumerate(proj):
    t.gen_text(line, row_num=7 + i)
    t.clone_frame(2)

t.clone_frame(20)

# ========== SCREEN 5: CONTACT ==========
t.clear_frame()

t.gen_text(f"{C}", row_num=1)
t.gen_text(f"  {'.'*60}", row_num=1)
t.gen_text(f"  .{'.'*58}.", row_num=2)
t.gen_text(f"  .        {W}  C O N T A C T  {XX}{C}           .", row_num=3)
t.gen_text(f"  .{'.'*58}.", row_num=4)
t.gen_text(f"{XX}", row_num=5)
t.clone_frame(10)

contact = [
    f"  {Y}GitHub{GR}:{XX}   {C}https://github.com/{USERNAME}{XX}",
    f"  {Y}Email{GR}:{XX}    {C}andadorkimphillip@gmail.com{XX}",
    f"  {Y}Location{GR}:{XX} {W}Paranaque City, Philippines{XX}",
]

for i, line in enumerate(contact):
    t.gen_text(f"  {line}", row_num=6 + i)
    t.clone_frame(3)

t.clone_frame(5)

dt = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
t.gen_text(f"  {GR}Last updated: {dt}{XX}", row_num=10)
t.clone_frame(5)

t.gen_text(f"  {C}{'.'*60}{XX}", row_num=12)
t.clone_frame(2)
t.gen_text(f"  {G}  Thank you for visiting!{XX}", row_num=13)
t.gen_text(f"  {G}  Have a great day!{XX}", row_num=14)
t.gen_text(f"  {C}{'.'*60}{XX}", row_num=15)
t.clone_frame(50)

t.gen_gif()

print("GIF generated: output.gif")
