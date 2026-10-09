# Upgraded catalogue builder (v2). Usage: python3 build_v2.py <base catalogue html> build.py <out.html> images.json
# real-project galleries, buyer FAQ) on top of the existing design system.
# Usage: python3 build2.py <base.html> <build.py> <out.html> <images.json>
import re, sys, json

BASE, OLD_BUILD, OUT, IMGS = sys.argv[1:5]
s = open(BASE).read()
I = json.load(open(IMGS))          # slot -> filename (all under img/)
style = s[s.index('<style>'):s.index('</style>') + len('</style>')]
defs = s[s.index('<svg width="0"'):]
defs = defs[:defs.index('</svg>') + len('</svg>')]
ob = open(OLD_BUILD).read()
EXTRA_CSS = ob[ob.index("EXTRA_CSS = r'''") + len("EXTRA_CSS = r'''"):]
EXTRA_CSS = EXTRA_CSS[:EXTRA_CSS.index("'''")]

NEW_CSS = r'''
/* ---------- trust ---------- */
.trust-hero { position: relative; height: 30cqw; margin-inline: -6.6cqw; overflow: hidden; }
.trust-hero img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 50%; }
.trust-hero::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, rgb(21 48 42 / .88) 0%, rgb(21 48 42 / .55) 46%, rgb(21 48 42 / 0) 78%); }
.trust-hero .msg { position: absolute; left: 6.6cqw; top: 0; bottom: 0; display: grid; align-content: center; gap: 1.2cqw; max-width: 46cqw; z-index: 1; }
.trust-hero .msg p { color: var(--on-dark); font: 700 2.7cqw/1.18 var(--display); font-stretch: 106%; margin: 0; }
.trust-hero .msg span { color: var(--brass-soft); font: 500 1.05cqw/1.3 var(--mono); letter-spacing: .16em; text-transform: uppercase; }
.trust8 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 3.2cqw 2.2cqw; flex: 1; align-content: start; }
.trust8 article { display: grid; gap: .9cqw; align-content: start; padding-top: 1.6cqw; border-top: .18cqw solid var(--spruce); }
.trust8 svg { width: 3.4cqw; height: 3.4cqw; color: var(--brass); }
.trust8 h3 { font-size: 2.05cqw; line-height: 1.12; }
.trust8 p { font-size: 1.42cqw; line-height: 1.45; color: var(--muted); }
.assure { display: flex; justify-content: space-between; align-items: center; gap: 3cqw; padding: 2.2cqw 2.6cqw; border: .16cqw solid var(--brass); }
.assure strong { font: 760 2.2cqw/1.15 var(--display); font-stretch: 108%; color: var(--spruce); }
.assure span { font-size: 1.36cqw; color: var(--muted); max-width: 44cqw; line-height: 1.45; }

/* ---------- hierarchy overview ---------- */
.lvl { display: flex; align-items: baseline; justify-content: space-between; gap: 2cqw; border-bottom: .18cqw solid var(--spruce); padding-bottom: .8cqw; }
.lvl b { font: 760 2cqw/1 var(--display); font-stretch: 110%; color: var(--spruce); }
.lvl span { font: 500 1.02cqw/1 var(--mono); letter-spacing: .15em; text-transform: uppercase; color: var(--brass); }
.core4 { display: grid; grid-template-columns: 1fr 1fr; gap: 2.2cqw 2.4cqw; }
.core4 article { display: grid; gap: .7cqw; }
.core4 img { width: 100%; height: 19cqw; object-fit: cover; }
.core4 h3 { font-size: 2.4cqw; display: flex; justify-content: space-between; align-items: baseline; }
.core4 h3 small { font: 500 1.02cqw/1 var(--mono); letter-spacing: .12em; color: var(--brass); }
.core4 p { font-size: 1.36cqw; color: var(--muted); }
.more8 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.6cqw 1.4cqw; }
.more8 article { display: grid; gap: .55cqw; }
.more8 img { width: 100%; height: 9.5cqw; object-fit: cover; }
.more8 h4 { font: 700 1.42cqw/1.15 var(--display); font-stretch: 104%; color: var(--spruce); margin: 0; }

/* ---------- section divider ---------- */
.divider { background: var(--spruce); color: var(--on-dark); }
.divider .hero { position: absolute; inset: 0 0 auto 0; height: 70cqw; }
.divider .hero img { width: 100%; height: 100%; object-fit: cover; }
.divider .hero::after { content: ""; position: absolute; inset: 0; background: linear-gradient(to bottom, rgb(21 48 42 / .78) 0%, rgb(21 48 42 / 0) 26%, rgb(21 48 42 / .2) 60%, var(--spruce) 100%); }
.divider .body { position: absolute; left: 6.6cqw; right: 6.6cqw; bottom: 6cqw; display: grid; gap: 2.2cqw; }
.divider .num { font: 500 1.15cqw/1 var(--mono); letter-spacing: .2em; text-transform: uppercase; color: var(--brass-soft); }
.divider h2 { color: var(--on-dark); font-size: 7cqw; font-stretch: 120%; line-height: .96; text-transform: uppercase; }
.divider .intro { color: var(--on-dark-muted); font-size: 1.85cqw; line-height: 1.45; max-width: 62cqw; }
.toc { display: grid; grid-template-columns: 1fr 1fr; gap: 0 4cqw; border-top: .12cqw solid rgb(238 240 234 / .22); }
.toc div { display: flex; justify-content: space-between; align-items: baseline; padding: 1.25cqw 0; border-bottom: .12cqw solid rgb(238 240 234 / .22); }
.toc b { font: 650 1.75cqw/1.2 var(--body); color: var(--on-dark); }
.toc span { font: 500 1.05cqw/1 var(--mono); letter-spacing: .1em; color: var(--brass-soft); }
.divider .topbar { position: absolute; top: 5.4cqw; left: 6.6cqw; right: 6.6cqw; display: flex; justify-content: space-between; z-index: 1; }
.divider .brand { color: var(--on-dark); }

/* ---------- core product extras ---------- */
.badge-core { display: inline-flex; align-items: center; gap: .7cqw; font: 500 1.05cqw/1 var(--mono); letter-spacing: .16em; text-transform: uppercase; color: var(--brass); }
.badge-core i { width: .9cqw; height: .9cqw; background: var(--brass); display: inline-block; }
.why-it { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.6cqw; }
.why-it div { background: var(--spruce); color: var(--on-dark); padding: 1.6cqw 1.8cqw; display: grid; gap: .5cqw; align-content: start; }
.why-it b { font: 720 1.75cqw/1.15 var(--display); font-stretch: 104%; }
.why-it span { font-size: 1.28cqw; line-height: 1.42; color: var(--on-dark-muted); }

/* ---------- journey (6 steps) ---------- */
.journey { flex: 1; min-height: 0; display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: 1fr 1fr; gap: 2.4cqw 2cqw; }
.jstep { display: grid; grid-template-rows: 1fr 13.5cqw; gap: 1.1cqw; min-height: 0; }
.jstep .vis { position: relative; min-height: 0; overflow: hidden; background: var(--spruce); }
.jstep .vis img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.jstep .vis svg.icon { position: absolute; left: 50%; top: 50%; width: 9cqw; height: 9cqw; transform: translate(-50%, -50%); color: var(--brass-soft); }
.jstep .vis .n { position: absolute; left: 1.2cqw; top: 1.2cqw; z-index: 1; background: var(--sheet); color: var(--spruce); font: 800 1.9cqw/1 var(--display); font-stretch: 120%; padding: .55cqw .8cqw; font-variant-numeric: tabular-nums; }
.jstep h3 { font-size: 2.05cqw; }
.jstep p { font-size: 1.3cqw; line-height: 1.42; color: var(--muted); }
.jstep .get { font-size: 1.22cqw; line-height: 1.35; color: var(--ink); }
.jstep .get b { font: 500 .95cqw/1 var(--mono); letter-spacing: .14em; text-transform: uppercase; color: var(--brass); margin-right: .5cqw; }
.jtext { display: grid; gap: .6cqw; }
.flow { display: flex; align-items: center; gap: 1cqw; font: 500 1.02cqw/1 var(--mono); letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }
.flow i { flex: 1; height: .14cqw; background: var(--line); }

/* ---------- FAQ ---------- */
.faq { display: grid; grid-template-columns: 1fr 1fr; gap: 0 3.4cqw; }
.faq div { padding: 3.2cqw 0; border-bottom: .12cqw solid var(--line); display: grid; gap: .7cqw; align-content: start; }
.faq div:nth-child(-n+2) { border-top: .18cqw solid var(--spruce); }
.faq b { font: 700 2.05cqw/1.2 var(--display); font-stretch: 104%; color: var(--spruce); }
.faq p { font-size: 1.52cqw; line-height: 1.55; color: var(--muted); }

/* ---------- next steps (contact) ---------- */
.next3 { margin-top: 3.4cqw; display: grid; grid-template-columns: repeat(3, 1fr); gap: 2cqw; }
.next3 div { border-top: .16cqw solid var(--brass); padding-top: 1.3cqw; display: grid; gap: .6cqw; }
.next3 span { font: 500 1.02cqw/1 var(--mono); letter-spacing: .16em; color: var(--brass-soft); }
.next3 b { font: 650 1.6cqw/1.25 var(--body); color: var(--on-dark); }
.back h2.contact-h { margin-top: 7cqw; }
.cust8 .vis { height: 27cqw; }
'''
style = style.replace('/* ---------- print ---------- */', EXTRA_CSS + NEW_CSS + '\n/* ---------- print ---------- */')

