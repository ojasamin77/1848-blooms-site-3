#!/usr/bin/env python3
"""Generates the static pages for 1848 Blooms & Designs, plus sitemap.xml, robots.txt and 404.html.
Run: python3 build.py (needs Pillow)."""
import os, html, json, datetime
from PIL import Image

OUT = os.path.dirname(os.path.abspath(__file__))
IMG = OUT + '/assets/img'
SITE = '1848 Blooms & Designs'
_d = {}

# ---------- business details (used in page text, footer, contact page and Google structured data) ----------
# Fill in the blanks and run `python3 build.py`. Empty values show the yellow placeholder on the page and
# are left out of the structured data, so nothing made-up reaches Google.
DOMAIN = 'https://1848bloomsanddesigns.com/'
BIZ = {
    'email': '',          # e.g. hello@1848bloomsanddesigns.com
    'phone': '',          # e.g. +1-302-555-0100 (use the same number as the Google Business Profile)
    'town': '',           # the town the studio is based in, e.g. "Wilmington"
    'state': 'DE',        # two-letter state of the studio
    'street': '',         # only if the studio address is shown on the Google Business Profile
    'postal': '',
    'instagram': '',      # full profile URLs
    'facebook': '',
    'pinterest': '',
    'google': '',         # the Google Business Profile / Maps link
}
AREA = 'Delaware and Philadelphia'
# Towns named in page copy and in the structured data (from Jonas, Nov 2026)
TOWNS = 'Greenville, Philadelphia, New Hope'
AREA_LONG = 'Delaware, Greenville, Philadelphia, New Hope and the surrounding areas'
TODAY = datetime.date.today().isoformat()
PAGES = []   # (filename, noindex) for the sitemap


def ph(key, fallback):
    """The real value if filled in, otherwise the yellow placeholder."""
    v = BIZ.get(key)
    return html.escape(v) if v else f'<span class="ph">{fallback}</span>'


def email_link():
    e = BIZ['email']
    return f'<a class="link" href="mailto:{html.escape(e)}">{html.escape(e)}</a>' if e else '<span class="ph">[hello@yourdomain.com]</span>'


def phone_link():
    t = BIZ['phone']
    return f'<a class="link" href="tel:{html.escape(t.replace(" ", ""))}">{html.escape(t)}</a>' if t else '<span class="ph">[Phone number]</span>'


def dims(n):
    if n not in _d:
        with Image.open(f'{IMG}/{n}.jpg') as i:
            _d[n] = i.size
    return _d[n]


SM = 800  # width of the smaller copy served to phones and small slots


def small(n):
    """Make assets/img/sm/<n>.jpg (800px wide) once, for srcset. Returns its width, or None if not needed."""
    w, h = dims(n)
    if w <= SM * 1.2:
        return None
    dst = f'{IMG}/sm/{n}.jpg'
    if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(f'{IMG}/{n}.jpg'):
        os.makedirs(f'{IMG}/sm', exist_ok=True)
        with Image.open(f'{IMG}/{n}.jpg') as i:
            i.convert('RGB').resize((SM, round(h * SM / w)), Image.LANCZOS).save(dst, 'JPEG', quality=80, optimize=True, progressive=True)
    return SM


def im(n, alt, cls='', eager=False, extra='', sizes='(max-width: 900px) 100vw, 50vw'):
    w, h = dims(n)
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ''
    sw = small(n)
    ss = f' srcset="assets/img/sm/{n}.jpg {sw}w, assets/img/{n}.jpg {w}w" sizes="{sizes}"' if sw else ''
    return f'<img{c} src="assets/img/{n}.jpg"{ss} width="{w}" height="{h}" alt="{html.escape(alt)}" {load} {extra}>'


def ratio(n):
    w, h = dims(n)
    return round(w / h, 3)



NAV = [('index.html','Home'),('weddings.html','Weddings'),('about.html','About'),('services.html','Services'),('floral-bar.html','Floral Bar'),
       ('portfolio.html','Portfolio'),('experiences.html','Experiences'),('contact.html','Contact')]
MNAV = [('index.html','Home'),('weddings.html','Weddings'),('about.html','About'),('designer.html','Meet the designer'),('services.html','Services'),('floral-bar.html','Floral Bar'),('portfolio.html','Portfolio'),('experiences.html','Experiences'),('reserve.html','Reserve your spot'),('contact.html','Contact')]
# small copy of the logo for the header and footer (the full file is 700px wide but shows at 86px)
if not os.path.exists(f'{OUT}/assets/logo-sm.png') or os.path.getmtime(f'{OUT}/assets/logo-sm.png') < os.path.getmtime(f'{OUT}/assets/logo.png'):
    with Image.open(f'{OUT}/assets/logo.png') as _l:
        _l.resize((172, 153), Image.LANCZOS).save(f'{OUT}/assets/logo-sm.png', optimize=True)
LOGO = '<a class="brand" href="index.html" aria-label="1848 Blooms &amp; Designs, home"><img src="assets/logo-sm.png" width="86" height="76" alt="1848 Blooms &amp; Designs"></a>'
SOC = ('<span class="social">'
       f'<a href="{BIZ["pinterest"] or "#"}" aria-label="Pinterest"' + (' rel="noopener" target="_blank"' if BIZ['pinterest'] else '') + '><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.2 2C6.9 2 4.2 5.600 4.2 8.900c0 2 .8 3.800 2.400 4.400.3.100.5 0 .6-.3l.2-.9c.1-.3 0-.4-.2-.6-.5-.6-.8-1.300-.8-2.300 0-3 2.200-5.700 5.800-5.700 3.200 0 4.900 2 4.900 4.500 0 3.400-1.500 6.200-3.700 6.200-1.200 0-2.100-1-1.800-2.200.3-1.500 1-3.100 1-4.200 0-1-.5-1.800-1.600-1.800-1.300 0-2.300 1.300-2.300 3.100 0 1.100.4 1.900.4 1.900l-1.500 6.400c-.4 1.800-.1 4.200 0 4.400 0 .1.200.2.300.1.100-.2 1.800-2.200 2.300-4.200l.9-3.500c.5.900 1.800 1.600 3.200 1.600 4.200 0 7-3.800 7-8.900C20.200 5 17 2 12.200 2z"/></svg></a>'
       f'<a href="{BIZ["instagram"] or "#"}" aria-label="Instagram"' + (' rel="noopener" target="_blank"' if BIZ['instagram'] else '') + '><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="3.500" y="3.500" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.200" cy="6.800" r=".6" fill="currentColor"/></svg></a>'
       f'<a href="{BIZ["facebook"] or "#"}" aria-label="Facebook"' + (' rel="noopener" target="_blank"' if BIZ['facebook'] else '') + '><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.500 21v-7.500h2.500l.4-3h-2.900V8.600c0-.9.3-1.500 1.500-1.500h1.500V4.400c-.3 0-1.200-.1-2.200-.1-2.200 0-3.700 1.300-3.700 3.800v2.400H7.800v3h2.800V21h2.900z"/></svg></a>'
       '</span>')


def header(cur):
    links = ''.join(f'<a href="{h}"' + (' aria-current="page"' if h == cur else '') + f'>{t}</a>' for h, t in NAV)
    m = ''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in MNAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hd"><div class="hd__top">
  <p class="flank hd__tag">Delaware + Philadelphia<br>floral designer</p>
  {LOGO}
  <div class="hd__right">{SOC}<a class="contact-link" href="contact.html">Contact</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mnav"><i aria-hidden="true"></i><span>Menu</span></button></div>
