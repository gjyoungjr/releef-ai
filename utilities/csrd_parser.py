import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from bs4.element import Tag


CSRD_REPORT_URL = 'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02013L0034-20240109&qid=1712714544806'
html_page = requests.get(CSRD_REPORT_URL).text


def get_directive_section(main_content):
  return main_content.find('div', {'class': 'eli-main-title'})

def get_content_section(main_content):
  return main_content.find('div', {'class': 'eli-subdivision'})

def get_chapter_sections(content_section):
  return content_section.find_all('div', recursive=False)

def get_article_sections(chapter_section):
  return chapter_section.find_all('div', {'class': 'eli-subdivision'}, recursive=False)

def get_directive_name(directive_section) -> str:
  title_doc = directive_section.find_all('p', {'class': 'title-doc-first'})
  title_doc = ' '.join([t.text.strip() for t in title_doc])
  return title_doc

def get_chapter_name(chapter_section) -> str:
  return chapter_section.find('p', {'class': 'title-division-2'}).text.strip().capitalize()

def get_chapter_id(chapter_section) -> str:
  chapter_id = chapter_section.find('p', {'class': 'title-division-1'}).text.strip()
  chapter_id = chapter_id.replace('CHAPTER', '').strip()
  return chapter_id

def get_article_name(article_section) -> str:
  return article_section.find('p', {'class': 'stitle-article-norm'}).text.strip()

def get_article_id(article_section) -> str:
  article_id = article_section.find('p', {'class': 'title-article-norm'}).text.strip()
  article_id = re.sub('\"?Article\s*', '', article_id).strip()
  return article_id


def _clean_paragraph(txt):
  # remove multiple break lines
  txt = re.sub('\n+', '\n', txt)
  # simplifies bullet points
  txt = re.sub('(\([\d\w]+\)\s?)\n', r'\1\t', txt)
  # simplifies quote
  txt = re.sub('‘', '\'', txt)
  # some weird references to other articles
  txt = re.sub('\(\\n[\d\w]+\n\)', '', txt)
  # remove spaces before punctuation
  txt = re.sub(f'\s([\.;:])', r'\1', txt)
  # remove reference links
  txt = re.sub('▼\w+\n', '', txt)
  # format numbers
  txt = re.sub('(?<=\d)\s(?=\d)', '', txt)
  # remove consecutive spaces
  txt = re.sub('\s{2,}', ' ', txt)
  # remove leading / trailing spaces
  txt = txt.strip()
  return txt 

def get_paragraphs(article_section):
  content = {}
  paragraph_number = '0'
  paragraph_content = []
  for child in article_section.children:
    if isinstance(child, Tag):
      if 'norm' in child.attrs.get('class'):
        if child.name == 'p':
          paragraph_content.append(child.text.strip())
        elif child.name == 'div':
          content[paragraph_number] = _clean_paragraph('\n'.join(paragraph_content))
          paragraph_number = child.find('span', {'class': 'no-parag'}).text.strip().split('.')[0]
          paragraph_content = [child.find('div', {'class': 'inline-element'}).text]
      elif 'grid-container' in child.attrs.get('class'):
        paragraph_content.append(child.text)
    content[paragraph_number] = _clean_paragraph('\n'.join(paragraph_content))
  return {k:v for k, v in content.items() if len(v) > 0}



main_content = BeautifulSoup(html_page, 'html.parser')
directive_section = get_directive_section(main_content)
directive_name = get_directive_name(directive_section)
content_section = get_content_section(main_content)

for chapter_section in get_chapter_sections(content_section):
  chapter_id = get_chapter_id(chapter_section)
  chapter_name = get_chapter_name(chapter_section)
  articles = len(get_article_sections(chapter_section))
  print(f'Chapter {chapter_id}: {chapter_name}')
  print(f'{articles} article(s)')
  print('')
  
  
nodes = []
edges = []

nodes.append(['0', 'CSRD', directive_name, 'DIRECTIVE'])


for chapter_section in get_chapter_sections(content_section):

  chapter_id = get_chapter_id(chapter_section)
  chapter_name = get_chapter_name(chapter_section)

  # level 1, chapter
  # chapters are included in root node
  nodes.append([ chapter_id, f'Chapter {chapter_id}', chapter_name, 'CHAPTER'])
  edges.append(['0', f'{chapter_id}', 'CONTAINS'])

  for article_section in get_article_sections(chapter_section):
    article_id = get_article_id(article_section)
    article_name = get_article_name(article_section)
    article_paragraphs = get_paragraphs(article_section)

    # level 2, article
    # articles are included in chapters
    nodes.append([f'{chapter_id}.{article_id}', f'Article {article_id}', article_name, 'ARTICLE'])
    edges.append([chapter_id, f'{chapter_id}.{article_id}', 'CONTAINS'])

    for paragraph_id, paragraph_text in article_paragraphs.items():

      # level 3, paragraph
      # paragraphs are included in articles
      nodes.append([f'{chapter_id}.{article_id}.{paragraph_id}', f'Article {article_id}({paragraph_id})', paragraph_text, 'PARAGRAPH'])
      edges.append([f'{chapter_id}.{article_id}', f'{chapter_id}.{article_id}.{paragraph_id}', 'CONTAINS'])
      

nodes_df = pd.DataFrame(nodes, columns=['id', 'label', 'content', 'group'])
edges_df = pd.DataFrame(edges, columns=['src', 'dst', 'label'])


print(nodes_df)