ICONS = '''
    <symbol id="i-custom" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 20l1-4L16 5l3 3L8 19z"/><path d="M14 7l3 3"/><path d="M4 20h16"/></g></symbol>
    <symbol id="i-globe" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.6 2.6 3.8 5.6 3.8 9s-1.2 6.4-3.8 9c-2.6-2.6-3.8-5.6-3.8-9S9.4 5.6 12 3z"/></g></symbol>
    <symbol id="i-design" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="4" width="18" height="16"/><path d="M3 10h9v10"/><path d="M12 14h9"/></g></symbol>
    <symbol id="i-network" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.5"><rect x="9" y="3" width="6" height="5"/><rect x="2" y="16" width="6" height="5"/><rect x="16" y="16" width="6" height="5"/><path d="M12 8v4M5 16v-4h14v4"/></g></symbol>
    <symbol id="i-shield" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 3l8 3v6c0 4.6-3.2 7.8-8 9.5C7.2 19.8 4 16.6 4 12V6z"/><path d="M8.5 12.2l2.4 2.3 4.6-4.9"/></g></symbol>
    <symbol id="i-person" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="8" r="4"/><path d="M4 21c.8-4.2 4-6.5 8-6.5s7.2 2.3 8 6.5"/></g></symbol>
    <symbol id="i-chat" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 5h16v11H10l-4 4v-4H4z"/><path d="M8 9.5h8M8 12.5h5"/></g></symbol>
    <symbol id="i-hand" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.5"><path d="M7.5 9a3 3 0 100 6c1.9 0 3-1.4 4.5-3s2.6-3 4.5-3a3 3 0 110 6c-1.9 0-3-1.4-4.5-3S9.4 9 7.5 9z"/></g></symbol>
    <symbol id="i-phone" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6 3h4l1.5 5-2.5 1.5a11 11 0 005.5 5.5L16 12.5l5 1.5v4a3 3 0 01-3 3C10 21 3 14 3 6a3 3 0 013-3z"/></g></symbol>
    <symbol id="i-talk" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 4h12v8H8l-3 3v-3H3z"/><path d="M15 8h6v8h-2v3l-3-3h-5v-4"/></g></symbol>
  </defs>'''