</div></header>
<nav class="primary" aria-label="Main">{links}</nav>
<nav class="mnav" id="mnav" aria-label="Menu">
  <ul>{m}</ul>
  <div class="foot-line"><span>Serving Delaware, Philadelphia + New Hope</span><span>Now booking 2026</span></div>
</nav>'''


def footer():
    follow = (f'<a class="btn" href="{html.escape(BIZ["instagram"])}" rel="noopener" target="_blank">Follow on Instagram</a>'
              if BIZ['instagram'] else '<a class="btn" href="#"><span class="ph">Follow @yourhandle</span></a>')
    thumbs = ''.join(im(n, a, sizes='(max-width: 560px) 33vw, 20vw') for n, a in [('arch-willow','A wooden wedding arch with white flowers'),('pastel-table-a','A pastel event table with a tall floral arrangement'),('bouquet-ribbon','A pastel bridal bouquet with a rust ribbon'),('bridesmaids','Bridesmaids holding white bouquets'),('ladder-daisies','Daisies in a woven basket')])
    return f'''<footer class="site-footer">
  <div class="f-top">{LOGO}<div class="hd__right">{SOC}<a class="contact-link" href="contact.html">Contact</a></div></div>
  <div class="f-mid">
    <ul><li><a href="index.html">Home</a></li><li><a href="weddings.html">Weddings</a></li><li><a href="about.html">About</a></li><li><a href="designer.html">Meet the designer</a></li><li><a href="portfolio.html">Portfolio</a></li></ul>
    <ul><li><a href="services.html">Services</a></li><li><a href="floral-bar.html">Floral Bar</a></li><li><a href="experiences.html">Experiences</a></li><li><a href="reserve.html">Reserve your spot</a></li></ul>
    <div class="f-btns"><a class="btn" href="reserve.html">Reserve your spot</a>{follow}
      <p class="f-note">{email_link()} &middot; {phone_link()}</p></div>
  </div>
  <div class="f-thumbs">{thumbs}</div>
  <div class="legal"><span>&copy; <span data-year>2026</span> 1848 Blooms &amp; Designs</span><span>Wedding and event florist serving Delaware, Greenville, Philadelphia, New Hope and the surrounding areas &middot; Now booking 2026</span></div>
</footer>'''


DE = {'@type': 'State', 'name': 'Delaware'}
PA = {'@type': 'State', 'name': 'Pennsylvania'}
AREAS = [DE, {'@type': 'City', 'name': 'Greenville', 'containedInPlace': DE},
         {'@type': 'City', 'name': 'Philadelphia', 'containedInPlace': PA},
         {'@type': 'City', 'name': 'New Hope', 'containedInPlace': PA}]


def florist():
    """schema.org Florist for Google. Only details that are filled in above are included."""
    d = {
        '@context': 'https://schema.org', '@type': 'Florist', '@id': DOMAIN + '#business',
        'name': SITE, 'url': DOMAIN, 'logo': DOMAIN + 'assets/logo.png',
        'image': [DOMAIN + f'assets/img/{n}.jpg' for n in ('home-banner', 'kiss-arch', 'bouquet-bright')],
        'description': 'Wedding and event florist serving Delaware, Greenville, Philadelphia, New Hope and the surrounding areas, plus hands-on floral workshops and the Floral Bar.',
        'areaServed': AREAS,
        'knowsAbout': ['Wedding flowers', 'Bridal bouquets', 'Ceremony arches', 'Event florals', 'Floral installations', 'Floral workshops'],
    }
    if BIZ['email']: d['email'] = BIZ['email']
    if BIZ['phone']: d['telephone'] = BIZ['phone']
    if BIZ['town']:
        a = {'@type': 'PostalAddress', 'addressLocality': BIZ['town'], 'addressRegion': BIZ['state'], 'addressCountry': 'US'}
        if BIZ['street']: a['streetAddress'] = BIZ['street']
        if BIZ['postal']: a['postalCode'] = BIZ['postal']
        d['address'] = a
    same = [BIZ[k] for k in ('instagram', 'facebook', 'pinterest', 'google') if BIZ[k]]
    if same: d['sameAs'] = same
    if BIZ['email'] or BIZ['phone']:
        d['contactPoint'] = {'@type': 'ContactPoint', 'contactType': 'Wedding and event inquiries', 'areaServed': 'US-DE',
                             **({'email': BIZ['email']} if BIZ['email'] else {}), **({'telephone': BIZ['phone']} if BIZ['phone'] else {})}
    return d


def ld(*objs):
    return ''.join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>\n' for o in objs)


def page(fname, title, desc, body, noindex=False, og='home-banner', schema=(), full_title=None):
    robots = '<meta name="robots" content="noindex">' if noindex else ''
    t = full_title or (SITE if fname == 'index.html' else f'{title} | {SITE}')
    url = DOMAIN if fname == 'index.html' else DOMAIN + fname
    ow, oh = dims(og)
    PAGES.append((fname, noindex))
    crumbs = [] if fname == 'index.html' or noindex else [{'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': DOMAIN},
        {'@type': 'ListItem', 'position': 2, 'name': title, 'item': url}]}]
    data = '' if noindex else ld(*schema, *crumbs)
    hero = body.find('fetchpriority="high"')
    pre = ''
    if hero != -1:  # let the browser start the hero photo before the CSS finishes
        tag = body[body.rfind('<img', 0, hero):hero]
        src = tag.split('src="', 1)[1].split('"', 1)[0]
        ss = f' imagesrcset="{tag.split("srcset=\"", 1)[1].split("\"", 1)[0]}" imagesizes="{tag.split("sizes=\"", 1)[1].split("\"", 1)[0]}"' if 'srcset="' in tag else ''
        pre = f'<link rel="preload" as="image" href="{src}"{ss} fetchpriority="high">'
    open(f'{OUT}/{fname}', 'w').write(f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(t)}</title>
<meta name="description" content="{html.escape(desc)}">
{robots}
{'' if noindex else f'<link rel="canonical" href="{url}">'}
<meta property="og:site_name" content="{html.escape(SITE)}">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{html.escape(t)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}assets/img/{og}.jpg">
<meta property="og:image:width" content="{ow}">
<meta property="og:image:height" content="{oh}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#C5A193">
<link rel="icon" type="image/png" href="assets/favicon.png">
<link rel="apple-touch-icon" href="assets/favicon.png">
{pre}
<link rel="stylesheet" href="assets/site.css?v=3">
{data}</head>
<body>
{header(fname)}
<main id="main">
{body}
</main>
{footer()}
<script src="assets/site.js"></script>
</body>
</html>
''')


# ---------- components ----------
def tbar(title, left, right, tag='h2', cls='dsp'):
    return f'<div class="tbar"><{tag} class="{cls}">{title}</{tag}></div>'


def phero(img, alt, title, left, right, lede, btn=None, plain=False):
    b = f'<div class="btn-row">{btn}</div>' if btn else ''
    bg = '' if plain else im(img, alt, 'phero__img', eager=True, sizes='100vw')
    cls = 'phero phero--plain' if plain else 'phero'
    eb = f'<span class="eyebrow">{left.replace("<br>", " ")} &middot; {right.replace("<br>", " ")}</span>'
    return f'''<section class="{cls}">
  {bg}
  <div class="phero__mid">{eb}{tbar(title, left, right, 'h1')}</div>
  <div class="phero__foot"><p>{lede}</p>{b}</div>
</section>'''


def closer(title='Let\u2019s design something unforgettable.', btn='Inquire now', href='contact.html', band='band-petal'):
    return f'''<section class="section {band}"><div class="wrap closer">
  <h2 class="dsp">{title}</h2><div class="btn-row"><a class="btn btn--arrow" href="{href}">{btn}</a></div>
</div></section>'''


