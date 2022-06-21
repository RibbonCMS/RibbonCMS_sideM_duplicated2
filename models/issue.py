""" ActionsのトリガーになったIssueの内容を読み込むモデル

Attributes:
    issue_path (string): Path to issue dir
    id (None | string): Issue id
    title (None | string): Title of the issue
    labels (None | list<dict>): Labels of the issue
        List:
            Dict:
                "color": string,
                "default": bool,
                "description": string,
                "id": int,
                "name": string,
                "node_id": string,
                "url": string
    closed_at (None | string): Datetime of the issue closed 
                        => "%Y年%m月%d日 %H時%M分"
    md (None | string): Parsed markdown of the Issue body
    fm (None | Dict): Parsed frontmatter of the Issue body
        if article issue:
            "posted_at": string
            "ogp_img_theme": string 
                             => 'basic' | 'kill_la_kill' | [URL]
            "ogp_description": string
"""

import os
import json

from functions.yaml_frontmatter import parse_frontmatter_from_issue, load_frontmatter
from functions.utils import format_time, color

class Issue():
    def __init__(self, issue_path):
        self.issue_path = issue_path
        self.id = self._read_id()
        self.title = self._read_title()
        self.labels = self._read_labels()
        self.closed_at = self._read_closed_at()
        self.fm, self.md = self._read_body()

    def _read_txt(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = f.read()
            return data
        return None

    def _read_id(self):
        filepath = f'{self.issue_path}/issue_id.txt'
        text = self._read_txt(filepath)
        if text is not None:
            text = text.split('\n')[0]
        return text

    def _read_title(self):
        filepath = f'{self.issue_path}/title.txt'
        text = self._read_txt(filepath)
        if text is not None:
            text = text.split('\n')[0]
        return text

    def _read_labels(self):
        filepath = f'{self.issue_path}/labels.txt'
        text = self._read_txt(filepath)
        if text is not None:
            text = json.loads(text)
        return text

    def _read_closed_at(self):
        filepath = f'{self.issue_path}/closed_at.txt'
        text = self._read_txt(filepath)
        if text is not None:
            text = text.split('\n')[0]
            text = format_time(text)
        return text

    def _read_body(self):
        filepath = f'{self.issue_path}/body.txt'
        text = self._read_txt(filepath)
        if text is not None:
            text = text
            fm, md = parse_frontmatter_from_issue(text)
            if fm is not None:
                fm = load_frontmatter(fm)
            return fm, md
        return None, None

    def __repr__(self):
        return f"Issue(issue_path='{self.issue_path}')"

    def __str__(self):
        labels = None
        if self.labels is not None:
            labels = '\n'+json.dumps(self.labels, indent=2, ensure_ascii=False)
        fm = None
        if self.fm is not None:
            fm = '\n'+json.dumps(self.fm, indent=2, ensure_ascii=False)
        omit_md = None
        if self.md is not None:
            omit_md = self.md[:100].replace('\n', ' ')
            if len(self.md) > 100:
                omit_md += '...'
        def color_params(line):
            line = line.split(' = ')
            line[0] = color(line[0], 'CYAN')
            line[1] = color(line[1], 'BROWN')
            return f'{line[0]} = {line[1]}'
        string = []
        string += [color_params(f"issue.issue_path = '{self.issue_path}'")]
        string += [color_params(f"issue.id = '{self.id}'")]
        string += [color_params(f"issue.title = '{self.title}'")]
        string += [color_params(f"issue.labels = {labels}")]
        string += [color_params(f"issue.closed_at = '{self.closed_at}'")]
        string += [color_params(f"issue.fm = {fm}")]
        string += [color_params(f"issue.md = '{omit_md}'")]
        return "\n".join(string)

    def is_include(self, labels):
        if self.labels is not None:
            for label in labels:
                if label in [l['name'].split('/')[0] for l in self.labels]:
                    return True
        return False
    
    def get_fm(self, key):
        if self.fm is None:
            return None
        if key in self.fm.keys():
            return self.fm[key]
        return None