defs = defs.replace('</defs>', ICONS, 1)

BRAND = '<div class="brand"><svg><use href="#mark"/></svg><span class="word">KIKFIA</span></div>'
def run(label): return '<div class="run">%s<span>%s</span></div>' % (BRAND, label)
FOOT = '<div class="foot"><span>Custom Portable Houses · kikfia.com</span><b>00 / 00</b></div>'

def page(aria, label, inner):
    return '''<section class="page" aria-label="%s">
  <div class="sheet">
    %s
    <div class="content">
%s
    </div>
    %s
  </div>
</section>''' % (aria, run(label), inner, FOOT)

def title(eyebrow, h2, pitch=None, badge=False):
    eb = '<p class="badge-core"><i></i>%s</p>' % eyebrow if badge else '<p class="eyebrow">%s</p>' % eyebrow
    p = '\n        <p class="pitch">%s</p>' % pitch if pitch else ''
    return '''      <div class="title-block">
        %s
        <h2>%s</h2>%s
      </div>''' % (eb, h2, p)

def dash(items): return '<ul class="dash">' + ''.join('<li>%s</li>' % i for i in items) + '</ul>'
def chips(items): return '<div class="chips">' + ''.join('<span class="chip">%s</span>' % i for i in items) + '</div>'
def cols3(feat, ben, cust):
    return '''      <div class="cols3">
        <div><p class="lbl">What's included</p>%s</div>
        <div><p class="lbl">What it means for you</p>%s</div>
        <div><p class="lbl">Make it yours</p>%s</div>
      </div>''' % (dash(feat), dash(ben), chips(cust))

def img(slot): return slot if slot.endswith('.jpg') else I[slot]

def core_page(aria, h2, pitch, hero, hero_alt, thumbs, feat, ben, cust, why, hero_pos='50% 50%'):
    th = ''.join('<figure><img src="img/%s" alt="%s"><figcaption>%s</figcaption></figure>' % (img(f), a, c) for f, c, a in thumbs)
    wy = '      <div class="why-it">' + ''.join('<div><b>%s</b><span>%s</span></div>' % w for w in why) + '</div>'
    inner = '\n'.join([
        title('Core product', h2, pitch, badge=True),
        '      <img class="pp-hero" src="img/%s" alt="%s" style="object-position:%s">' % (img(hero), hero_alt, hero_pos),
        '      <div class="pp-thumbs">%s</div>' % th,
        cols3(feat, ben, cust),
        wy,
    ])
    return page(aria, 'Core Products', inner)

def fig(slot, cap, alt, cls=''):
    c = ' class="%s"' % cls if cls else ''
    return '<figure%s><img src="img/%s" alt="%s"><figcaption>%s</figcaption></figure>' % (c, img(slot), alt, cap)

def category_page(aria, eyebrow, h2, pitch, figs, types):
    m = '      <div class="mosaic">' + ''.join(fig(*f) for f in figs) + '</div>'
    t = '      <div class="types">' + ''.join('<div><b>%s</b><span>%s</span></div>' % x for x in types) + '</div>'
    return page(aria, 'More Solutions', '\n'.join([title(eyebrow, h2, pitch), m, t]))

def extract(aria):
    x = s[s.index('<section class="page" aria-label="%s">' % aria):]
    return x[:x.index('</section>') + len('</section>')]

