""" YAML付きマークダウンのパースやYAMLの読み込み

Returns:
    frontmatter: Dict
    markdown: string
"""

import yaml

def parse_frontmatter_from_issue(text):
    frontmatter = []
    yaml_start_flag = False
    lines = text.split('\n')
    for i, line in enumerate(lines):
        line = line.rstrip('\r\n')
        if line == "```yaml" or line=="```yml":
            yaml_start_flag = True
            continue
        if line == "```" and yaml_start_flag:
            frontmatter = "\n".join(frontmatter)
            markdown = "\n".join(lines[i+1:])
            return frontmatter, markdown
        if line != "" and not yaml_start_flag:
            break
        if yaml_start_flag:
            frontmatter += [line]
    frontmatter = None
    markdown = "\n".join(lines)
    return frontmatter, markdown

def parse_frontmatter_from_article(text):
    frontmatter = []
    lines = text.split('\n')
    for i in range(1, len(lines)):
        line = lines[i].rstrip('\r\n')
        if line == "---":
            frontmatter = "\n".join(frontmatter)
            markdown = "\n".join(lines[i+1:])
            return frontmatter, markdown
        frontmatter += [line]
    return None, "\n".join(lines)

def load_frontmatter(frontmatter):
    return yaml.safe_load(frontmatter)

