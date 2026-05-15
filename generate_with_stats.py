import gifos
import os, requests

USERNAME = (
    os.environ.get("GITHUB_REPOSITORY_OWNER")
    or os.environ.get("GIT_USERNAME")
    or "pandadoor"
)

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

t = gifos.Terminal(width=700, height=450, xpad=10, ypad=10)
t.set_prompt(f"\x1b[92m{USERNAME}\x1b[0m@\x1b[96mpandadoor\x1b[0m $ ")

t.gen_text("\x1b[92m[  OK  ]\x1b[0m Reached target Graphical Interface.", row_num=1)
t.clone_frame(5)
t.gen_text("\x1b[92m[  OK  ]\x1b[0m Started Session Manager.", row_num=2)
t.clone_frame(5)
t.gen_text("\x1b[92m[  OK  ]\x1b[0m Created user slice.", row_num=3)
t.clone_frame(5)
t.gen_text("\x1b[92m[  OK  ]\x1b[0m Started GitHub Profile Service.", row_num=4)
t.clone_frame(12)

t.gen_prompt(row_num=5)
t.gen_typing_text("./github-stats --user " + USERNAME, row_num=5, contin=True, speed=1)
t.clone_frame(5)

t.gen_text("", row_num=6)
t.gen_text(f"\x1b[96m--- GitHub Overview for {USERNAME} ---\x1b[0m", row_num=7)
t.clone_frame(3)

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

t.clone_frame(10)
t.gen_text(f"\x1b[96m--- end ---\x1b[0m", row_num=8+len(sl))
t.clone_frame(8)

bot = 9 + len(sl)
t.gen_prompt(row_num=bot)
t.gen_typing_text("cat skills.txt", row_num=bot, contin=True, speed=1)
t.clone_frame(5)
t.clear_frame()

t.gen_prompt(row_num=1)
t.gen_typing_text("cat skills.txt", row_num=1, contin=True, speed=1)
t.clone_frame(5)

t.gen_text("", row_num=2)
t.gen_text("\x1b[96m--- Tech Stack ---\x1b[0m", row_num=3)
t.clone_frame(3)

skills = [
    ("\x1b[94mLanguages:\x1b[0m  ", "C, C++, C#, Java, JavaScript, TypeScript, PHP, COBOL"),
    ("\x1b[94mWeb:\x1b[0m        ", "Laravel, HTML, CSS"),
    ("\x1b[94mDatabase:\x1b[0m   ", "PostgreSQL, MySQL"),
    ("\x1b[94mTools:\x1b[0m      ", "Git, VS Code, Visual Studio, .NET, Node.js"),
    ("\x1b[94mPlatforms:\x1b[0m  ", "Windows, Linux"),
]

for i, (label, value) in enumerate(skills):
    t.gen_text(f"{label}{value}", row_num=4+i)
    t.clone_frame(2)

t.clone_frame(10)
t.gen_text(f"\x1b[96m--- end ---\x1b[0m", row_num=4+len(skills))
t.clone_frame(6)

fr = 5 + len(skills)
t.gen_prompt(row_num=fr)
t.gen_typing_text("echo 'Thanks for visiting!'", row_num=fr, contin=True, speed=1)
t.clone_frame(5)
t.gen_text("\x1b[92mThanks for visiting!\x1b[0m", row_num=fr+1)
t.clone_frame(40)

t.gen_gif()

print("GIF generated: output.gif")