pages = []

# 01 COVER
pages.append('''<section class="page cover" aria-label="Cover">
  <div class="hero"><img src="img/%s" alt="%s"></div>
  <div class="topbar">
    <div class="brand"><svg><use href="#mark"/></svg><span class="word">KIKFIA</span></div>
    <span class="edition">Product Catalogue · 2026</span>
  </div>
  <div class="bottom">
    <p class="eyebrow">KIKFIA</p>
    <h1>Custom<br>Portable<br>Houses</h1>
    <div class="rule"></div>
    <p class="sub"><strong style="color:var(--on-dark);font-weight:600">Custom Portable Housing Solutions.</strong> ADUs, expandable, tiny and modular homes, plus complete modular buildings for business, hospitality and community projects.</p>
    <div class="lines"><span>ADU Houses</span><span>Expandable Houses</span><span>Tiny Houses</span><span>Modular Homes</span><span>Commercial &amp; Community Projects</span></div>
  </div>
</section>''' % (img('cover'), I.get('cover_alt', 'Modern portable house')))

# 02 ABOUT
pages.append(page('About KIKFIA', 'About KIKFIA', '''      <div class="title-block">
        <p class="eyebrow">About KIKFIA</p>
        <h2>Your partner for portable and modular buildings.</h2>
      </div>
      <div class="about-grid">
        <div class="copy">
          <p class="lead">KIKFIA helps homeowners, investors, businesses and institutions get quality space faster, with a custom design and one team supporting them from first idea to final installation.</p>
          <p>We work with an established network of manufacturing partners and match every project to the right building system: expandable, folding, modular or steel structure. You choose the layout, finishes and options. We coordinate design, production, shipping and installation support.</p>
          <p>Whether you need one backyard ADU or a complete resort, school or workforce site, you get the same care, clear communication and written commitments.</p>
        </div>
        <dl class="facts">
          <div><dt>Sectors served</dt><dd>5</dd></div>
          <div><dt>Project size</dt><dd>1 unit to full sites</dd></div>
          <div><dt>Design</dt><dd>Custom every time</dd></div>
          <div><dt>Build</dt><dd>Factory-made quality</dd></div>
          <div><dt>Delivery</dt><dd>U.S. &amp; worldwide</dd></div>
        </dl>
      </div>
      <img class="band bleed" src="img/%s" alt="Single-story modular villa with full-height glass walls and a landscaped garden">
      <div class="three" style="grid-template-columns:repeat(4,1fr);gap:2.4cqw">
        <div><p class="eyebrow">Mission</p><h3>Better space, sooner.</h3><p>Make quality living and working space faster and simpler to own.</p></div>
        <div><p class="eyebrow">Vision</p><h3>A building for every plan.</h3><p>Adding a home, an office or a whole site should feel easy and predictable.</p></div>
        <div><p class="eyebrow">Quality</p><h3>Confirmed in writing.</h3><p>Materials, sizes and finishes are agreed before production starts.</p></div>
        <div><p class="eyebrow">Customization</p><h3>Built your way.</h3><p>Every design is adapted to your site, your use and your style.</p></div>
      </div>''' % img('about_band')))

# 03 WHY CUSTOMERS TRUST KIKFIA
trust = [
 ('i-custom','Customized Solutions','Every building is planned around your site, your budget and how you will use it.'),
 ('i-globe','International Project Support','We coordinate production, shipping and documents for projects in the U.S. and abroad.'),
 ('i-design','Professional Design Assistance','Floor plans, finishes and drawings are prepared for your approval before anything is built.'),
 ('i-network','Manufacturing Partner Network','Established factories matched to each product, from a single home to a complete site.'),
 ('i-shield','Quality-Focused Approach','Galvanized steel structures, specifications confirmed in writing and checks before shipping.'),
 ('i-person','Customer-Centered Service','One dedicated contact who answers clearly and keeps you informed at every step.'),
 ('i-chat','Project Consultation Support','A free consultation to choose the right model, size and options for your goals.'),
 ('i-hand','Long-Term Cooperation','Support after delivery, plus a partner for repeat orders and multi-phase projects.'),
]
t8 = ''.join('<article><svg><use href="#%s"/></svg><h3>%s</h3><p>%s</p></article>' % x for x in trust)
pages.append(page('Why customers trust KIKFIA', 'Why customers trust us', '''      <div class="title-block">
        <p class="eyebrow">Why customers trust KIKFIA</p>
        <h2>Confidence at every step of your project.</h2>
      </div>
      <div class="trust-hero"><img src="img/%s" alt="Two-story modular building being installed with a crane"><div class="msg"><span>Peace of mind</span><p>One partner from your first question to final installation.</p></div></div>
      <div class="trust8">%s</div>
      <div class="assure"><strong>No surprises.</strong><span>Clear drawings, itemized quotes and a written schedule before production begins.</span></div>''' % (img('trust_hero'), t8)))

