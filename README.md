# Tools & Media Library

A public, anonymous resource directory built from the Sentai `#toolbox` Discord export. It is a static HTML/CSS/JS site designed for GitHub Pages.

## Build the public data

Keep the raw Discord export out of Git history. Run the parser locally:

```bash
python scripts/build_links.py SENTAI-social-toolbox-446037106792595456.json --ginyu ginyu
```

This creates `data/links.json` with unique URLs, inferred categories, link context, and Ginyu repeat-post picks. Review descriptions before committing because Discord context can be noisy.

## GitHub stars and picks

For GitHub entries, fill `githubStars` in `data/links.json` from the repository's current GitHub star count. A repository gets the **Ginyu’s Pick** badge when it has at least 1,000 stars or was posted by Ginyu at least twice. The included parser handles the repeat-post rule; apply the 1,000-star rule when refreshing star data.

## Publish

In GitHub: **Settings → Pages → Build and deployment → Deploy from a branch**, then select `main` and `/ (root)`. The directory will be published at `https://g1nyu.github.io/tools-and-media-library/`.