# ================================================================== HOME
rail_imgs = ['table-window','bridesmaids','bouquet-bright','couple-window','pastel-table-a','arch-pampas','bouquet-chair','installation-hanging','tablescape-citrus','bouquet-ribbon']
rail_alt = {
    'table-window': 'A bright table by a window with a centerpiece of yellow and orange flowers',
    'bridesmaids': 'Bridesmaids in lavender dresses holding white bouquets on a brick patio',
    'bouquet-bright': 'A bright bridal bouquet of yellow, coral and blush flowers held against a white dress',
    'couple-window': 'A bride and groom sharing a quiet moment at a window, her bouquet in hand',
    'pastel-table-a': 'A pink and cream event table with a tall pastel arrangement and a taper candle',
    'arch-pampas': 'A wooden triangle ceremony arch dressed with pampas grass and dried flowers',
    'bouquet-chair': 'A pink and blue bouquet with a pale blue ribbon resting on a wooden chair',
    'installation-hanging': 'A long hanging floral installation of pink, magenta and white flowers',
    'tablescape-citrus': 'A centerpiece of orange roses and yellow blooms on a linen-covered table',
    'bouquet-ribbon': 'A pastel and coral bouquet tied with a rust-colored ribbon',
}
RAIL = ''.join(f'<figure style="--ar:{round(dims(n)[0]/dims(n)[1],3)}">{im(n, rail_alt[n], sizes="(max-width: 560px) 68vw, (max-width: 1450px) 29vw, 420px")}</figure>' for n in rail_imgs)

home = f'''
<section class="hero">
  {im('home-banner', 'A long white table set with candles, glassware and a low arrangement of yellow, peach and white flowers beside a window', 'hero__img', eager=True, sizes='100vw')}
  <div class="hero__body">
    <span class="eyebrow">Delaware, Philadelphia + New Hope &middot; Now booking 2026</span>
    <h1>Wedding and event florals that lead with <span class="script">atmosphere.</span></h1>
    <div class="btn-row">
      <a class="btn btn--arrow" href="weddings.html">Weddings</a>
      <a class="btn btn--arrow" href="services.html#events">Events</a>
      <a class="btn btn--arrow" href="experiences.html">Experiences + Floral Bar</a>
    </div>
  </div>
  <span class="scroll-cue" aria-hidden="true">Scroll to begin</span>
</section>

<section class="intro">
  <div class="wrap">
    <h2 class="dsp">Thoughtful design. Intentional details. Unforgettable moments.</h2>
    <span class="rule"></span>
    <p>We design florals for weddings, private events and hands-on gatherings across Delaware, Greenville, Philadelphia, New Hope and the surrounding areas. Each one starts with the room, the season and the people who will fill it, then gets built stem by stem.</p>
    <div class="btn-row"><a class="btn" href="services.html">Explore offerings</a><a class="btn btn--ghost" href="contact.html">Check your date</a></div>
  </div>
</section>

<section class="rail-wrap" aria-label="Recent work">
  <div class="rail" data-rail>{RAIL}</div>
  <div class="rail-ctl"><button type="button" class="prev" data-prev><i></i>Previous</button><button type="button" class="next" data-next>Next<i></i></button></div>
</section>

<section class="bio">
  <div class="bio__img">{im('designer-smile', 'The designer smiling in a beige apron, holding a bouquet of white, yellow and orange flowers')}</div>
  <div class="bio__card">
    <span class="eyebrow">Meet the designer</span>
    <h2 class="dsp"><span class="ph">[Designer name]</span></h2>
    <span class="rule"></span>
    <p class="ph">[Two or three lines in her voice: how long she has designed, what her process feels like, what clients say about working with her.]</p>
    <a class="arrow-link" href="designer.html">Learn more</a>
  </div>
</section>

<section class="feature">
  {im('table-long-pastel', 'A long white table set with pastel centerpieces and wishbone chairs in a bright room', sizes='100vw')}
  <div class="feature__card">
    <h2 class="dsp">Weddings + events</h2>
    <p>We take on a limited number of weddings and events each season so every client gets our full creative focus. Our full-service design covers every touchpoint, from personal flowers to installations, and we deliver and set up everything.</p>
    <div class="btn-row btn-row--center" style="margin-top:0"><a class="btn" href="weddings.html">Wedding florals</a><a class="btn btn--ghost" href="services.html#events">Event florals</a></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2 class="dsp" style="text-align:center">Floral experiences</h2>
    <p class="sec-intro">From hands-on workshops to private gatherings and the Floral Bar, our experiences are designed to inspire creativity, connection and a deeper appreciation for the beauty in everyday moments.</p>
    <div class="cards">
      <figure><a href="experiences.html"><div class="ph-img">{im('designing-table', 'A florist arranging yellow and white flowers at a table in a bright room', '', extra='style="object-position:70% 50%"', sizes='(max-width: 860px) 100vw, 33vw')}</div><h3>Workshops</h3></a><figcaption><p>Learn a designer’s techniques in a small class and leave with your own arrangement.</p></figcaption></figure>
      <figure><a href="experiences.html"><div class="ph-img">{im('designer-making', 'A designer arranging flowers in white bowls at a wooden table', '', extra='style="object-position:30% 50%"', sizes='(max-width: 860px) 100vw, 33vw')}</div><h3>Private gatherings</h3></a><figcaption><p>Bring the workshop to your group for a shower, a birthday or a team day.</p></figcaption></figure>
      <figure><a href="floral-bar.html"><div class="ph-img">{im('ladder-daisies', 'Daisies and cosmos in a woven basket at the foot of a wooden ladder', sizes='(max-width: 860px) 100vw, 33vw')}</div><h3>The Floral Bar</h3></a><figcaption><p>A self-serve flower station for your event. Pick, arrange, take home.</p></figcaption></figure>
    </div>
    <div class="btn-row btn-row--center" style="margin-top:clamp(2.2rem,4vw,3.6rem)"><a class="btn" href="reserve.html">Reserve your spot</a></div>
  </div>
</section>

<section class="section band-paper2">
  <div class="wrap">
    <h2 class="dsp" style="text-align:center;margin-bottom:clamp(2rem,4vw,3.5rem)">Kind words</h2>
    <div class="rev">
      <figure class="rc"><span class="src"><span class="ph">[Source]</span></span><blockquote class="ph">[Client quote about their wedding or event.]</blockquote><cite class="ph">[Client name]</cite></figure>
      <figure class="rc"><span class="src"><span class="ph">[Source]</span></span><blockquote class="ph">[Client quote about working with the designer.]</blockquote><cite class="ph">[Client name]</cite></figure>
      <figure class="rc"><span class="src"><span class="ph">[Source]</span></span><blockquote class="ph">[Client quote about a workshop or the Floral Bar.]</blockquote><cite class="ph">[Client name]</cite></figure>
    </div>
  </div>
</section>

<section class="closing">
  {im('centerpiece-wide-b', 'A wide reception table with a lush centerpiece of roses, pampas and greenery', sizes='100vw')}
  <div><span class="script">Let’s design florals they’ll remember.</span><a class="btn btn--cream btn--arrow" href="contact.html">Inquire now</a></div>
</section>
'''
page('index.html', 'Home',
     'Wedding and event florist serving Delaware, Greenville, Philadelphia and New Hope. Bouquets, ceremony and reception florals and installations. Check your date.',
     home, schema=[florist(), {'@context': 'https://schema.org', '@type': 'WebSite', 'name': SITE, 'url': DOMAIN}],
     full_title='Wedding & Event Florist in Delaware & Philadelphia | 1848 Blooms')