# 04 PRODUCTS & SOLUTIONS OVERVIEW (hierarchy)
core = [('ov_adu','ADU Houses','A complete second home for family, guests or rental income.','06'),
        ('ov_exp','Expandable Houses','Ships compact, opens on site into a finished home.','07'),
        ('ov_tiny','Tiny Houses &amp; Cabins','Smart, efficient living in a small footprint.','09'),
        ('ov_mod','Modular Homes','Family homes and villas built from factory modules.','10')]
c4 = ''.join('<article><img src="img/%s" alt="%s"><h3>%s<small>p. %s</small></h3><p>%s</p></article>' % (img(a), b.replace('&amp;','and'), b, d, c) for a, b, c, d in core)
more = [tuple(x) for x in I['more8']]
m8 = ''.join('<article><img src="img/%s" alt="%s"><h4>%s</h4></article>' % (img(a), b.replace('&amp;','and'), b) for a, b in more)
pages.append(page('Products and solutions', 'Products &amp; Solutions', '''      <div class="title-block">
        <p class="eyebrow">Products &amp; solutions</p>
        <h2>Four core products. One partner for every project.</h2>
      </div>
      <div class="lvl"><b>Core products</b><span>Our main focus</span></div>
      <div class="core4">%s</div>
      <div class="lvl"><b>More solutions</b><span>%s</span></div>
      <div class="more8">%s</div>''' % (c4, I['more_pages'], m8)))

# 05 DIVIDER: CORE PRODUCTS
def divider(aria, n, h2, intro, hero, toc):
    tc = ''.join('<div><b>%s</b><span>p. %s</span></div>' % x for x in toc)
    return '''<section class="page divider" aria-label="%s">
  <div class="hero"><img src="img/%s" alt=""></div>
  <div class="topbar">%s<span class="edition">%s</span></div>
  <div class="body">
    <p class="num">%s</p>
    <h2>%s</h2>
    <p class="intro">%s</p>
    <div class="toc">%s</div>
  </div>
</section>''' % (aria, img(hero), BRAND, n, n, h2, intro, tc)
pages.append(divider('Core products', 'Section 01 · Core products', 'Core<br>Products',
  'Our four core product lines cover most homes, rentals and backyard projects. Each one can be customized to your site, budget and style.',
  'div_core', [('ADU Houses','06'),('Expandable Houses','07'),('Tiny Houses &amp; Cabins','09'),('Modular Homes','10')]))

# 06 ADU
pages.append(core_page('ADU Houses', 'ADU Houses &amp; Backyard Studios',
 'A complete second home on your lot for family, guests, a home office or long-term rental income.',
 'adu_hero', 'Single-story ADU house with large windows',
 [('adu_t1','Backyard studio','Backyard studio with glass doors'),('adu_t2','Kitchenette','Bright interior with kitchenette and glass doors'),('adu_t3','Bedroom','Bedroom with white bedding')],
 ['Full kitchen and bathroom','Insulated walls, roof and floor','Wiring and plumbing ready for hookup'],
 ['A separate home without a long build','Can create steady rental income','Drawings to support your permit'],
 ['Floor plan','Cladding','Windows','Roof style','Porch'],
 [('Family close by','Room for parents, adult children or a caregiver.'),('Income potential','A private unit you can rent long-term.'),('Less disruption','Built in a factory, installed quickly on site.')], I.get('adu_pos','50% 55%')))

# 07 EXPANDABLE FEATURE (existing page, friendlier labels)
ef = extract('Expandable Houses')
ef = ef.replace('<p class="eyebrow">Featured product line</p>', '<p class="badge-core"><i></i>Core product</p>')
ef = ef.replace('Products &amp; Solutions</span></div>', 'Core Products</span></div>', 1)
ef = ef.replace('<p class="lbl">Key features</p>', '<p class="lbl">What\'s included</p>').replace('<p class="lbl">Benefits</p>', '<p class="lbl">What it means for you</p>').replace('<p class="lbl">Customize</p>', '<p class="lbl">Make it yours</p>')
ef = ef.replace('Ships as a compact unit and unfolds on site into a finished home almost three times its closed width.', 'Arrives as a compact unit and opens on site into a finished, ready-to-live home almost three times wider.')
ef = ef.replace('src="img/expandable-40.jpg"', 'src="img/%s"' % img('exp_hero'))
a = ef.index('<div class="strip">'); b = ef.index('</div>', a) + len('</div>')
ef = ef[:a] + '<div class="strip">' + ''.join('<figure><img src="img/%s" alt="%s"><figcaption>%s</figcaption></figure>' % (img(x[0]), x[2], x[1]) for x in I['exp_strip']) + '</div>' + ef[b:]
pages.append(ef)

# 08 EXPANDABLE IN REAL PROJECTS
er = I['exp_projects']
_m = '      <div class="mosaic">' + ''.join(fig(*f) for f in er['figs']) + '</div>'
_t = '      <div class="types">' + ''.join('<div><b>%s</b><span>%s</span></div>' % tuple(x) for x in er['types']) + '</div>'
pages.append(page('Expandable houses in real projects', 'Core Products', '\n'.join([title('Expandable houses · Real projects', er['h2'], er['pitch'], badge=True), _m, _t])))

