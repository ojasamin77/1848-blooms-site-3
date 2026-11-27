# 1848 Blooms & Designs — site v3

Static site (HTML, CSS, vanilla JS). No build step needed to view: open `index.html`.

- `build.py` regenerates the pages (`python3 build.py`, needs Pillow).
- Fonts: Gilda Display (headings, free stand-in for Cammron Light), Questrial, Pinyon Script, Cormorant — embedded in `assets/site.css`.
- Placeholder copy is highlighted yellow (`.ph`). Replace designer name/story, contact details, social links (currently `#`), prices, FAQ and testimonials.
- Forms: set `FORM_ENDPOINT` in `assets/site.js` (e.g. Formspree). Empty = preview mode.
- Hosting: GitHub Pages → Settings → Pages → deploy from `main`, root.

## SEO

- Business details (email, phone, town, social links, Google Business Profile link) live in the `BIZ` block at the top of `build.py`. Fill them in and run `python3 build.py`: the footer, contact page and Google structured data (Florist JSON-LD) all update. Blank values stay as yellow placeholders and are left out of the structured data.
- `build.py` also writes `sitemap.xml`, `robots.txt` and `404.html` (which forwards old Shopify links like `/pages/contact` to the matching page), and 800px copies of photos in `assets/img/sm/` for phones.
- Canonical URLs, Open Graph images and the sitemap use `DOMAIN` (https://1848bloomsanddesigns.com/).