# ================================================================== ABOUT
about = f'''
{phero('table-long-pastel', 'A long white table set with pastel centerpieces and wishbone chairs in a bright room', 'About 1848', 'Delaware<br>and Philadelphia', 'Floral<br>design studio',
       '1848 Blooms &amp; Designs creates florals for weddings and events, and teaches hands-on floral experiences.')}

<section class="section band-moss">
  <div class="wrap">
    {tbar('How we design', 'Our approach', 'In three parts')}
    <div class="principles" style="margin-top:clamp(2.5rem,5vw,4.5rem)">
      <div><h3>Thoughtful design</h3><p>We begin with questions about the space, the season and how you want people to feel. The flowers follow from the answers, never from a template.</p></div>
      <div><h3>Intentional details</h3><p>A ribbon color, a stem height, the way a bouquet sits in the hand. We decide each one on purpose, and we check them against each other.</p></div>
      <div><h3>Unforgettable moments</h3><p>Good florals do their work quietly. They become the thing guests mention afterward, without ever getting in the way of the day.</p></div>
    </div>
  </div>
</section>

<section class="full-img">{im('table-window', 'A bright table by a window set with glassware and a centerpiece of yellow and orange flowers', extra='style="object-position:50% 70%"', sizes='100vw')}</section>

<section class="section">
  <div class="wrap split split--top split--57">
    <div class="copy">
      <h2 class="dsp" style="font-size:clamp(2rem,.9rem + 3.6vw,4.2rem)">How an event comes together</h2>
      <p>Every project follows the same four steps, whether it is one bouquet or a full wedding. <span class="ph">[Confirm this process and add typical timelines.]</span></p>
    </div>
    <ol class="steps">
      <li><div><h3>Inquire</h3><p>Tell us the date, the place and what you are imagining. We reply with availability.</p></div></li>
      <li><div><h3>Consult</h3><p>We talk through the space, your palette and your priorities, and look at inspiration together.</p></div></li>
      <li><div><h3>Design</h3><p>You receive a proposal with florals, quantities and pricing. We refine it with you until it feels right.</p></div></li>
      <li><div><h3>Deliver and set up</h3><p>We prepare the flowers, bring them to your venue and install them, so you can focus on everything else.</p></div></li>
    </ol>
  </div>
</section>

<section class="panels">
  <div class="panel panel--img">{im('designer-smile', 'The designer smiling in a beige apron, holding a bouquet of white, yellow and orange flowers')}</div>
  <div class="panel panel--petal panel--center"><div>
    <h2 class="dsp">Meet the designer behind 1848</h2>
    <p>Every arrangement starts with one person’s eye. Read how she got started and what she cares about when she designs.</p>
    <div class="btn-row"><a class="btn" href="designer.html">Meet the designer</a></div>
  </div></div>
</section>

{closer('Tell us about your event.', 'Inquire now', band='band-paper2')}
'''
page('about.html', 'About', 'About 1848 Blooms & Designs, a wedding and event floral studio serving Delaware, Greenville, Philadelphia, New Hope and the surrounding areas.', about)

# ================================================================== DESIGNER
designer = f'''
{phero('designer-couch', 'The designer relaxing on a cream sofa with a laptop, a bouquet of orange and yellow flowers beside her', 'Meet the designer', 'Designer<br>and owner', '1848 Blooms<br>&amp; Designs',
       '<span class="ph">[Designer name]</span>, designer and owner of 1848 Blooms &amp; Designs.')}

<section class="panels">
  <div class="panel panel--img" style="min-height:640px">{im('designer-doorway', 'The designer standing in a sunlit doorway wearing a beige apron')}</div>
  <div class="panel panel--petal panel--center"><div>
    <h2 class="dsp">Why flowers</h2>
    <p class="ph">[Her story, in her own voice: how she started, what first drew her to flowers, and what the name 1848 means. Two or three short paragraphs is plenty.]</p>
    <p class="ph">I design with the season first. What is growing decides the palette, and the room decides the shape. [Edit or replace this line so it sounds like her.]</p>
    <p class="ph">[What she loves most about the work: the first walk-through of a venue, the moment a bouquet comes together, the room when guests arrive.]</p>
    <div class="btn-row"><a class="btn" href="contact.html">Work with her</a><a class="btn btn--ghost" href="experiences.html">Join an experience</a></div>
  </div></div>
</section>

<section class="section band-paper2">
  <div class="wrap">
    {tbar('In the studio', 'Making', 'Gathering')}
    <div class="strip" style="margin-top:clamp(2rem,4vw,3.5rem)">
      <figure style="--r:{ratio('designer-window')}">{im('designer-window', 'The designer in an orange shirt and apron holding a bouquet by a window')}</figure>
      <figure style="--r:{ratio('designer-making')}">{im('designer-making', 'A designer arranging flowers in white bowls at a wooden table by a window')}</figure>
      <figure style="--r:{ratio('designer-stool')}">{im('designer-stool', 'The designer laughing on a stool, holding a bouquet and a single stem')}</figure>
    </div>
  </div>
</section>

{closer('Let’s make something together.', 'Inquire now')}
'''
page('designer.html', 'Meet the designer', 'Meet the designer and owner of 1848 Blooms & Designs, a wedding and event florist serving Delaware, Philadelphia and New Hope.', designer, og='designer-smile')

# ================================================================== SERVICES
services = f'''
{phero('arch-pampas', 'A wooden triangle ceremony arch dressed with pampas grass and dried flowers on a deck', 'Services', 'Weddings', 'Events',
       'Full-service wedding and event florals for Delaware, Greenville, Philadelphia, New Hope and the surrounding areas, from a single bouquet to a ceremony and reception, designed around your venue and delivered by us.',
       '<a class="btn" href="contact.html">Start an inquiry</a>')}

<section id="weddings" class="panels">
  <div class="panel panel--img" style="min-height:680px">{im('kiss-arch', 'A couple kissing under a wooden arch draped in white fabric and white flowers')}</div>
  <div class="panel panel--petal panel--center"><div>
    <h2 class="dsp">Weddings</h2>
    <p>Your florals should feel like you and fit your venue. We design the whole picture so the ceremony, the reception and the people in them all feel connected.</p>
    <ul class="tick">
      <li><strong>Bridal and bridesmaid bouquets</strong><span>Plus boutonnieres, corsages and flowers for family.</span></li>
      <li><strong>Ceremony florals</strong><span>Arches, aisle pieces and welcome signage.</span></li>
      <li><strong>Reception florals</strong><span>Centerpieces, head table and tablescapes.</span></li>
      <li><strong>Installations</strong><span>Hanging and statement pieces for the moments guests will photograph.</span></li>
    </ul>
    <p class="small"><span class="ph">Wedding florals start at [$____].</span></p>
    <div class="btn-row"><a class="btn" href="contact.html?type=wedding">Inquire about your wedding</a><a class="btn btn--ghost" href="weddings.html">More on weddings</a></div>
  </div></div>
</section>

<section id="events" class="panels">
  <div class="panel panel--deep panel--center"><div>
    <h2 class="dsp">Events</h2>
    <p>Dinners, showers, birthdays and corporate gatherings across Delaware, Greenville, Philadelphia and New Hope. We style the table and the room so the occasion feels considered from the first glance.</p>
    <ul class="tick">
      <li><strong>Tablescapes and centerpieces</strong><span>Florals planned alongside your linens, candles and place settings.</span></li>
      <li><strong>Hanging and ladder installations</strong><span>Overhead pieces that turn a plain room into a place.</span></li>
      <li><strong>Arrangements and bouquets</strong><span>For hosts, guests of honor and gifting.</span></li>
    </ul>
    <p class="small" style="color:rgba(246,238,232,.85)"><span class="ph">Event florals start at [$____].</span></p>
    <div class="btn-row"><a class="btn btn--cream" href="contact.html?type=private">Inquire about your event</a></div>
  </div></div>
  <div class="panel panel--img" style="min-height:680px">{im('pastel-table-a', 'A pastel table with a tall arrangement of pink and white flowers, a taper candle and pink napkins')}</div>
</section>

<section class="panels">
  <div class="panel panel--img" style="min-height:460px">{im('installation-hanging', 'A long hanging floral installation of pink, magenta and white flowers with trailing greenery')}</div>
  <div class="panel panel--petal-2 panel--paper2 panel--center"><div>
    <h2 class="dsp">Want guests to make their own?</h2>
    <p>Add a Floral Bar to your event, or book a hands-on experience for your group.</p>
    <div class="btn-row"><a class="btn" href="floral-bar.html">See the Floral Bar</a><a class="btn btn--ghost" href="experiences.html">See experiences</a></div>
  </div></div>
</section>

<section class="section">
  <div class="wrap split split--top split--57">
    <h2 class="dsp" style="font-size:clamp(2rem,.9rem + 3.4vw,4rem)">Questions we hear a lot</h2>
    <div class="faq">
      <details><summary>How far ahead should I book?</summary><div><p class="ph">[Answer: for example, how many months ahead for weddings and how many weeks for events.]</p></div></details>
      <details><summary>Do you deliver and set up?</summary><div><p class="ph">[Answer: delivery and setup details, and any fees.]</p></div></details>
      <details><summary>Do you travel outside Delaware and Philadelphia?</summary><div><p class="ph">[Answer: travel radius and travel fees.]</p></div></details>
      <details><summary>How do deposits and payments work?</summary><div><p class="ph">[Answer: deposit amount, payment schedule and accepted payment methods.]</p></div></details>
      <details><summary>Can I choose my own colors and flowers?</summary><div><p class="ph">[Answer: how much of the palette is the client’s call, and how seasonality affects it.]</p></div></details>
    </div>
  </div>
</section>

{closer('Ready to talk florals?', 'Inquire now', band='band-petal')}
'''
page('services.html', 'Wedding & Event Florals', 'Wedding and event florals in Delaware, Greenville, Philadelphia and New Hope: bouquets, ceremony and reception florals, tablescapes and installations, set up by us.', services, og='arch-pampas')

