#!/usr/bin/env python3
import argparse, json, re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

URL_RE = re.compile(r'https?://[^\s<>"`]+')
TRIM = '.,;:!?)\]}\'"'
GITHUB_RE = re.compile(r'^github\.com/([^/]+)/([^/?#]+)', re.I)

def category(url, text):
    s = (url + ' ' + text).lower()
    rules = [
        ('Anime & Manga', ('anilist','myanimelist','mangadex','manga','anime','anilist')),
        ('Streaming & Media', ('jellyfin','plex','stremio','stream','media','torrent')),
        ('Games', ('steam','itch.io','game','rom','emulator')),
        ('Development', ('github','gitlab','npmjs','developer','code','api')),
        ('AI', ('huggingface','openai','claude','gemini','llm','ai ')),
        ('Privacy & Downloads', ('vpn','privacy','download','archive.org','f-droid')),
        ('Design', ('figma','font','design','icon','color')),
    ]
    return next((name for name, words in rules if any(w in s for w in words)), 'Other')

def title_from_url(url):
    p=urlparse(url); path=p.path.strip('/').split('/')
    return ' / '.join(path[-2:]) if p.netloc=='github.com' and len(path)>=2 else p.netloc.removeprefix('www.')

def messages(data):
    if isinstance(data, list): return data
    for key in ('messages','channel','data'):
        if isinstance(data.get(key), list): return data[key]
    return []

def main():
    ap=argparse.ArgumentParser(description='Build anonymous public link data from a DiscordChatExporter JSON export.')
    ap.add_argument('input', help='DiscordChatExporter JSON file')
    ap.add_argument('-o','--output',default='data/links.json')
    ap.add_argument('--ginyu',default='ginyu',help='Discord display name or username to treat as Ginyu')
    args=ap.parse_args()
    raw=json.loads(Path(args.input).read_text(encoding='utf-8'))
    rows=[]
    for msg in messages(raw):
        text=msg.get('content','') or ''
        author=msg.get('author') or {}
        author_text=' '.join(str(author.get(k,'') or '') for k in ('name','nickname','displayName','username')).lower()
        for url in URL_RE.findall(text):
            url=url.rstrip(TRIM)
            if url: rows.append((url,text, args.ginyu.lower() in author_text))
    frequency=Counter(url for url,_,_ in rows)
    mine=Counter(url for url,_,me in rows if me)
    merged={}
    for url,text,is_mine in rows:
        if url not in merged:
            domain=urlparse(url).netloc.lower().removeprefix('www.')
            gh=GITHUB_RE.match(domain + urlparse(url).path)
            merged[url]={'url':url,'name':title_from_url(url),'description':text[:220].replace(url,'').strip(),'category':category(url,text),'domain':domain,'githubRepo':f'{gh.group(1)}/{gh.group(2)}' if gh else None,'githubStars':None,'pick':False}
        if not merged[url]['description'] and text: merged[url]['description']=text[:220].replace(url,'').strip()
    for url,item in merged.items():
        item['pick']=bool(item['githubRepo'] and mine[url]>=2)
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(json.dumps({'links':sorted(merged.values(),key=lambda x:(x['category'],x['name'].lower()))},ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Wrote {len(merged)} unique links to {args.output}. GitHub stars are filled by update_stars.py or manually.')
if __name__=='__main__': main()
