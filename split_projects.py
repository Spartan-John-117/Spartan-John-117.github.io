import json
import os
import re

projects_js_path = '/home/john-spartan/Documents/portfolio/Site_Portfolio/js/data/projects.js'
out_dir = '/home/john-spartan/Documents/portfolio/Site_Portfolio/js/data/projects'

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

with open(projects_js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the JSON string part
match = re.search(r'const projectData = (\{.*?\});$', content, re.DOTALL)
if not match:
    print("Could not find projectData JSON in file.")
    exit(1)

json_str = match.group(1)
data = json.loads(json_str)

for project_id, project_info in data.items():
    title = project_info.get("title", "")
    domain = project_info.get("domain", "")
    technologies = project_info.get("technologies", [])
    markdown_content = project_info.get("content", "")
    
    # Escape backticks and ${} to prevent template literal interpolation issues
    safe_markdown = markdown_content.replace('`', '\\`').replace('${', '\\${')
    
    techs_str = json.dumps(technologies, ensure_ascii=False)
    
    js_content = f"""window.projectData = window.projectData || {{}};
window.projectData["{project_id}"] = {{
    title: {json.dumps(title, ensure_ascii=False)},
    domain: {json.dumps(domain, ensure_ascii=False)},
    technologies: {techs_str},
    content: `
{safe_markdown}
`
}};"""

    out_file = os.path.join(out_dir, f"{project_id}.js")
    with open(out_file, 'w', encoding='utf-8') as out:
        out.write(js_content)

print(f"Successfully split {len(data)} projects.")