# ================================================================== WEDDINGS (landing page for "wedding florist" searches)
WG = [('bouquet-bright', 'A bright bridal bouquet of yellow, coral and blush flowers held against a white dress'),
      ('arch-willow', 'A wooden ceremony pergola draped with white fabric and flowers beneath a willow tree'),
      ('bridesmaids', 'Bridesmaids in lavender dresses holding white bouquets on a brick patio'),
      ('reception-lights', 'A wedding reception table beneath string lights with a pampas and rose centerpiece')]
wstrip = ''.join(f'<figure style="--r:{ratio(n)}">{im(n, a, sizes="(max-width: 900px) 50vw, 25vw")}</figure>' for n, a in WG)
weddings = f'''
{phero('couple-window', 'A bride and groom sharing a quiet moment at a window, her bouquet in hand', 'Wedding florist', 'Delaware<br>and Greenville', 'Philadelphia<br>and New Hope',
       'Wedding flowers for couples marrying in Delaware, Greenville, Philadelphia, New Hope and the surrounding areas, designed around your venue and set up by us.',
       '<a class="btn" href="contact.html?type=wedding">Check your date</a>')}

<section class="panels">
  <div class="panel panel--img" style="min-height:680px">{im('kiss-arch', 'A couple kissing under a wooden wedding arch draped in white fabric and white flowers')}</div>
  <div class="panel panel--petal panel--center"><div>
    <h2 class="dsp">Wedding flowers, start to finish</h2>
    <p>Your florals should feel like you and fit your venue. We design the whole picture so the ceremony, the reception and the people in them all feel connected, and we take on a limited number of weddings each season so every couple gets our full creative focus.</p>
    <ul class="tick">
      <li><strong>Bridal and bridesmaid bouquets</strong><span>Plus boutonnieres, corsages and flowers for family.</span></li>
      <li><strong>Ceremony florals</strong><span>Arches, aisle pieces and welcome signage.</span></li>
      <li><strong>Reception florals</strong><span>Centerpieces, head table and tablescapes.</span></li>
      <li><strong>Installations</strong><span>Hanging and statement pieces for the moments guests will photograph.</span></li>
      <li><strong>A Floral Bar</strong><span>Guests build their own bouquet as a favor. <a class="link" href="floral-bar.html">How it works</a></span></li>
    </ul>
    <p class="small"><span class="ph">Wedding florals start at [$____].</span></p>
    <div class="btn-row"><a class="btn" href="contact.html?type=wedding">Inquire about your wedding</a></div>
  </div></div>
</section>

<section class="section band-paper2">
  <div class="wrap">
    {tbar('Recent weddings', 'Bouquets', 'Ceremonies')}
    <div class="strip" style="margin-top:clamp(2rem,4vw,3.5rem)">{wstrip}</div>
    <div class="btn-row btn-row--center" style="margin-top:clamp(2rem,4vw,3rem)"><a class="btn" href="portfolio.html#weddings">See the wedding portfolio</a></div>
  </div>
</section>

<section class="section">
  <div class="wrap split split--top split--57">
    <div class="copy">
      <h2 class="dsp" style="font-size:clamp(2rem,.9rem + 3.6vw,4.2rem)">Where we design weddings</h2>
      <p>We design and install wedding flowers across Delaware, including Greenville, and in Philadelphia, New Hope and the surrounding areas of Pennsylvania. Marrying a little farther out? Tell us the venue and we will let you know what is possible.</p>
      <p class="ph">[Name a few venues you have worked at or love, for example estates, barns, gardens and city venues. Real venue names help couples searching for them find you.]</p>
    </div>
    <ol class="steps">
      <li><div><h3>Inquire</h3><p>Tell us your date, your venue and what you are imagining. We reply with availability.</p></div></li>
      <li><div><h3>Consult</h3><p>We talk through the space, your palette and your priorities, and look at inspiration together.</p></div></li>
      <li><div><h3>Design</h3><p>You receive a proposal with florals, quantities and pricing. We refine it with you until it feels right.</p></div></li>
      <li><div><h3>Deliver and set up</h3><p>We bring everything to your venue and install it, so you can focus on the day.</p></div></li>
    </ol>
  </div>
</section>

<section class="section band-paper2">
  <div class="wrap split split--top split--57">
    <h2 class="dsp" style="font-size:clamp(2rem,.9rem + 3.4vw,4rem)">Wedding flower questions</h2>
    <div class="faq">
      <details><summary>How far ahead should we book our wedding florist?</summary><div><p class="ph">[Answer: how many months ahead most couples book, and how busy spring and fall get.]</p></div></details>
      <details><summary>Do you deliver and set up at our venue?</summary><div><p>Yes. We bring the flowers to your venue and install them. <span class="ph">[Add any delivery or breakdown fees.]</span></p></div></details>
      <details><summary>Which areas do you serve?</summary><div><p>Delaware, including Greenville, plus Philadelphia, New Hope and the surrounding areas. <span class="ph">[Add your travel radius and any travel fees.]</span></p></div></details>
      <details><summary>Is there a minimum for weddings?</summary><div><p class="ph">[Answer: your wedding minimum or typical starting investment.]</p></div></details>
      <details><summary>Can we choose our own colors and flowers?</summary><div><p class="ph">[Answer: how much of the palette is the couple’s call, and how seasonality affects it.]</p></div></details>
    </div>
  </div>
</section>

<section class="section band-petal"><div class="wrap closer">
  <h2 class="dsp">Tell us about your wedding.</h2>
  <p style="max-width:40ch;margin:1.2rem auto 0">Share your date, venue and guest count, and we will reply with availability and next steps.</p>
  <div class="btn-row btn-row--center"><a class="btn btn--arrow" href="contact.html?type=wedding">Check your date</a></div>
  <p class="small" style="margin-top:1.4rem">Or write to {email_link()} &middot; {phone_link()}</p>
</div></section>
'''
page('weddings.html', 'Wedding Florist in Delaware, Philadelphia & New Hope',
     'Wedding flowers for couples in Delaware, Greenville, Philadelphia and New Hope: bridal bouquets, ceremony arches, centerpieces and installations. Check your date.',
     weddings, og='kiss-arch', schema=[{
         '@context': 'https://schema.org', '@type': 'Service', 'serviceType': 'Wedding florist',
         'name': 'Wedding florals', 'url': DOMAIN + 'weddings.html',
         'description': 'Bridal and bridesmaid bouquets, ceremony florals, reception florals and installations, delivered and set up at your venue.',
         'provider': {'@type': 'Florist', '@id': DOMAIN + '#business', 'name': SITE, 'url': DOMAIN}, 'areaServed': AREAS}],
     full_title='Wedding Florist in Delaware, Philadelphia & New Hope | 1848 Blooms')

