# Tools & Media Library

A public, anonymous resource directory built from a Sentai `#toolbox` export. It is a static HTML/CSS/JS GitHub Pages site.

## No local setup needed

Use the deployed site’s **Import export** tab:

1. Choose the DiscordChatExporter `.json` or `.txt` file.
2. Enter your Discord name, `ginyu` by default.
3. Select **Build & fetch GitHub stars**.
4. Download the generated `links.json`.
5. On GitHub, open `data/links.json`, choose **Edit**, replace its contents with the downloaded file, then commit.

The import runs entirely in your browser. Your Discord export is never uploaded, stored, or committed. JSON is best because it preserves author data and can mark repositories you posted repeatedly as **Ginyu’s Pick**. TXT still extracts and organizes links but cannot reliably identify which posts were yours. GitHub projects at 1,000+ stars get **Ginyu’s Pick** automatically in either mode.

## Optional command line path

The scripts remain available if preferred:

```bash
python scripts/build_links.py SENTAI-social-toolbox-446037106792595456.json --ginyu ginyu
python scripts/update_stars.py
```

Keep raw Discord exports out of Git history.

## Publish

In GitHub: **Settings → Pages → Build and deployment → Deploy from a branch**, then select `main` and `/ (root)`. The directory will be published at `https://g1nyu.github.io/tools-and-media-library/`.
