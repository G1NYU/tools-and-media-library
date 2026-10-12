# Tools & Media Library

A public, anonymous resource directory built from the Sentai `#toolbox` Discord export. It is a static HTML/CSS/JS site designed for GitHub Pages.

## About the Discord files

Nothing is wrong with your JSON export. The limitation was this chat's attachment search reader: it could see the file exists but did not resolve its internal file ID, so it could not safely parse 3.4 MB of JSON here.

The TXT and HTML exports work well too. Use the HTML export if you want richer surrounding context, or TXT if you mainly want URLs and plain message text. The included parser currently accepts DiscordChatExporter JSON; use JSON locally because it preserves message authors, allowing the repeated-post **Ginyu’s Pick** rule to work accurately.

## Build public data

Keep all raw Discord exports out of Git history. Put the export next to this repository and run:

```bash
python scripts/build_links.py SENTAI-social-toolbox-446037106792595456.json --ginyu ginyu
```

This creates `data/links.json` with unique URLs, inferred categories, link context, and repeat-post picks. Review descriptions before committing because Discord context can be noisy.

## Refresh GitHub stars

Run this after generating the data:

```bash
python scripts/update_stars.py
```

It queries GitHub for every detected repository, writes each current `githubStars` count, and automatically marks a repository as **Ginyu’s Pick** at 1,000 stars. For much higher API limits, create a fine-grained GitHub token with read-only public metadata access and run:

```bash
GITHUB_TOKEN=your_token_here python scripts/update_stars.py
```

Never commit the token. The parser preserves a repeated-post pick even when a project has fewer than 1,000 stars.

## Publish

In GitHub: **Settings → Pages → Build and deployment → Deploy from a branch**, then select `main` and `/ (root)`. The directory will be published at `https://g1nyu.github.io/tools-and-media-library/`.