# ================================================================== FLORAL BAR
bar = f'''
{phero('', '', 'The Floral Bar', 'Pick<br>and arrange', 'Take it<br>home',
       'A self-serve flower station for your event. Guests choose their own blooms, build a bouquet or arrangement, and leave with something they made.',
       '<a class="btn" href="contact.html">Inquire about a Floral Bar</a>', plain=True)}

<section class="panels">
  <div class="panel panel--img" style="min-height:640px">{im('home-floralbar', 'A woven basket filled with white and hot pink roses')}</div>
  <div class="panel panel--deep panel--center"><div>
    <h2 class="dsp">Pick your stems. Arrange them. Take them home.</h2>
    <p>The Floral Bar turns flowers into the activity. We set up the bar with seasonal stems, greenery and containers in your palette, and a designer shows guests how to build something beautiful.</p>
    <div class="btn-row"><a class="btn btn--cream" href="contact.html">Inquire about a Floral Bar</a></div>
  </div></div>
</section>

<section class="section">
  <div class="wrap">
    {tbar('How it works', 'Three steps', 'For every guest')}
    <ol class="steps steps--three" style="margin-top:clamp(2.5rem,5vw,4.5rem)">
      <li><h3>Pick</h3><p>We set up the bar with seasonal stems, greenery and containers in your palette. Guests choose what they love.</p></li>
      <li><h3>Arrange</h3><p>A designer is on hand to show guests how to build a bouquet or arrangement, whatever their experience.</p></li>
      <li><h3>Take</h3><p>Everyone leaves with their own piece, wrapped and ready to carry home. It doubles as a favor.</p></li>
    </ol>
  </div>
</section>

<section class="panels">
  <div class="panel panel--petal panel--center"><div>
    <h2 class="dsp">Where it works best</h2>
    <ul class="tick">
      <li><strong>Bridal showers and bachelorette parties</strong></li>
      <li><strong>Weddings and rehearsal dinners</strong><span>Part of the reception, or a favor guests make.</span></li>
      <li><strong>Birthdays and baby showers</strong></li>
      <li><strong>Corporate and team events</strong></li>
    </ul>
    <p><span class="ph">[What is included: stems per guest, containers, a designer on site, setup and cleanup, and the guest counts you can serve.]</span></p>
    <p class="small"><span class="ph">Floral Bar packages start at [$____].</span></p>
    <div class="btn-row"><a class="btn" href="contact.html">Inquire about a Floral Bar</a></div>
  </div></div>
  <div class="panel panel--img" style="min-height:640px">{im('ladder-daisies', 'Daisies and cosmos in a woven basket at the foot of a wooden ladder')}</div>
</section>

{closer('Bring the Floral Bar to your event.', 'Start an inquiry', band='band-paper2')}
'''
page('floral-bar.html', 'Floral Bar for Weddings & Events', 'A self-serve flower bar for weddings, showers and events in Delaware, Philadelphia and New Hope. Guests pick stems, arrange them and take them home.', bar, og='home-floralbar')

# ================================================================== EXPERIENCES
exp = f'''
{phero('designing-table', 'A florist arranging yellow and white flowers at a table in a bright room', 'Experiences', 'Workshops', 'Private<br>gatherings',
       'Hands-on floral experiences that bring people together around flowers, designed to inspire creativity and connection.',
       '<a class="btn" href="reserve.html">Reserve your spot</a>')}

<section class="section">
  <div class="wrap">
    <div class="xp">
      <figure>{im('designer-making', 'A designer arranging flowers in white bowls at a wooden table by a window')}</figure>
      <div>
        <h2 class="dsp">Floral workshops</h2>
        <p>Join a small class, learn the techniques behind a designer’s arrangements and leave with your own piece. No experience needed. <span class="ph">[Confirm format.]</span></p>
        <dl>
          <dt>Length</dt><dd><span class="ph">[Hours]</span></dd>
          <dt>Group size</dt><dd><span class="ph">[Number of guests]</span></dd>
          <dt>Price</dt><dd><span class="ph">[$ per person]</span></dd>
          <dt>Where</dt><dd><span class="ph">[Studio or venue and city]</span></dd>
        </dl>
        <div class="btn-row"><a class="btn" href="reserve.html?experience=workshop">Reserve your spot</a></div>
      </div>
    </div>
    <div class="xp">
      <figure>{im('table-window', 'A bright table by a window set with glassware and a centerpiece of yellow and orange flowers', '', extra='style="object-position:50% 75%"')}</figure>
      <div>
        <h2 class="dsp">Private gatherings</h2>
        <p>Bring a workshop to your group: bridal showers, birthdays, team outings or a day with friends. We shape the experience around the occasion. <span class="ph">[Confirm format.]</span></p>
        <dl>
          <dt>Length</dt><dd><span class="ph">[Hours]</span></dd>
          <dt>Group size</dt><dd><span class="ph">[Minimum and maximum]</span></dd>
          <dt>Price</dt><dd><span class="ph">[$ per person or per group]</span></dd>
          <dt>Where</dt><dd><span class="ph">[Your space or ours]</span></dd>
        </dl>
        <div class="btn-row"><a class="btn" href="reserve.html?experience=private">Reserve your spot</a></div>
      </div>
    </div>
  </div>
</section>

<section class="section band-paper2">
  <div class="wrap split split--top split--57">
    <div class="copy"><h2 class="dsp" style="font-size:clamp(2rem,.9rem + 3.4vw,4rem)">Upcoming dates</h2><p>Spots are limited so everyone gets time with the designer.</p></div>
    <table class="dates">
      <thead><tr><th scope="col">Date</th><th scope="col">Experience</th><th scope="col">Spots</th></tr></thead>
      <tbody>
        <tr><td><span class="ph">[Date and time]</span></td><td><span class="ph">[Workshop name]</span></td><td><a class="link" href="reserve.html?experience=workshop">Reserve</a></td></tr>
        <tr><td><span class="ph">[Date and time]</span></td><td><span class="ph">[Workshop name]</span></td><td><a class="link" href="reserve.html?experience=workshop">Reserve</a></td></tr>
        <tr><td><span class="ph">[Date and time]</span></td><td><span class="ph">[Workshop name]</span></td><td><a class="link" href="reserve.html?experience=workshop">Reserve</a></td></tr>
      </tbody>
    </table>
  </div>
</section>

{closer('Make something beautiful together.', 'Reserve your spot', 'reserve.html', 'band-petal')}
'''
page('experiences.html', 'Floral Workshops & Private Gatherings', 'Hands-on floral workshops and private flower-arranging parties with 1848 Blooms & Designs in Delaware, Greenville, Philadelphia and New Hope.', exp, og='designing-table')

