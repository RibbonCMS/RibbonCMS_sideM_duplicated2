""" 記事のモデル

Attributes:
    slug (string): slug if the article
    title (string): Title of the article
    markdown (string): The body content of the article
    tag_ids (list<string>): Tag ids of the article
    posted_at (string): Datetime of the article posted 
                        => %Y年%m月%d日 %H時%M分
    updated_at (string): Datetime of the article updated 
                        => %Y年%m月%d日 %H時%M分
    description (string): OGP description
"""
import os 

import yaml

from functions.yaml_frontmatter import parse_frontmatter_from_article, load_frontmatter
from functions.utils import color

class Article():
    def __init__(
            self, 
            slug=None, 
            title=None, 
            markdown=None, 
            tag_ids=None, 
            posted_at=None, 
            updated_at=None, 
            description=None,
            ):
        self.slug = slug
        self.title = title
        self.markdown = markdown
        self.tag_ids = tag_ids
        self.posted_at = posted_at
        self.updated_at = updated_at
        self.description = description

    @classmethod
    def from_article(cls, article_path, slug):
        article_path = f'{article_path}/{slug}/index.md'
        if not os.path.exists(article_path):
            print(f'{article_path} is not exists.')
            return Article()
        with open(article_path, "r") as f:
            text = f.read()
        fm, markdown = parse_frontmatter_from_article(text)
        fm = load_frontmatter(fm)

        def fm_getter(key):
            if key in fm.keys():
                return fm[key]
            else:
                return None

        title = fm_getter("title")
        tag_ids = fm_getter("tag_ids")
        posted_at = fm_getter("posted_at")
        updated_at = fm_getter("updated_at")
        description = fm_getter("description")
        return Article(
                    slug=slug, 
                    title=title, 
                    markdown=markdown, 
                    tag_ids=tag_ids, 
                    posted_at=posted_at, 
                    updated_at=updated_at, 
                    description=description,
                )

    def update(
            self,
            slug=None, 
            title=None, 
            markdown=None, 
            tag_ids=None, 
            posted_at=None,
            updated_at=None,
            description=None,
            ):
        if slug is not None:
            self.slug = slug
        if title is not None:
            self.title = title
        if markdown is not None:
            self.markdown = markdown
        if tag_ids is not None:
            self.tag_ids = tag_ids
        if posted_at is not None:
            self.posted_at = posted_at
        if updated_at is not None:
            self.updated_at = updated_at
        if description is not None:
            self.description = description

    def __repr__(self):
        text  = [f"Article("]
        text += [f"    slug='{self.slug}', "]
        text += [f"    title='{self.title}', "]
        text += [f'    markdown="""{self.markdown}""", ']
        text += [f"    tag_ids={self.tag_ids}, "]
        text += [f"    posted_at='{self.posted_at}', "]
        text += [f"    updated_at='{self.updated_at}', "]
        text += [f'    description="""{self.description}""",']
        text += [f")"]
        return "\n".join(text)

    def __str__(self):
        omit_md = None
        if self.markdown is not None:
            omit_md = self.markdown[:100].replace('\n', ' ')
            if len(self.markdown) > 100:
                omit_md += '...'
        omit_description = None
        if self.description is not None:
            omit_description = self.description[:100].replace('\n', ' ')
            if len(self.description) > 100:
                omit_description += '...'
        def color_params(line):
            line = line.split(' = ')
            line[0] = color(line[0], 'CYAN')
            line[1] = color(line[1], 'BROWN')
            return f'{line[0]} = {line[1]}'
        text  = []
        text += [color_params(f"article.slug = '{self.slug}' ")]
        text += [color_params(f"article.title = '{self.title}' ")]
        text += [color_params(f"article.markdown = '{omit_md}' ")]
        text += [color_params(f"article.tag_ids = '{self.tag_ids}' ")]
        text += [color_params(f"article.posted_at = '{self.posted_at}' ")]
        text += [color_params(f"article.updated_at = '{self.updated_at}' ")]
        text += [color_params(f"article.description = '{omit_description}'")]
        return "\n".join(text)
        
    def save(self, article_dir):
        article_path = f"{article_dir}/{self.slug}"
        if not os.path.exists(article_path):
            os.makedirs(article_path)
        output = self._format_output()
        with open(f'{article_path}/index.md', 'w') as f:
            f.write(output)

    def _format_output(self):
        fm = self._format_frontmatter()
        md = self._format_markdown()
        output = f"---\n{fm}\n---\n{md}"
        return output

    def _format_frontmatter(self):
        fm = {
                "slug": self.slug, 
                "title": self.title, 
                "tag_ids": self.tag_ids, 
                "posted_at": self.posted_at, 
                "updated_at": self.updated_at, 
                "description": self.description,
            }
        fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True)
        return fm

    def _format_markdown(self):
        return self.markdown