# 09 TINY & CABINS
pages.append(core_page('Tiny Houses and Cabins', 'Tiny Houses &amp; Cabins',
 'Smart, efficient living in a small footprint, for first homes, retreats and vacation rentals.',
 'tiny_hero', 'Modern tiny house',
 [('tiny_t1','Built for winter','Cabin in deep snow'),('tiny_t2','Studio pod','Black studio pod with glass door'),('tiny_t3','Compact kitchen','Compact kitchen inside a tiny house')],
 ['Insulated steel or composite shell','Large windows and glass doors','Compact kitchen and full bathroom'],
 ['Lower cost to own and run','Easy to move to a new site','Strong appeal for short-term rentals'],
 ['Exterior color','Glass walls','Sleeping loft','Deck &amp; steps','Heating &amp; A/C'],
 [('Affordable','A full home at a fraction of a traditional build.'),('Flexible','Place it on land, a backyard or a campground.'),('Rental-ready','Guests love a modern, design-led stay.')], I.get('tiny_pos','50% 50%')))

# 10 MODULAR HOMES
pages.append(core_page('Modular Homes', 'Modular Homes',
 'Factory-built modules joined into spacious family homes and modern villas, one or two stories.',
 'mod_hero', 'Modular home',
 [('mod_t1','Glass-walled villa','Modular villa with full-height glass'),('mod_t2','Stacked modules','White stacked modules forming a two-story home'),('mod_t3','Villa with garden','Modular villa with landscaped garden')],
 ['Stackable steel modules','Open-plan or multi-bedroom layouts','Full-height glass, balconies and stairs'],
 ['Factory quality, fewer site delays','More predictable cost and schedule','Add modules as your family grows'],
 ['Module count','Floor plan','Facade','Glass walls','Finishes'],
 [('Space to grow','From two bedrooms to large family layouts.'),('Modern design','Clean lines, big glass, quality finishes.'),('Predictable','A clear quote and schedule from day one.')], I.get('mod_pos','50% 55%')))

# 11 INTERIORS
_f = ''.join('<figure><div class="ph"><img src="img/%s" alt="%s"></div><figcaption>%s</figcaption></figure>' % (img(x[0]), x[2], x[1]) for x in I['interiors'])
pages.append(page('Interiors', 'Interiors', '''      <div class="title-block">
        <p class="eyebrow">Interiors</p>
        <h2>Finished inside, not just outside.</h2>
        <p class="pitch">Kitchens, bathrooms, living and work spaces are finished before delivery, so you can move in or open sooner.</p>
      </div>
      <div class="interiors">%s</div>
      <div class="finishes">
        <div><span>Walls</span><b>Sandwich panel or bamboo-wood finish</b></div>
        <div><span>Floors</span><b>SPC or vinyl plank</b></div>
        <div><span>Kitchens</span><b>Cabinets, sink and counters</b></div>
        <div><span>Bathrooms</span><b>Wet and dry areas, full fixtures</b></div>
      </div>''' % _f))

# 12 DIVIDER: MORE SOLUTIONS
pages.append(divider('More solutions', 'Section 02 · More solutions', 'More<br>Solutions',
  'The same building systems also deliver villas, offices, resorts, warehouses, schools and clinics, from a single unit to a complete site.',
  'div_more', [tuple(x) for x in I['more_toc']]))

# 13-17 SECONDARY
for spec in I['secondary']:
    pages.append(category_page(spec['aria'], spec['eyebrow'], spec['h2'], spec['pitch'], [tuple(f) for f in spec['figs']], [tuple(t) for t in spec['types']]))

