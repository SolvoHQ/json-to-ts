# JSON to TypeScript

Paste JSON, get TypeScript interfaces or types instantly. Zero signup, zero upload — runs entirely in your browser.

**Live:** https://json-to-ts-app.netlify.app/

![JSON to TypeScript — two-pane converter showing JSON on the left and generated TS interfaces on the right](code/og-image.png)

## Why this exists

Most "JSON to TypeScript" tools are buried inside multi-language code generators (quicktype, transform.tools, json2ts.com). They work, but the conversion you want is three clicks deep, the page is slow, and half the UI is irrelevant.

This is the opposite. One page, one job:

- **Focus** — JSON in, TypeScript out. Nothing else.
- **Speed** — live conversion as you type. No "Convert" button.
- **Long-tail SEO** — dedicated landing pages for the JSON shapes developers actually search for (Stripe webhooks, GitHub API responses, OpenAI chat completions, AWS Lambda events, JSON:API).

## Local development

There's no build step and no backend. Open the file:

```sh
open code/index.html
# or
python3 -m http.server -d code 8000
```

Everything is one self-contained HTML file with vanilla JS — no frameworks, no bundlers, no npm install.

## Repository layout

```
code/                                Live site root (deployed to Netlify)
  index.html                         The converter
  og-image.png                       Social preview image
  robots.txt, sitemap.xml            SEO basics
  <slug>/index.html                  Long-tail landing pages
tools/
  build_landing.py                   Generator for landing pages
  build_og_image.py                  Generator for og-image.png from og-image.svg
```

Adding a new long-tail landing page is one dict entry in `tools/build_landing.py` plus a redeploy.

## License

MIT — see [LICENSE](LICENSE).
