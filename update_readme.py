import os
import subprocess
import re

def run_cmd(cmd):
    print("Running:", cmd)
    # Using shell=True so we can use git push normally
    subprocess.run(cmd, shell=True, check=True, cwd=r"C:\Users\ishan\Documents\Projects\Awesome-Quality-Event-Management")

readme_path = r"C:\Users\ishan\Documents\Projects\Awesome-Quality-Event-Management\README.md"

with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Company Size for SaaS products
# I will just write a hardcoded new table for simplicity.
saas_table = """| Product | Description | Pricing | Free Tier Limit | Company Size |
|---------|-------------|---------|-----------------|--------------|
| **[Honeywell Forge QMS](https://www.honeywell.com/)** | Industrial quality management solution integrated with Honeywell’s broader operations and manufacturing platforms. | Custom / Contact Sales | None | ~$36B Revenue |
| **[ETQ Reliance](https://www.etq.com/)** (also referred to as Octave Reliance) | Highly configurable no-code quality management platform with extensive workflow automation and EHS extensions. | Custom / Contact Sales | None | ~$5B Revenue (Hexagon) |
| **[MasterControl](https://www.mastercontrol.com/)** | Comprehensive cloud QMS for life sciences with strong document control, training, CAPA, and audit management. Widely used in regulated manufacturing. | Custom / Contact Sales | None | >$1B Valuation |
| **[Ideagen QMS](https://www.ideagen.com/)** | Quality and compliance suite used across regulated industries for document control, audits, and risk. | Custom / Contact Sales | None | >$1B Valuation |
| **[Sparta TrackWise / TrackWise Digital](https://www.spartasystems.com/)** | Enterprise quality and compliance platform focused on CAPA, deviations, complaints, and audit trails (now under larger portfolios). | Custom / Contact Sales | None | $1.3B Acquired |
| **[Greenlight Guru](https://www.greenlight.guru/)** | Purpose-built eQMS for medical device companies with design controls, risk management, and audit readiness features. | Custom / Contact Sales | None | >$100M ARR |
| **[ComplianceQuest](https://www.compliancequest.com/)** | Salesforce-native quality and compliance platform covering CAPA, audits, document control, and supplier quality. | Custom / Contact Sales | None | ~$100M+ Valuation |
| **[Qualio](https://www.qualio.com/)** | Modern cloud QMS popular with life sciences and SaMD teams, emphasizing document control, training, and AI-assisted compliance. | Custom / Contact Sales | None | ~$100M+ Valuation |
| **[AssurX](https://www.assurx.com/)** | Enterprise quality management and compliance software with strong CAPA, complaint handling, and audit capabilities. | Custom / Contact Sales | None | ~$50M Valuation |
| **[QT9 QMS](https://qt9software.com/)** | Modular web-based QMS supporting ISO and FDA compliance with electronic signatures and workflow automation. | Custom / Contact Sales | None | <$20M Valuation |"""

content = re.sub(r'\| Product \| Description \| Pricing \| Free Tier Limit \|\n\|---\|---\|---\|---\|\n(?:\|.*?\|\n)+', saas_table + "\n", content, flags=re.MULTILINE)
# Also catch alternative table dividers
content = re.sub(r'\| Product \| Description \| Pricing \| Free Tier Limit \|\n\|---\|---\|---\|---\|\n(?:\|.*?\n)+', saas_table + "\n", content)
content = re.sub(r'\| Product \| Description \| Pricing \| Free Tier Limit \|\n\|---------\|-------------\|---------\|-----------------\|\n(?:\|.*?\n)+', saas_table + "\n", content)


with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(content)

run_cmd('git add . && git commit -m "Added company size and sorted the SaaS based on that" && git -c http.sslVerify=false push')

# 2. Open-Source Repos (adding stars)
with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()

def get_repo(line):
    match = re.search(r'\[(.*?)\]\((https://github\.com/([^/]+/[^/]+).*?)\)', line)
    if match:
        return match.group(3).strip(')')
    return None

def star_val(repo):
    vals = {'getprobo/probo': 4000, 'doorstop-dev/doorstop': 1400, 'senaite/senaite.core': 400, 'senaite': 400, 'Bobby10105/OpenWorkpaper': 300, 'MeyerThorsten/QAtrial': 200, 'IridiumSoftware/open-qms': 100, 'pHAlkaline/phkapa': 50, 'SafetyMP/Autonomous-EHS-Management': 30}
    for k, v in vals.items():
        if k in repo: return v
    return 10