# 18 CUSTOMIZATION (re-generated with same content as before)
swatch6 = '<div class="vis swatch6"><i style="background:#F4F4F1"></i><i style="background:#1D2022"></i><i style="background:#5C6266"></i><i style="background:repeating-linear-gradient(90deg,#9A6233 0 .5cqw,#A86C3A .5cqw 1.1cqw,#8F5A2E 1.1cqw 1.5cqw)"></i><i style="background:#B9BDB8"></i><i style="background:#CDBFA6"></i></div>'
mats = '<div class="vis mats"><div class="m-wood">Woodgrain</div><div class="m-metal">Metal cladding</div><div class="m-bamboo">Bamboo-wood</div><div class="m-panel">Sandwich panel</div></div>'
sizes = '<div class="vis sizes">' + ''.join('<div class="row"><span>%d FT</span><div class="bar">%s</div></div>' % (10*n, '<i></i>'*n) for n in (1,2,3,4)) + '</div>'
c8 = [
 ('<svg class="vis" viewBox="0 0 240 200" role="img" aria-label="Example floor plan with living room, kitchen, two bedrooms and bathroom" style="padding:4%"><g fill="none" stroke="#15302A" stroke-width="3"><rect x="10" y="10" width="220" height="180"/><path d="M120 10v70M10 110h110M120 110v80M120 80h110M175 110v80"/><path d="M120 110h55"/></g><g fill="#B08A4E"><rect x="60" y="107" width="22" height="6"/><rect x="132" y="77" width="22" height="6"/><rect x="117" y="140" width="6" height="20"/><rect x="172" y="140" width="6" height="18"/></g><g font-family="IBM Plex Mono, monospace" font-size="11" fill="#17201D" text-anchor="middle"><text x="65" y="62">LIVING</text><text x="175" y="50">KITCHEN</text><text x="65" y="155">BED 1</text><text x="147" y="155">BATH</text><text x="203" y="155">BED 2</text></g><g font-family="IBM Plex Mono, monospace" font-size="8" fill="#59655F" text-anchor="middle"><text x="120" y="6">40 FT</text></g></svg>', 'Floor Plans', 'Open plan or one to three bedrooms, arranged around how you live.'),
 ('<img class="vis contain" src="img/%s" alt="3D cutaway of a one-bedroom layout">' % img('cust_layout'), 'Interior Layout', 'Move walls, kitchens and bathrooms. Add storage and built-ins.'),
 ('<img class="vis" src="img/%s" alt="House with covered veranda">' % img('cust_ext'), 'Exterior Design', 'Verandas, canopies, decks, stairs and roof styles.'),
 (swatch6, 'Colors', 'Frame and wall colors from white and black to woodgrain and sand.'),
 ('<img class="vis" src="img/%s" alt="House with large glass windows">' % img('cust_win'), 'Windows', 'Sliding, awning or floor-to-ceiling glass, single or double glazed.'),
 ('<img class="vis" src="img/%s" alt="House with glass and solid doors">' % img('cust_door'), 'Doors', 'Steel security, glass sliding or hinged aluminum doors.'),
 (mats, 'Materials', 'Choose wall panels, cladding, flooring and countertops.'),
 (sizes, 'Sizes', 'Standard 10–40 ft modules, combined side by side or stacked.'),
]
c8h = ''.join('<article>%s<h3>%s</h3><p>%s</p></article>' % x for x in c8)
pages.append(page('Customization', 'Customization', '''      <div class="title-block">
        <p class="eyebrow">Customization</p>
        <h2>Designed around you.</h2>
        <p class="pitch">Choose what matters to you. We turn your choices into drawings you approve before anything is built.</p>
      </div>
      <div class="cust8">%s</div>
      <div class="project-band"><strong>Have your own design?</strong><span>Send us your drawings or site plan and we will adapt our building systems to fit.</span></div>''' % c8h))

# 19-20 GALLERIES
for g in I['galleries']:
    tiles = ''.join(fig(*t) for t in g['tiles'])
    pages.append(page(g['aria'], 'Project Gallery', '''      <div class="title-block">
        <p class="eyebrow">%s</p>
        <h2>%s</h2>
      </div>
      <div class="gal" style="%s">%s</div>
      <p class="fine">%s</p>''' % (g['eyebrow'], g['h2'], g.get('grid',''), tiles, g['note'])))

# 21 HOW WE WORK
J = [
 (None, 'i-phone', '01', 'Consultation', 'Tell us about your site, budget and goals. We recommend the right products.', 'Model suggestions and a budget range'),
 (None, 'i-talk', '02', 'Project Discussion', 'We confirm quantities, timeline, delivery location and local requirements.', 'A clear project scope'),
 ('j_design', None, '03', 'Design &amp; Customization', 'Your layout, finishes and options become drawings for your approval.', 'Approved drawings and written quote'),
 ('j_make', None, '04', 'Manufacturing', 'Your building is made to the approved specification in the factory.', 'Progress updates and a pre-shipment check'),
 ('j_ship', None, '05', 'Delivery', 'We arrange packing, freight and delivery to your site or nearest port.', 'Shipping schedule and documents'),
 ('j_install', None, '06', 'Installation Support', 'Guides and direct help while your local crew sets the building.', 'Installation guide and ongoing support'),
]
def jstep(x):
    slot, icon, n, h, p, g = x
    vis = '<img src="img/%s" alt="">' % img(slot) if slot else '<svg class="icon"><use href="#%s"/></svg>' % icon
    return '<div class="jstep"><div class="vis"><span class="n">%s</span>%s</div><div class="jtext"><h3>%s</h3><p>%s</p><p class="get"><b>You get</b>%s</p></div></div>' % (n, vis, h, p, g)
pages.append(page('How we work', 'How we work', '''      <div class="title-block">
        <p class="eyebrow">How we work</p>
        <h2>Six simple steps to your new building.</h2>
        <p class="pitch">You always know what happens next, what you receive and what we need from you.</p>
      </div>
      <div class="journey">%s</div>''' % ''.join(jstep(x) for x in J)))

