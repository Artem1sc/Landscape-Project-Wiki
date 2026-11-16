"""Convert approved Markdown/YAML Wiki pages into a dependency-free static site.

Run from any directory: python3 scripts/build_site.py
The `wiki/` directory remains the single editorial source of truth.
"""
from __future__ import annotations
from pathlib import Path
import json, re, html, sys
import yaml
import mistune
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
WIKI=ROOT/'wiki'; OUT=ROOT/'docs'; OUT.mkdir(exist_ok=True)
md=mistune.create_markdown(escape=True, plugins=['table'])
PROJECT_TYPE={
 'parks-open-spaces':'公園與開放綠地','streets-public-realm':'街道與公共空間',
 'waterfront-blue-infrastructure':'水岸與藍色基礎設施','ecological-landscapes':'生態景觀',
 'residential-commercial':'住宅與商業景觀','institutional':'校園與公共機構',
 'heritage-regeneration':'文化保存與再生','regional-infrastructure':'區域與基礎設施'}
SCALE={'micro':'微型','site':'基地','neighborhood':'街廓／社區','urban':'都市','regional':'區域／流域'}
STRATEGY={
 'stormwater-management':'雨洪管理','ecological-restoration':'生態修復','topographic-design':'地形操作',
 'climate-adaptation':'氣候調適','urban-connectivity':'都市縫合','cultural-heritage':'文化保存',
 'material-reuse':'材料再利用','community-participation':'公共參與',
 'multifunctional-space':'多功能空間','low-impact-development':'低衝擊開發'}
STAGE={'completed':'已完工','construction':'施工中','planning':'規劃中','competition':'競圖','unbuilt':'未實現','unknown':'未查得'}

def read_doc(path):
 raw=path.read_text(encoding='utf-8')
 match=re.match(r'^---\n(.*?)\n---\n?',raw,re.S)
 if not match: raise ValueError(f'Missing YAML front matter: {path}')
 return yaml.safe_load(match.group(1)), raw[match.end():]

sources={}
for path in sorted((ROOT/'raw'/'sources').glob('**/SRC-*.md')):
 attrs,body=read_doc(path)
 sid=attrs['id']; assert sid not in sources, f'Duplicate source: {sid}'
 sources[sid]={k:attrs.get(k) for k in ['id','case_slug','title','author_or_organization','url','language','source_type','published_date','accessed_date','reproduction_permission']}
 assert str(attrs.get('url','')).startswith('https://'), f'Bad source url in {path}'

def convert_markdown(txt):
 markup=md(txt)
 soup=BeautifulSoup(markup,'html.parser')
 for link in soup.find_all('a',href=True):
  href=link['href']; m=re.search(r'(?:^|/)([A-Za-z0-9-]+)\.md$',href)
  if not m: continue
  slug=m.group(1)
  if '/sources/' in href:
   sid=slug; link['href']=sources.get(sid,{}).get('url','#')
   link['target']='_blank'; link['rel']='noopener noreferrer'
  elif '/strategies/' in href: link['href']=f'strategy.html?id={slug}'
  elif '/cases/' in href or href.startswith('./'): link['href']=f'case.html?id={slug}'
 # Convert bracketed source references into hyperlinks (only whitelisted source IDs).
 for node in list(soup.find_all(string=True)):
  if not re.search(r'\[SRC-[\w-]+\]',str(node)): continue
  fragments=[]; start=0; src=str(node)
  for match in re.finditer(r'\[(SRC-[\w-]+)\]',src):
   if match.start()>start: fragments.append(src[start:match.start()])
   sid=match.group(1)
   if sid in sources:
    el=soup.new_tag('a',href=sources[sid]['url'],target='_blank',rel='noopener noreferrer')
    el['class']='source-ref'; el['title']=sources[sid]['title']; el.string=f'↗ {sid.split("-")[-1]}'
    fragments.append(el)
   else: fragments.append(match.group(0))
   start=match.end()
  fragments.append(src[start:])
  for piece in fragments: node.insert_before(piece)
  node.extract()
 # Security hardening for any external source links.
 for link in soup.find_all('a',href=True):
  if str(link['href']).startswith('http'):
   link['target']='_blank'; link['rel']='noopener noreferrer'
 return str(soup)

def sections_from(body,mode='case'):
 if mode=='case':
  pattern=r'(?m)^## (0[1-6]) ([^\n]+)\n'
  found=list(re.finditer(pattern,body))
  if len(found)!=6: raise ValueError(f'Expected 6 case sections, found {len(found)}')
  out=[]
  for i,m in enumerate(found):
   end=found[i+1].start() if i+1<len(found) else len(body)
   chunk=body[m.end():end]
   if i==5: chunk=re.split(r'(?m)^## (?:圖像|來源)',chunk)[0]
   heading=m.group(2).split('｜')
   out.append({'number':m.group(1),'title_en':heading[0].strip(),'title_zh':(heading[-1].strip() if len(heading)>1 else heading[0].strip()),'html':convert_markdown(chunk)})
  return out
 # Strategy sections: preserve the content, not review-only banner.
 content=re.sub(r'(?m)^> \*\*Wiki 狀態[^\n]+\n','',body)
 content=re.sub(r'(?m)^# [^\n]+\n','',content,count=1)
 return convert_markdown(content)

cases=[]
for path in sorted((WIKI/'cases').glob('*.md')):
 attrs,body=read_doc(path)
 if attrs.get('status')!='published': continue
 cid=attrs['id']; assert path.stem==cid
 assert all(s in sources for s in attrs.get('source_ids',[])),cid+' missing source'
 for key in attrs.get('project_types',[]): assert key in PROJECT_TYPE,(cid,key)
 for key in attrs.get('strategy_tags',[]): assert key in STRATEGY,(cid,key)
 for key in attrs.get('spatial_scale',[]): assert key in SCALE,(cid,key)
 cases.append({**attrs,'sections':sections_from(body),'cover':attrs.get('hero_image') or {},
               'description':re.sub(r'\[[^\]]*\]','',re.sub(r'\*\*','', re.search(r'## 01 Background & Context｜專案背景\n\n(.*?)(?:\n\n|\n##)',body,re.S).group(1))).strip()[:185]})
case_ids={c['id'] for c in cases}
for c in cases:
 for rel in c.get('related_cases',[]): assert rel in case_ids, f"Bad related case: {rel}"

strategies=[]
for path in sorted((WIKI/'strategies').glob('*.md')):
 attrs,body=read_doc(path)
 if attrs.get('status')!='published': continue
 assert path.stem==attrs['id']
 assert all(cid in case_ids for cid in attrs.get('related_cases',[]))
 strategies.append({**attrs,'html':sections_from(body,'strategy')})

data={'cases':cases,'strategies':strategies,'sources':sources,
      'vocab':{'project_types':PROJECT_TYPE,'spatial_scale':SCALE,'strategy_tags':STRATEGY,'project_stage':STAGE},
      'updated':'2026-11-16','data_origin':'wiki/ Markdown and raw/sources/ YAML'}
js='window.LANDSCAPE_WIKI_DATA = '+json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+';\n'
(OUT/'assets'/'data.js').write_text(js,encoding='utf-8')
print(f"Built docs/assets/data.js from {len(cases)} approved cases, {len(strategies)} strategies, {len(sources)} source records")