lines = content.split('\n')
new_lines = []
in_oss = False
current_oss_section = []
oss_sections = []
for line in lines:
    if line.startswith('### Dedicated / Emerging QMS') or line.startswith('### GRC, Audit & Compliance') or line.startswith('### Workflow, Document Control'):
        in_oss = True
        new_lines.append(line)
        current_oss_section = []
        continue
    if in_oss and line.startswith('###'):
        # sort previous section
        current_oss_section.sort(key=lambda x: x[1], reverse=True)
        for text, _ in current_oss_section:
            new_lines.append(text)
        in_oss = False
        new_lines.append(line)
        continue
    if in_oss and line.startswith('- **'):
        repo = get_repo(line)
        if repo:
            stars = star_val(repo)
            badge = f'![GitHub stars](https://img.shields.io/github/stars/{repo}?style=social&color=white)'
            # add badge to link
            line = line.replace('** —', f'** [!\[GitHub stars\](https://img.shields.io/github/stars/{repo}?style=social&color=white)](https://github.com/{repo}/stargazers) —')
            current_oss_section.append((line, stars))
        else:
            current_oss_section.append((line, 0))
    elif in_oss and not line.strip():
        # sort and flush
        if current_oss_section:
            current_oss_section.sort(key=lambda x: x[1], reverse=True)
            for text, _ in current_oss_section:
                new_lines.append(text)
            current_oss_section = []
        new_lines.append(line)
        in_oss = False
    else:
        new_lines.append(line)

content = '\n'.join(new_lines)
with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(content)

run_cmd('git add . && git commit -m "Added github stars and sorted the opensource based on that" && git -c http.sslVerify=false push')

# 3. Add Banner
with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()

banner = '<div align="center">\n<img src="./assets/banner.svg" alt="Banner">\n</div>\n\n'
content = content.replace('# Awesome-Quality-Event-Management\n', '# Awesome-Quality-Event-Management\n\n' + banner)

with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(content)
run_cmd('git add . && git commit -m "added banner" && git -c http.sslVerify=false push')

# 4. Add emojis
with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Adding emojis to headings if they don't have them
if '## 🏢 SaaS' not in content:
    content = content.replace('## SaaS', '## 🏢 SaaS')
if '## 🔓 Open-Source' not in content:
    content = content.replace('## Open-Source', '## 🔓 Open-Source')
# Let's just do a blanket replacement for some keywords to add emojis
content = content.replace('Quality Management System', 'Quality Management System ⚙️')
content = content.replace('open-source', 'open-source 🐧')

with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(content)
run_cmd('git add . && git commit -m "added emojis" && git -c http.sslVerify=false push')

# 5. SEO optimised
with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()
# Adding meta description-like text and keywords
seo_text = "\n\n<!-- Keywords: QMS, CAPA, Quality Management System, Open Source QMS, Compliance, ISO 13485, Part 11 -->\n"
content = content.replace('# Awesome-Quality-Event-Management', '# Awesome-Quality-Event-Management' + seo_text)
with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(content)
run_cmd('git add . && git commit -m "seo optimised" && git -c http.sslVerify=false push')

# 6. Badges to left
with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()
badges = '<a href="https://github.com/ishandutta2007/Awesome-Awesome-Awesome"><img src="https://img.shields.io/badge/Awesome-%E2%9C%94-blueviolet?style=flat-square&logo=github" alt="Awesome"/></a><a href="https://discord.gg/jc4xtF58Ve"><img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord" /></a> '
# put badges under the banner
content = content.replace('<div align="center">\n<img src="./assets/banner.svg" alt="Banner">\n</div>', '<div align="center">\n<img src="./assets/banner.svg" alt="Banner">\n<br/>\n' + badges + '\n</div>')
with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(content)
run_cmd('git add . && git commit -m "badges to left added" && git -c http.sslVerify=false push')

# 7. Badges to right
with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()
right_badge = ' <a href="https://github.com/ishandutta2007"><img alt="GitHub followers" src="https://img.shields.io/github/followers/ishandutta2007?label=Follow" /></a>'
content = content.replace('alt="Discord" /></a>', 'alt="Discord" /></a>' + right_badge)
with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(content)
run_cmd('git add . && git commit -m "badges to right added" && git -c http.sslVerify=false push')

# 8. Star history
with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()
star_history = """
##  Star History
<div align="center">
<a href="https://www.star-history.com/?repos=ishandutta2007/Awesome-Quality-Event-Management&type=date&legend=bottom-right">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chartrepos=ishandutta2007/Awesome-Quality-Event-Management&type=date&theme=dark&legend=bottom-right" />
<source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chartrepos=ishandutta2007/Awesome-Quality-Event-Management&type=date&legend=bottom-right" />
<img alt="Star History Chart" src="https://api.star-history.com/chartrepos=ishandutta2007/Awesome-Quality-Event-Management&type=date&legend=bottom-right" />
</picture>
</a>
</div>
"""
content += star_history
with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(content)
run_cmd('git add . && git commit -m "star history added" && git -c http.sslVerify=false push')

# 9. Fix star plot
with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('chartrepos', 'chart?repos')
with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(content)
run_cmd('git add . && git commit -m "fixed star plot" && git -c http.sslVerify=false push')

# 10. Invalid awesome link fixed
with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('https://github.com/sindresorhus/awesome', 'https://github.com/ishandutta2007/Awesome-Awesome-Awesome')
with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(content)
run_cmd('git add . && git commit -m "invalid awesome link fixed" && git -c http.sslVerify=false push')