# ================================================================== PORTFOLIO
P = [
    ('kiss-arch', 'weddings', 'A couple kissing under a wooden arch draped in white fabric and flowers'),
    ('table-long-pastel', 'events', 'A long white table with pastel centerpieces and wishbone chairs'),
    ('bouquet-bright', 'bouquets weddings', 'A bright bouquet of yellow, coral and blush flowers held against a white dress'),
    ('bridesmaids', 'weddings', 'Bridesmaids in lavender dresses holding white bouquets on a brick patio'),
    ('place-setting', 'details events', 'A place setting with a blush menu card, a sprig of yellow flowers and gold flatware'),
    ('installation-hanging', 'events', 'A long hanging floral installation of pink, magenta and white flowers'),
    ('bouquet-chair', 'bouquets', 'A pink and blue bouquet with a pale blue ribbon resting on a wooden chair'),
    ('arch-pampas', 'weddings', 'A wooden triangle ceremony arch dressed with pampas grass and dried flowers'),
    ('flatlay-suite', 'details weddings', 'An invitation suite flat lay with a ring box and soft blooms'),
    ('pastel-table-a', 'events', 'A pink and cream table with a tall pastel arrangement and a taper candle'),
    ('couple-window', 'weddings', 'A bride and groom sharing a quiet moment at a window, her bouquet in hand'),
    ('tablescape-citrus', 'events details', 'A centerpiece of orange roses and yellow blooms on a linen-covered table'),
    ('bouquet-white-b', 'bouquets', 'A white bouquet of roses and wildflowers with greenery'),
    ('reception-lights', 'events weddings', 'A reception table beneath string lights with a pampas and rose centerpiece'),
    ('ladder-daisies', 'floral-bar', 'Daisies and cosmos in a woven basket beside a wooden ladder'),
    ('bouquet-ribbon', 'bouquets', 'A pastel and coral bouquet tied with a rust-colored ribbon'),
    ('flatlay-blue', 'details', 'Blush invitation cards with pale blue ribbon and delphinium'),
    ('arch-willow', 'weddings', 'A wooden ceremony pergola draped with white fabric and flowers beneath a willow tree'),
    ('bowl-window', 'details events', 'A white footed bowl of yellow, peach and pink flowers on a window ledge'),
    ('basket-walk', 'floral-bar', 'A woman in a white dress carrying a striped basket of wildflowers'),
    ('couple-bouquet', 'weddings', 'A bride seated with a white bouquet beside her groom'),
    ('bouquet-anthurium', 'bouquets', 'A bouquet with green anthurium, white roses and a cream ribbon'),
    ('tablescape-detail', 'details events', 'A closeup of a tablescape with roses, glassware and a place card'),
    ('installation-ladders', 'events', 'A hanging floral installation above two wooden ladders with small vases'),
    ('pastel-closeup', 'details events', 'A closeup of pink roses and blue glassware on a pastel table'),
    ('bouquet-marble', 'bouquets', 'A white bouquet tied with trailing ribbon on a marble stool'),
    ('invitations-pink', 'details', 'Blush wedding invitations with a ring box and yellow craspedia'),
    ('ladder-basket', 'floral-bar', 'A woven basket of wildflowers on a wooden ladder'),
]
shots = ''.join(f'<button type="button" class="shot" data-cat="{c}" aria-label="View larger: {html.escape(a)}">{im(n, a, sizes='(max-width: 900px) 50vw, 33vw')}</button>' for n, c, a in P)
portfolio = f'''
{phero('', '', 'Portfolio', 'Weddings<br>and events', 'Bouquets<br>and details',
       'A look at recent weddings, events, bouquets and the details between them.', plain=True)}

<section class="section section--tight">
  <div class="wrap">
    <div class="filters" role="group" aria-label="Filter portfolio">
      <button type="button" data-filter="all" aria-pressed="true">All</button>
      <button type="button" data-filter="weddings" aria-pressed="false">Weddings</button>
      <button type="button" data-filter="events" aria-pressed="false">Events</button>
      <button type="button" data-filter="bouquets" aria-pressed="false">Bouquets</button>
      <button type="button" data-filter="details" aria-pressed="false">Details</button>
      <button type="button" data-filter="floral-bar" aria-pressed="false">Floral Bar</button>
    </div>
    <div class="gallery">{shots}</div>
  </div>
</section>

<dialog class="lb" id="lightbox" aria-label="Photo viewer">
  <div class="lb__in"><img src="" alt=""><p class="lb__cap"></p></div>
  <button type="button" class="x" aria-label="Close">&times;</button>
  <button type="button" class="pv" aria-label="Previous photo">&lsaquo;</button>
  <button type="button" class="nx" aria-label="Next photo">&rsaquo;</button>
</dialog>

{closer('Like what you see?', 'Inquire now', band='band-paper2')}
'''
page('portfolio.html', 'Wedding & Event Flower Portfolio', 'Real weddings, events, bridal bouquets and floral details by 1848 Blooms & Designs, a florist serving Delaware, Philadelphia and New Hope.', portfolio, og='kiss-arch')

# ================================================================== CONTACT
contact = f'''
{phero('', '', 'Contact', 'Inquiries', 'Now booking<br>2026',
       'Share the basics and we will reply with availability and next steps. <span class="ph">[Typical response time.]</span>', plain=True)}

<section class="section">
  <div class="wrap form-grid">
    <form class="form" data-form="inquiry" novalidate>
      <div class="field"><label for="name">Your name</label><input id="name" name="name" autocomplete="name" required><p class="err">Enter your name.</p></div>
      <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required><p class="err">Enter a valid email address.</p></div>
      <div class="field"><label for="phone">Phone <span class="hint">(optional)</span></label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
      <div class="field"><label for="kind">What are you planning?</label>
        <select id="kind" name="event_type" required>
          <option value="">Choose one</option>
          <option>Wedding</option><option>Private event</option><option>Corporate event</option>
          <option>Floral Bar</option><option>Workshop or private gathering</option><option>Something else</option>
        </select><p class="err">Choose what you are planning.</p></div>
      <div class="field"><label for="date">Event date <span class="hint">(if you have one)</span></label><input id="date" name="event_date" type="date"></div>
      <div class="field"><label for="venue">Venue or city</label><input id="venue" name="venue" autocomplete="off"></div>
      <div class="field"><label for="guests">Guest count <span class="hint">(roughly)</span></label><input id="guests" name="guests" type="number" min="1" inputmode="numeric"></div>
      <div class="field"><label for="found">How did you find us?</label><input id="found" name="found_us"></div>
      <div class="field full"><label for="msg">What are you imagining?</label><textarea id="msg" name="message" placeholder="Colors, flowers you love, the feeling you want, anything that helps." required></textarea><p class="err">Tell us a little about your plans.</p></div>
      <div class="hp" aria-hidden="true"><label>Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label></div>
      <div class="notice" role="status"></div>
      <button class="btn" type="submit">Send inquiry</button>
    </form>
    <aside class="aside">
      {im('pastel-table-c', 'A pastel table set with a tall arrangement of pink and white flowers, pink napkins and gold flatware')}
      <dl>
        <div><dt>Email</dt><dd>{email_link()}</dd></div>
        <div><dt>Phone</dt><dd>{phone_link()}</dd></div>
        <div><dt>Service area</dt><dd>Delaware, Greenville, Philadelphia, New Hope and the surrounding areas</dd></div>
        <div><dt>Follow along</dt><dd><a class="link" href="{BIZ['instagram'] or '#'}">Instagram</a>, <a class="link" href="{BIZ['pinterest'] or '#'}">Pinterest</a>, <a class="link" href="{BIZ['facebook'] or '#'}">Facebook</a></dd></div>
      </dl>
    </aside>
  </div>
</section>
'''
page('contact.html', 'Contact & Inquiries', 'Inquire about wedding or event florals, the Floral Bar or a workshop. 1848 Blooms & Designs serves Delaware, Greenville, Philadelphia and New Hope.', contact, schema=[florist()])

