#!/usr/bin/env python3
import argparse, json, os, time
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

API = 'https://api.github.com/repos/'

def get_repo(repo, token):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'tools-and-media-library'}
    if token: headers['Authorization'] = f'Bearer {token}'
    req = Request(API + repo, headers=headers)
    with urlopen(req, timeout=20) as response:
        return json.load(response)

def main():
    ap = argparse.ArgumentParser(description='Refresh GitHub stars and automatic Ginyu’s Pick badges.')
    ap.add_argument('-i', '--input', default='data/links.json')
    ap.add_argument('--delay', type=float, default=.25, help='Seconds between API requests')
    args = ap.parse_args()
    path = Path(args.input)
    data = json.loads(path.read_text(encoding='utf-8'))
    token = os.getenv('GITHUB_TOKEN')
    updated = failed = 0
    for item in data.get('links', []):
        repo = item.get('githubRepo')
        if not repo:
            continue
        try:
            metadata = get_repo(repo, token)
            item['githubStars'] = metadata.get('stargazers_count', 0)
            if item['githubStars'] >= 1000:
                item['pick'] = True
            updated += 1
            print(f"{repo}: ★ {item['githubStars']}")
        except HTTPError as error:
            failed += 1
            print(f'{repo}: GitHub returned HTTP {error.code}; keeping existing data')
        except Exception as error:
            failed += 1
            print(f'{repo}: {error}; keeping existing data')
        time.sleep(args.delay)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Updated {updated} GitHub projects; {failed} failed.')
    if not token:
        print('Tip: set GITHUB_TOKEN for GitHub API rate limits higher than the unauthenticated allowance.')

if __name__ == '__main__':
    main()
