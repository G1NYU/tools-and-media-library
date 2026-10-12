#!/usr/bin/env python3
import argparse, json, re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse
URL_RE=re.compile(r'https?://[^\s<>"`]+');TRIM='.,;:!?)]}\'"';GITHUB_RE=re.compile(r'^github\.com/([^/]+)/([^/?#]+)',re.I)
def category(url,text):
 s=(url+' '+text).lower();rules=[('Anime & Manga',('anilist','myanimelist','mangadex','manga','anime')),('Streaming & Media',('jellyfin','plex','stremio','stream','media','torrent')),('Games',('steam','itch.io','game','rom','emulator')),('Development',('github','gitlab','npmjs','developer','code','api')),('AI',('huggingface','openai','claude','gemini','llm','ai ')),('Privacy & Downloads',('vpn','privacy','download','archive.org','f-droid')),('Design',('figma','font','design','icon','color'))];return next((n for n,w in rules if any(x in s for x in w)),'Other')
def name(url):
 p=urlparse(url);a=p.path.strip('/').split('/');return ' / '.join(a[-2:]) if p.netloc.lower().replace('www.','')=='github.com' and len(a)>=2 else p.netloc.lower().replace('www.','')
def rows_json(data,ginyu):
 ms=data if isinstance(data,list) else next((data.get(k) for k in ('messages','channel','data') if isinstance(data.get(k),list)),[])
 for m in ms:
  text=m.get('content','') or '';a=m.get('author') or {};who=' '.join(str(a.get(k,'') or '') for k in ('name','nickname','displayName','username')).lower()
  for u in URL_RE.findall(text):yield u.rstrip(TRIM),text,ginyu in who
def rows_txt(text):
 for u in URL_RE.findall(text):yield u.rstrip(TRIM),text[max(0,text.find(u)-120):text.find(u)+len(u)+120)],False
def main():
 ap=argparse.ArgumentParser();ap.add_argument('input');ap.add_argument('-o','--output',default='data/links.json');ap.add_argument('--ginyu',default='ginyu');a=ap.parse_args();p=Path(a.input);raw=p.read_text(encoding='utf-8');rows=rows_json(json.loads(raw),a.ginyu.lower()) if p.suffix.lower()=='.json' else rows_txt(raw);mine=Counter();items={}
 for u,t,me in rows:
  mine[u]+=me
  if u not in items:
   d=urlparse(u).netloc.lower().removeprefix('www.');g=GITHUB_RE.match(d+urlparse(u).path);items[u]={'url':u,'name':name(u),'description':t.replace(u,'').strip()[:220],'category':category(u,t),'domain':d,'githubRepo':f'{g.group(1)}/{g.group(2)}' if g else None,'githubStars':None,'pick':False}
 for u,x in items.items():x['pick']=bool(x['githubRepo'] and mine[u]>=2)
 Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps({'links':sorted(items.values(),key=lambda x:(x['category'],x['name'].lower()))},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