# ================================================================== RESERVE
reserve = f'''
{phero('', '', 'Reserve your spot', 'Workshops', 'Private<br>gatherings',
       'Choose an experience and a date, and we will confirm your spot by email.', plain=True)}

<section class="section">
  <div class="wrap form-grid">
    <form class="form" data-form="reservation" novalidate>
      <fieldset class="field full" style="border:0;padding:0;margin:0">
        <legend>Which experience?</legend>
        <div class="choice" style="margin-top:.6rem">
          <label><input type="radio" name="experience" value="workshop" required><span>Floral workshop</span></label>
          <label><input type="radio" name="experience" value="private"><span>Private gathering</span></label>
        </div>
        <p class="err">Choose an experience.</p>
      </fieldset>
      <div class="field"><label for="rdate">Preferred date</label><input id="rdate" name="preferred_date" type="date" required><p class="err">Choose a date.</p></div>
      <div class="field"><label for="rguests">Number of guests</label><input id="rguests" name="guests" type="number" min="1" value="1" inputmode="numeric" required><p class="err">Enter how many guests.</p></div>
      <div class="field"><label for="rname">Your name</label><input id="rname" name="name" autocomplete="name" required><p class="err">Enter your name.</p></div>
      <div class="field"><label for="remail">Email</label><input id="remail" name="email" type="email" autocomplete="email" required><p class="err">Enter a valid email address.</p></div>
      <div class="field"><label for="rphone">Phone <span class="hint">(optional)</span></label><input id="rphone" name="phone" type="tel" autocomplete="tel"></div>
      <div class="field full"><label for="rnotes">Anything we should know?</label><textarea id="rnotes" name="notes" placeholder="The occasion, accessibility needs, or questions."></textarea></div>
      <div class="hp" aria-hidden="true"><label>Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label></div>
      <div class="notice" role="status"></div>
      <button class="btn" type="submit">Reserve my spot</button>
    </form>
    <aside class="aside">
      {im('designer-making', 'A designer arranging flowers in white bowls at a wooden table', '', extra='style="aspect-ratio:3/2;object-position:30% 50%"')}
      <dl>
        <div><dt>What happens next</dt><dd>We email you to confirm your date and share details. <span class="ph">[Add payment steps.]</span></dd></div>
        <div><dt>Cancellations</dt><dd><span class="ph">[Cancellation and rescheduling policy.]</span></dd></div>
        <div><dt>Questions</dt><dd><a class="link" href="contact.html">Send us a message</a></dd></div>
      </dl>
    </aside>
  </div>
</section>
'''
page('reserve.html', 'Reserve a Workshop Spot', 'Reserve a spot in a floral workshop or private gathering with 1848 Blooms & Designs in Delaware, Philadelphia and New Hope.', reserve)

# ================================================================== THANK YOU
thanks = f'''
<div data-thanks>
<section class="phero phero--plain">
  <div class="phero__mid"><div class="tbar"><p class="flank">We received<br>your message</p><h1 class="dsp" data-ty-title>Thank you</h1><p class="flank">Talk<br>soon</p></div></div>
  <div class="phero__foot">
    <p data-ty="inquiry">We received your inquiry and will reply by email <span class="ph">[within X business days]</span>.</p>
    <p data-ty="reservation" hidden>We received your reservation request. We will email you to confirm your spot <span class="ph">[within X business days]</span>.</p>
  </div>
</section>
<section class="section thanks-body">
  <div class="wrap split">
    <div>
      <ul class="tick">
        <li><strong>While you wait</strong><span>Browse recent work in the <a class="link" href="portfolio.html">portfolio</a>, or save ideas to share when we talk.</span></li>
        <li><strong>Need to add something?</strong><span>Reply to our email, or write to us at {email_link()}.</span></li>
      </ul>
      <div class="btn-row" style="margin-top:2rem"><a class="btn" href="index.html">Back to home</a><a class="btn btn--ghost" href="portfolio.html">See the portfolio</a></div>
    </div>
    <figure>{im('bouquet-ribbon', 'A pastel and coral bouquet tied with a rust-colored ribbon', '', extra='style="aspect-ratio:4/5;object-position:50% 40%"')}</figure>
  </div>
</section>
</div>
'''
page('thank-you.html', 'Thank you', 'Thank you from 1848 Blooms & Designs.', thanks, noindex=True)

# ================================================================== 404 (GitHub Pages serves this for any missing URL,
# including old Shopify links like /pages/contact, so it sends visitors somewhere useful)
nf = f'''
<section class="phero phero--plain">
  <div class="phero__mid"><span class="eyebrow">Page not found</span><div class="tbar"><h1 class="dsp">This page has moved</h1></div></div>
  <div class="phero__foot"><p>The page you were looking for is not here any more. Try one of these instead.</p>
  <div class="btn-row"><a class="btn" href="weddings.html">Weddings</a><a class="btn" href="services.html">Weddings + events</a><a class="btn btn--ghost" href="contact.html">Contact</a></div></div>
</section>
<script>(function(){{var p=location.pathname.toLowerCase(),m=[['wedding','weddings.html'],['contact','contact.html'],['about','about.html'],['portfolio','portfolio.html'],['gallery','portfolio.html'],['workshop','experiences.html'],['class','experiences.html'],['bar','floral-bar.html'],['event','services.html']];
for(var i=0;i<m.length;i++)if(p.indexOf(m[i][0])>-1){{location.replace('/'+m[i][1]);return;}}}})();</script>
'''
page('404.html', 'Page not found', 'This page has moved. Find wedding and event florals by 1848 Blooms & Designs.', nf, noindex=True)
# links on the 404 page must work from any depth (e.g. /pages/contact), so make them root-relative
_n = open(f'{OUT}/404.html').read()
for a in ('href="assets/', 'src="assets/', 'srcset="assets/', ', assets/', 'href="index.html', 'href="weddings.html', 'href="about.html', 'href="services.html',
          'href="floral-bar.html', 'href="portfolio.html', 'href="experiences.html', 'href="contact.html', 'href="reserve.html', 'href="designer.html'):
    _n = _n.replace(a, a.replace('"', '"/', 1) if '"' in a else ', /assets/')
open(f'{OUT}/404.html', 'w').write(_n)

# ================================================================== SITEMAP + ROBOTS
PRI = {'index.html': '1.0', 'weddings.html': '0.9', 'services.html': '0.9', 'contact.html': '0.8', 'portfolio.html': '0.7'}
urls = ''.join(f'  <url><loc>{DOMAIN if f == "index.html" else DOMAIN + f}</loc><lastmod>{TODAY}</lastmod><priority>{PRI.get(f, "0.6")}</priority></url>\n'
               for f, ni in PAGES if not ni)
open(f'{OUT}/sitemap.xml', 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
open(f'{OUT}/robots.txt', 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}sitemap.xml\n')
print('built', len([f for f in os.listdir(OUT) if f.endswith('.html')]), 'pages')