# 22 PROMISE (why customers choose)
pill = [
 ('Reliability','We do what we quote, on the schedule we agree, and keep you informed at every step.'),
 ('Customization','Your layout, finishes, colors and size. Every project is adapted to you.'),
 ('Quality','Galvanized steel structures, quality finishes and a check before every shipment.'),
 ('Transparency','Itemized quotes listing the building, options, shipping and what is not included.'),
 ('Long-Term Support','Documents, installation guidance and help with questions long after delivery.'),
]
ph = ''.join('<div><h3>%s</h3><p>%s</p></div>' % x for x in pill)
ph += '<div class="note-cell"><h3>Small or large</h3><p>One studio or a multi-building site, you get the same care and one point of contact.</p></div>'
pages.append(page('Why customers choose KIKFIA', 'Our promise', '''      <div class="title-block">
        <p class="eyebrow">Why customers choose KIKFIA</p>
        <h2>Peace of mind, built in.</h2>
      </div>
      <div class="pillars">%s</div>
      <div class="quality">
        <div>
          <p class="eyebrow" style="margin-bottom:1.2cqw">Commitment to quality</p>
          <ul class="checks">
            <li><svg><use href="#check"/></svg><div><b>Galvanized steel structure</b><span>Corrosion-resistant frames on every building.</span></div></li>
            <li><svg><use href="#check"/></svg><div><b>Everything confirmed in writing</b><span>Materials, sizes, finishes and options before production.</span></div></li>
            <li><svg><use href="#check"/></svg><div><b>Production updates</b><span>Photos and progress reports while your building is made.</span></div></li>
            <li><svg><use href="#check"/></svg><div><b>Pre-shipment check</b><span>Finishes and fittings reviewed before shipping.</span></div></li>
            <li><svg><use href="#check"/></svg><div><b>Drawings and guides included</b><span>Documentation for your installer and permit office.</span></div></li>
            <li><svg><use href="#check"/></svg><div><b>One point of contact</b><span>A dedicated person who knows your project.</span></div></li>
          </ul>
        </div>
        <div class="photo"><img src="img/%s" alt="%s"></div>
      </div>''' % (ph, img('promise_photo'), I.get('promise_alt','Finished modular building'))))

# 23 FAQ
faq = [
 ('Can I change the floor plan?', 'Yes. Every model can be adapted: walls, kitchen, bathroom, windows, doors and finishes. You approve the drawings before production.'),
 ('Do I need a permit?', 'Rules differ by city and county. We provide drawings and specifications to support your application. Your local authority makes the final decision.'),
 ('What do I prepare on site?', 'A level foundation (slab, piers or screw piles) and utility connections, arranged with a local contractor. We share the foundation and connection details.'),
 ('How is my building delivered?', 'Units ship in standard containers, flat-packed or as expandable modules. We coordinate freight to your site or nearest port and send all shipping documents.'),
 ('How long does it take?', 'It depends on the model, customization and quantity. Your written quote includes a production and shipping schedule.'),
 ('What is included in the price?', 'Your itemized quote lists the building, options, packing and shipping, plus anything not included, such as foundations and local installation.'),
 ('Do you help with installation?', 'Yes. You receive installation guides and drawings, and we support your local crew directly during setup.'),
 ('Can you handle large projects?', 'Yes. Through our manufacturing partner network we support single homes through resorts, camps and multi-building sites, delivered in phases if needed.'),
]
fq = ''.join('<div><b>%s</b><p>%s</p></div>' % x for x in faq)
pages.append(page('Frequently asked questions', 'FAQ', '''      <div class="title-block">
        <p class="eyebrow">Questions buyers ask</p>
        <h2>Straight answers before you start.</h2>
      </div>
      <div class="faq">%s</div>
      <div class="assure" style="margin-top:auto"><strong>Still have questions?</strong><span>Book a free consultation. We will walk you through options, timing and costs for your site.</span></div>''' % fq))

# 24 CONTACT
bk = s[s.index('<section class="page back"'):]
bk = bk[:bk.index('</section>') + len('</section>')]
bk = bk.replace('<h2>Let\'s plan<br>your house.</h2>', '<h2 class="contact-h">Let\'s plan<br>your project.</h2>')
bk = bk.replace('Tell us where it is going and how you will use it. We will recommend a model, share layout options and send a written quote.',
                'Tell us what you want to build, where it is going and your budget. We will recommend the right solution and send a clear, written quote.')
nxt = '''<div class="next3"><div><span>01</span><b>Send us your idea, location and budget</b></div><div><span>02</span><b>Free consultation to choose models and options</b></div><div><span>03</span><b>Receive drawings and an itemized quote</b></div></div>
    <div class="cta">'''
bk = bk.replace('<div class="cta">', nxt, 1)
bk = bk.replace('<strong>Free design consultation</strong><span>Share your site, size and budget and get model recommendations within your first call.</span>',
                '<strong>Book your free project consultation</strong><span>Call, email or message us on Facebook and Instagram to get started.</span>')
pages.append(bk)

total = len(pages)
pages = [re.sub(r'<b>\d\d / \d+</b>', '<b>%02d / %d</b>' % (i + 1, total), pg) for i, pg in enumerate(pages)]
body = '\n\n'.join(pages)
head = s[:s.index('<style>')]
open(OUT, 'w').write(head + style + '\n\n' + defs + '\n\n' + body + '\n')
print('pages', total)
