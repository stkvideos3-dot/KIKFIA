# Usage: python3 build.py <base catalogue html>  (rebuilds the 24-page layout in place)
# Builds catalogue/kikfia-catalogue.html from page templates.
# Reuses the existing <style> and SVG defs, adds new layout CSS, renumbers footers.
import re, sys, html

SRC = sys.argv[1]
s = open(SRC).read()
style = s[s.index('<style>'):s.index('</style>') + len('</style>')]
defs = s[s.index('<svg width="0"'):]
defs = defs[:defs.index('</svg>') + len('</svg>')]

EXTRA_CSS = r'''
/* ---------- product page (pp) ---------- */
.pp-hero { flex: 1; min-height: 30cqw; height: auto; width: 100%; object-fit: cover; }
.pp-thumbs { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.2cqw; }
.pp-thumbs figure { margin: 0; display: grid; gap: .6cqw; }
.pp-thumbs img { height: 17cqw; width: 100%; object-fit: cover; background: var(--paper); }
.ideal { display: flex; align-items: center; flex-wrap: wrap; gap: 1.2cqw 1.6cqw; padding-top: 1.6cqw; border-top: .12cqw solid var(--line); }
.ideal .k { font: 500 1.02cqw/1 var(--mono); letter-spacing: .15em; text-transform: uppercase; color: var(--brass); }

/* ---------- solutions overview ---------- */
.sol { display: grid; grid-template-columns: 1fr 1fr; gap: 2.6cqw 2.8cqw; }
.sol article { display: grid; gap: 1cqw; align-content: start; min-width: 0; }
.sol img { width: 100%; height: 18.5cqw; object-fit: cover; }
.sol h3 { font-size: 2.3cqw; }
.sol .chips .chip { font-size: 1.28cqw; }
.sol .statement { background: var(--spruce); color: var(--on-dark); padding: 2.6cqw; align-content: center; gap: 1.4cqw; }
.sol .statement p.big { font: 700 2.25cqw/1.25 var(--display); font-stretch: 104%; color: var(--on-dark); }
.sol .statement p { color: var(--on-dark-muted); font-size: 1.4cqw; }

/* ---------- category mosaic ---------- */
.mosaic { flex: 1; min-height: 0; display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: repeat(3, 1fr); gap: 1.2cqw; }
.mosaic figure, .gal figure { margin: 0; position: relative; overflow: hidden; min-height: 0; background: var(--paper); }
.mosaic img, .gal img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.mosaic figcaption, .gal figcaption { position: absolute; left: 0; right: 0; bottom: 0; padding: 2.6cqw 1.2cqw 1cqw; color: #fff; background: linear-gradient(to top, rgb(8 20 16 / .74), rgb(8 20 16 / 0)); }
.m-big { grid-column: span 2; grid-row: span 2; }
.types { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.4cqw 2cqw; padding-top: 1.8cqw; border-top: .18cqw solid var(--spruce); }
.types div { display: grid; gap: .45cqw; align-content: start; }
.types b { font: 700 1.55cqw/1.15 var(--display); font-stretch: 104%; color: var(--spruce); }
.types span { font-size: 1.22cqw; line-height: 1.4; color: var(--muted); }

/* ---------- gallery ---------- */
.gal { flex: 1; min-height: 0; display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: repeat(4, 1fr); gap: 1.2cqw; }
.g-big { grid-column: span 2; grid-row: span 2; }
.g-tall2 { grid-row: span 2; }
.stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2cqw; padding-top: 1.6cqw; border-top: .18cqw solid var(--spruce); }
.stats div { display: grid; gap: .5cqw; }
.stats b { font: 760 2.1cqw/1.1 var(--display); font-stretch: 110%; color: var(--spruce); }
.stats span { font-size: 1.2cqw; line-height: 1.4; color: var(--muted); }

/* ---------- why choose (6) ---------- */
.why6 { display: grid; grid-template-columns: 1fr 1fr; gap: 0 3.2cqw; }
.why6 .reason { grid-template-columns: 2.6cqw 1fr; column-gap: 1.2cqw; }
.why6 .reason svg { width: 2.1cqw; height: 2.1cqw; color: var(--brass); grid-row: span 2; margin-top: .2cqw; }
.why6 .reason:nth-child(-n+2) { padding-top: 0; }
.why-band { flex: 1; min-height: 30cqw; height: auto; width: calc(100% + 13.2cqw); object-fit: cover; object-position: 50% 45%; }

/* ---------- customization (8) ---------- */
.cust8 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2.6cqw 1.8cqw; }
.cust8 article { display: grid; gap: .9cqw; align-content: start; min-width: 0; }
.cust8 .vis { height: 24cqw; width: 100%; object-fit: cover; background: #fff; border: .12cqw solid var(--line); display: block; }
.cust8 img.vis.contain { object-fit: contain; }
.cust8 h3 { font-size: 2cqw; }
.cust8 p { font-size: 1.36cqw; line-height: 1.42; color: var(--muted); }
.vis.swatch6 { display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: repeat(2, 1fr); gap: .5cqw; padding: .8cqw; }
.vis.swatch6 i { display: block; border: .12cqw solid var(--line); }
.vis.mats { display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: .5cqw; padding: .8cqw; }
.vis.mats div { display: flex; align-items: flex-end; padding: .5cqw .6cqw; font: 500 .85cqw/1.1 var(--mono); letter-spacing: .08em; text-transform: uppercase; }
.m-wood { background: repeating-linear-gradient(90deg, #9A6233 0 .5cqw, #A86C3A .5cqw 1.1cqw, #8F5A2E 1.1cqw 1.5cqw); color: #fff; }
.m-metal { background: repeating-linear-gradient(90deg, #6E7479 0 1.6cqw, #5C6266 1.6cqw 1.9cqw); color: #fff; }
.m-bamboo { background: repeating-linear-gradient(90deg, #D9C39A 0 .9cqw, #CDB487 .9cqw 1.4cqw); color: #3b2d17; }
.m-panel { background: repeating-linear-gradient(0deg, #F1F1EE 0 2.4cqw, #D8DAD5 2.4cqw 2.55cqw); color: #3a3f3c; }
.vis.sizes { display: grid; align-content: center; gap: 1cqw; padding: 1.4cqw; }
.vis.sizes .row { display: grid; grid-template-columns: 4.6cqw 1fr; align-items: center; gap: .8cqw; font: 500 1cqw/1 var(--mono); color: var(--muted); }
.vis.sizes .bar { display: flex; gap: .25cqw; height: 1.8cqw; }
.vis.sizes .bar i { flex: 0 0 calc(25% - .19cqw); background: var(--spruce-2); }
.project-band { display: flex; justify-content: space-between; align-items: center; gap: 3cqw; background: var(--spruce); color: var(--on-dark); padding: 2.4cqw 2.8cqw; }
.project-band strong { font: 760 2.2cqw/1.15 var(--display); font-stretch: 108%; }
.project-band span { font-size: 1.36cqw; color: var(--on-dark-muted); max-width: 46cqw; line-height: 1.45; }

/* ---------- process (visual) ---------- */
.steps.tight .step { padding: 1.6cqw 0; }
.pstrip { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.2cqw; flex: 1; min-height: 0; }
.pstrip figure { margin: 0; display: grid; grid-template-rows: 1fr auto; gap: .7cqw; min-height: 0; }
.pstrip .ph { position: relative; min-height: 0; }
.pstrip .ph img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.pstrip figcaption b { color: var(--brass); font-weight: 500; margin-right: .6cqw; }

/* ---------- pillars ---------- */
.pillars { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2.4cqw 2.8cqw; }
.pillars > div { display: grid; gap: .8cqw; align-content: start; border-top: .18cqw solid var(--spruce); padding-top: 1.4cqw; }
.pillars h3 { font-size: 2.1cqw; }
.pillars p { font-size: 1.36cqw; color: var(--muted); }
.pillars .note-cell { background: var(--spruce); border-top-color: var(--brass); padding: 1.6cqw 1.8cqw; }
.pillars .note-cell h3 { color: var(--on-dark); }
.pillars .note-cell p { color: var(--on-dark-muted); }
.range .card img { height: 27cqw; }
.range { gap: 3.2cqw 1.8cqw; }
'''
style = style.replace('/* ---------- print ---------- */', EXTRA_CSS + '\n/* ---------- print ---------- */')

def esc(t): return t
BRAND = '<div class="brand"><svg><use href="#mark"/></svg><span class="word">KIKFIA</span></div>'
def run(label): return '<div class="run">%s<span>%s</span></div>' % (BRAND, label)
FOOT = '<div class="foot"><span>Custom Portable Houses · kikfia.com</span><b>00 / 00</b></div>'

def page(aria, label, inner, sheet_style=''):
    st = ' style="%s"' % sheet_style if sheet_style else ''
    return '''<section class="page" aria-label="%s">
  <div class="sheet"%s>
    %s
    <div class="content">
%s
    </div>
    %s
  </div>
</section>''' % (aria, st, run(label), inner, FOOT)

def title(eyebrow, h2, pitch=None):
    p = '\n        <p class="pitch">%s</p>' % pitch if pitch else ''
    return '''      <div class="title-block">
        <p class="eyebrow">%s</p>
        <h2>%s</h2>%s
      </div>''' % (eyebrow, h2, p)

def dash(items): return '<ul class="dash">' + ''.join('<li>%s</li>' % i for i in items) + '</ul>'
def chips(items): return '<div class="chips">' + ''.join('<span class="chip">%s</span>' % i for i in items) + '</div>'
def cols3(feat, ben, cust):
    return '''      <div class="cols3">
        <div><p class="lbl">Key features</p>%s</div>
        <div><p class="lbl">Benefits</p>%s</div>
        <div><p class="lbl">Customize</p>%s</div>
      </div>''' % (dash(feat), dash(ben), chips(cust))

def product_page(aria, eyebrow, h2, pitch, hero, hero_alt, thumbs, feat, ben, cust, ideal, hero_pos='50% 50%'):
    th = ''.join('<figure><img src="img/%s" alt="%s"><figcaption>%s</figcaption></figure>' % (f, a, c) for f, c, a in thumbs)
    inner = '\n'.join([
        title(eyebrow, h2, pitch),
        '      <img class="pp-hero" src="img/%s" alt="%s" style="object-position:%s">' % (hero, hero_alt, hero_pos),
        '      <div class="pp-thumbs">%s</div>' % th,
        cols3(feat, ben, cust),
        '      <div class="ideal"><span class="k">Ideal for</span>%s</div>' % chips(ideal),
    ])
    return page(aria, 'Products &amp; Solutions', inner)

def fig(img, cap, alt, cls=''):
    c = ' class="%s"' % cls if cls else ''
    return '<figure%s><img src="img/%s" alt="%s"><figcaption>%s</figcaption></figure>' % (c, img, alt, cap)

def category_page(aria, label, eyebrow, h2, pitch, figs, types):
    m = '      <div class="mosaic">' + ''.join(fig(*f) for f in figs) + '</div>'
    t = '      <div class="types">' + ''.join('<div><b>%s</b><span>%s</span></div>' % x for x in types) + '</div>'
    return page(aria, label, '\n'.join([title(eyebrow, h2, pitch), m, t]))

pages = []

# 1 COVER
pages.append('''<section class="page cover" aria-label="Cover">
  <div class="hero"><img src="img/backyard-studio.jpg" alt="Wood-clad backyard studio with glass doors and a solar roof"></div>
  <div class="topbar">
    <div class="brand"><svg><use href="#mark"/></svg><span class="word">KIKFIA</span></div>
    <span class="edition">Product Catalogue · 2026</span>
  </div>
  <div class="bottom">
    <p class="eyebrow">KIKFIA</p>
    <h1>Custom<br>Portable<br>Houses</h1>
    <div class="rule"></div>
    <p class="sub"><strong style="color:var(--on-dark);font-weight:600">Custom Portable Housing Solutions.</strong> Homes, offices, hospitality and modular buildings, designed around your project.</p>
    <div class="lines"><span>Residential</span><span>Commercial</span><span>Hospitality</span><span>Industrial &amp; Storage</span><span>Institutional</span></div>
  </div>
</section>''')

# 2 ABOUT
pages.append(page('About KIKFIA', 'About KIKFIA', '''      <div class="title-block">
        <p class="eyebrow">About KIKFIA</p>
        <h2>Factory-built houses, designed around you.</h2>
      </div>
      <div class="about-grid">
        <div class="copy">
          <p class="lead">KIKFIA is a portable housing and modular building company serving homeowners, investors, businesses and institutions.</p>
          <p>We combine proven factory-built steel structures with the layout, finishes and features each customer needs. A backyard studio, a family ADU, a resort or a staff camp all start the same way: a conversation about your site, your budget and how the space will be used.</p>
          <p>From there we choose the right building system, adapt the design and manage production, shipping and installation support until your building is standing on site.</p>
        </div>
        <dl class="facts">
          <div><dt>Solution sectors</dt><dd>5</dd></div>
          <div><dt>Project size</dt><dd>1 unit to full sites</dd></div>
          <div><dt>Structure</dt><dd>Galvanized steel</dd></div>
          <div><dt>Build</dt><dd>Factory-made</dd></div>
          <div><dt>Delivery</dt><dd>U.S. &amp; worldwide</dd></div>
        </dl>
      </div>
      <img class="band bleed" src="img/villa-panorama.jpg" alt="Single-story modular villa with full-height glass walls and a landscaped garden">
      <div class="three" style="grid-template-columns:repeat(4,1fr);gap:2.4cqw">
        <div><p class="eyebrow">Mission</p><h3>Better space, sooner.</h3><p>Make quality living and working space faster and more affordable to own.</p></div>
        <div><p class="eyebrow">Vision</p><h3>A building for every plan.</h3><p>Adding a home, an office or a whole site should be as simple as choosing the right design.</p></div>
        <div><p class="eyebrow">Quality</p><h3>Checked in writing.</h3><p>Materials, sizes and finishes are confirmed before production starts.</p></div>
        <div><p class="eyebrow">Customization</p><h3>Built your way.</h3><p>Every project is adapted to the customer's site, use and style.</p></div>
      </div>'''))

# 3 WHY CHOOSE
reasons = [
 ('Custom Designs', 'Start from a proven model and change what matters: layout, finishes, windows, colors and size.'),
 ('Flexible Solutions', 'One unit or a full site. Expandable, folding and modular systems for every budget.'),
 ('Quality Manufacturing', 'Galvanized steel frames and factory production, with specs confirmed in writing.'),
 ('Professional Support', 'Drawings, shipping coordination and installation guidance from start to finish.'),
 ('Modern Housing Solutions', 'Clean modern designs with large glass, quality finishes and efficient layouts.'),
 ('Customer-Focused Approach', 'One point of contact, clear written quotes and straight answers.'),
]
r = ''.join('<div class="reason"><svg><use href="#check"/></svg><h3>%s</h3><p>%s</p></div>' % x for x in reasons)
pages.append(page('Why choose KIKFIA', 'Why choose KIKFIA', '''      <div class="title-block">
        <p class="eyebrow">Why choose KIKFIA</p>
        <h2>Six reasons customers build with us.</h2>
      </div>
      <img class="why-band bleed" src="img/p-office-2storey-install.jpg" alt="Two-story modular office building being installed with a crane">
      <div class="why6">%s</div>''' % r))

# 4 SOLUTIONS OVERVIEW
sol = [
 ('p-resort-villas-aerial.jpg', 'Residential', 'Aerial view of pitched-roof villas among trees',
  ['ADU Houses','Tiny Houses','Expandable Houses','Folding Houses','Modular Homes','Family Homes','Luxury &amp; Modern Villas','Holiday Homes','Guest Houses','Backyard Studios']),
 ('p-sales-center-night.jpg', 'Commercial', 'Two-story modular sales center with terrace at dusk',
  ['Portable Offices','Office Buildings','Sales Offices','Showrooms','Retail Shops','Cafés','Restaurants','Commercial Buildings']),
 ('commercial.jpg', 'Hospitality', 'Row of colorful raised container hotel units',
  ['Resort Villas','Hotel Units','Eco Lodges','Glamping Units','Tourist Accommodation']),
 ('p-steel-warehouse-frame.jpg', 'Industrial &amp; Storage', 'Steel frame of a large warehouse under construction',
  ['Warehouses','Storage Units','Workshop Buildings','Industrial Buildings','Site Facilities']),
 ('p-kindergarten-glass.jpg', 'Institutional', 'Modular kindergarten with glass walls and a garden',
  ['Schools','Classrooms','Training Centers','Medical Clinics','Healthcare Facilities','Labor Camps','Staff Accommodation']),
]
cards = ''.join('<article><img src="img/%s" alt="%s"><h3>%s</h3>%s</article>' % (i, a, h, chips(c)) for i, h, a, c in sol)
cards += '<article class="statement"><p class="eyebrow" style="color:var(--brass-soft)">Any size, any use</p><p class="big">No matter the project size or requirements, KIKFIA delivers customized portable housing and modular building solutions.</p><p>From a single backyard studio to a complete resort, school or workforce camp.</p></article>'
pages.append(page('Solutions overview', 'Solutions', '''      <div class="title-block">
        <p class="eyebrow">Our solutions</p>
        <h2>One partner for every project.</h2>
      </div>
      <div class="sol">%s</div>''' % cards))

# 5 ADU
pages.append(product_page('ADU Houses', 'Residential', 'ADU Houses',
 'A complete second home on your lot for family, a caregiver or long-term rental income.',
 'adu.jpg', 'Single-story white ADU house with large windows',
 [('hip-roof-veranda.jpg','Covered veranda','Small house with hip roof and covered veranda'),
  ('int-living.jpg','Living area','Living room inside a modular house'),
  ('int-kitchen.jpg','Full kitchen','Kitchen inside a modular house')],
 ['Full kitchen and bathroom','Insulated walls, roof and floor','Wiring and plumbing ready for hookup'],
 ['A separate home without a traditional build','Can create steady rental income','Drawings and specs for your permit'],
 ['Floor plan','Cladding','Windows','Roof style','Porch'],
 ['Family members','Caregivers','Long-term rental','Home office'], '50% 55%'))

# 6 TINY
pages.append(product_page('Tiny Houses', 'Residential', 'Tiny Houses',
 'A full home in a small footprint, with smart layouts for sleeping, cooking and a complete bathroom.',
 'tiny.jpg', 'Two black container-style tiny houses with glass doors',
 [('black-container-tiny-home-side.jpg','Steel shell','Black tiny house seen from the side with glass doors'),
  ('i-container-kitchen.jpg','Compact kitchen','White kitchen inside a container tiny house'),
  ('r-glass-front.jpg','Glass-front model','Tiny house with full glass front')],
 ['Steel container-style shell','Glass doors for natural light','Compact kitchen and bathroom'],
 ['Lower cost to own and run','Easy to move to a new site','Great for rentals and retreats'],
 ['Exterior color','Glass walls','Sleeping layout','Deck &amp; steps'],
 ['First homes','Short-term rentals','Retreats','Downsizing']))

# 7 EXPANDABLE (existing featured page, kept)
exp_feature = s[s.index('<section class="page" aria-label="Expandable Houses">'):]
exp_feature = exp_feature[:exp_feature.index('</section>') + len('</section>')]
pages.append(exp_feature)

# 8 EXPANDABLE RANGE (existing)
exp_range = s[s.index('<section class="page" aria-label="Expandable model range">'):]
exp_range = exp_range[:exp_range.index('</section>') + len('</section>')]
pages.append(exp_range)

# 9 FOLDING
pages.append(product_page('Folding Houses', 'Residential · Site', 'Folding Houses',
 'Folds flat for shipping and opens on site. The fastest, most economical way to add space.',
 'folding.jpg', '40 ft folding container house with woodgrain walls',
 [('f-two-story.jpg','Stacked two levels','Two-story folding house with exterior stairs'),
  ('p-site-units-black-roof.jpg','Units on site','Folding units with black roofs installed on site'),
  ('p-factory-expandable-line.jpg','Factory finished','Finished units with woodgrain walls in the factory')],
 ['Galvanized steel frame, bolted connections','2–3 in insulated sandwich panels','Join side by side or stack 3 levels'],
 ['Many units ship in one container','Small units set up without a crane','Reusable and relocatable'],
 ['Bath module','Kitchen','Partitions','Doors &amp; windows','Color'],
 ['Fast housing','Site offices','Camps','Emergency space']))

# 10 FOLDING RANGE (existing)
fold_range = s[s.index('<section class="page" aria-label="Folding and flat-pack range">'):]
fold_range = fold_range[:fold_range.index('</section>') + len('</section>')]
pages.append(fold_range)

# 11 MODULAR HOMES & VILLAS
pages.append(product_page('Modular Homes and Villas', 'Residential', 'Modular Homes &amp; Villas',
 'Factory-built modules joined into family homes, modern villas and luxury residences.',
 'villa-panorama.jpg', 'Single-story modular villa with glass walls in a tropical garden',
 [('modular.jpg','Two-story homes','Two-story modular homes at sunset'),
  ('g-villa-aerial.jpg','Villa with garden','Modular villa seen from above'),
  ('i-glass-dining.jpg','Glass dining room','Dining room with glass walls')],
 ['Stackable steel modules','Open-plan or multi-bedroom layouts','Full-height glass, balconies and stairs'],
 ['Factory quality control','More predictable cost and schedule','Add modules as needs grow'],
 ['Module count','Floor plan','Facade','Glass walls','Finishes'],
 ['Family homes','Luxury villas','Modern villas','Vacation homes'], '50% 55%'))

# 12 CABINS & STUDIOS
pages.append(product_page('Portable Cabins and Backyard Studios', 'Residential', 'Portable Cabins &amp; Backyard Studios',
 'Insulated cabins and private studios for remote land, seasonal sites or the space behind your house.',
 'cabin-snow.jpg', 'Grey portable cabin with large windows standing in deep snow',
 [('backyard-studio.jpg','Backyard studio','Wood-clad backyard studio with glass doors'),
  ('capsule-pod-cabin-glass-front-factory.jpg','Capsule cabin','Capsule cabin with curved glass front'),
  ('g-capsule-snow.jpg','Built for winter','White capsule cabin covered in icicles')],
 ['Insulated composite shell','Large double-glazed windows','Raised base on adjustable supports'],
 ['Comfortable in hot and cold seasons','Move it when plans change','Minimal site preparation'],
 ['Window layout','Bathroom','Kitchenette','Heating &amp; A/C','Cladding'],
 ['Home offices','Studios','Remote land','Campgrounds'], '50% 48%'))

# 13 GUEST & HOLIDAY
pages.append(product_page('Guest Houses and Holiday Homes', 'Residential · Hospitality', 'Guest Houses &amp; Holiday Homes',
 'Private suites for visitors and vacation homes that can earn income when you are away.',
 'guesthouse.jpg', 'Container guest house with a rooftop deck and outdoor stairs',
 [('g-guesthouse-front.jpg','Rooftop terrace','Guest house with deck and rooftop terrace'),
  ('glass-villa-pool.jpg','Pool villa','Modern glass villa next to a pool'),
  ('r-deck.jpg','Deck edition','Small house with wood-look cladding and a raised deck')],
 ['Bedroom, bathroom and kitchenette','Sliding glass doors','Optional rooftop deck with stairs'],
 ['Host family in comfort and privacy','Earn income as a vacation rental','Adds outdoor living space'],
 ['Rooftop deck','Railings','Accent cladding','Lighting','Pool deck'],
 ['Guest suites','Holiday homes','Vacation rentals','Airbnb hosts']))

# 14 OFFICES
pages.append(product_page('Portable Offices', 'Commercial', 'Portable Offices',
 'Ready-to-use offices for job sites, sales teams and growing companies, from one unit to multi-story buildings.',
 'p-office-2storey-finished.jpg', 'Finished two-story modular office with a glass ground floor',
 [('p-office-interior.jpg','Bright interiors','Office interior with glass doors and meeting table'),
  ('office.jpg','Single office unit','White and graphite portable office unit'),
  ('f-glass-office.jpg','Two-story office','Two-story office modules with large windows')],
 ['Open-plan interiors with glass entry','Lighting, power and A/C ready','Stack or join units into buildings'],
 ['Up and running fast','Moves when the project moves','A professional face for clients'],
 ['Partitions','Restroom','Meeting room','Glass facade','Your branding'],
 ['Job sites','Sales offices','Startups','Site management'], '50% 60%'))

# 15 COMMERCIAL
pages.append(category_page('Commercial buildings', 'Commercial', 'Commercial solutions', 'Spaces that bring customers in.',
 'Showrooms, shops, cafés and restaurants built from modules, open sooner and easy to expand or move.',
 [('p-sales-center-night.jpg','Sales center with terrace','Two-story modular sales center at dusk','m-big'),
  ('p-cafe-terrace.jpg','Café terrace','Café terrace on a modular building'),
  ('p-rooftop-cafe-render.jpg','Rooftop café','Modular café with rooftop seating'),
  ('p-restaurant-pool-render.jpg','Restaurant','Modular restaurant with glass front by a pool'),
  ('p-retail-hall-interior.jpg','Retail hall','Large bright retail hall interior'),
  ('p-cinema-hall-render.jpg','Commercial building','Two-story steel commercial building')],
 [('Office Buildings','Multi-story modular offices'),('Sales Offices','Real estate and site sales'),('Showrooms','Display products in style'),('Retail Shops','Pop-up or permanent stores'),
  ('Cafés','Compact units with terraces'),('Restaurants','Kitchens, dining and decks'),('Commercial Buildings','Large-span steel halls'),('Branding','Your colors, signs and facade')]))

# 16 HOSPITALITY
pages.append(category_page('Hospitality', 'Hospitality', 'Hospitality solutions', 'Resorts and stays guests remember.',
 'Villas, hotel units and glamping cabins that open in phases and grow with demand.',
 [('p-resort-villas-aerial.jpg','Resort villas','Aerial view of pitched-roof resort villas','m-big'),
  ('resort-aerial.jpg','Capsule cabin resort','Aerial view of a resort with capsule cabins around a pool'),
  ('g-stacked-tower.jpg','Stacked hotel units','Stacked colorful container hotel'),
  ('commercial.jpg','Hotel units','Row of colorful raised container hotel units'),
  ('g-resort-row.jpg','Beach resort row','Row of navy expandable houses under palm trees'),
  ('white-pod-lake.jpg','Lakeside glamping','White pod cabin beside a lake')],
 [('Resort Villas','Private villas with decks'),('Hotel Units','Stackable rooms and suites'),('Eco Lodges','Low-impact raised cabins'),('Glamping Units','Capsule and pod cabins'),
  ('Tourist Accommodation','Rooms for parks and attractions'),('Pools &amp; Decks','Outdoor living areas'),('Phased Openings','Start small, add units'),('Theming','Finishes to match your brand')]))

# 17 INDUSTRIAL & STORAGE
pages.append(category_page('Industrial and storage', 'Industrial &amp; Storage', 'Industrial &amp; storage solutions', 'Strong buildings for hard work.',
 'Steel warehouses, workshops, storage units and site facilities, sized for your operation.',
 [('p-steel-warehouse-frame.jpg','Steel warehouse','Steel frame of a large warehouse','m-big'),
  ('p-commercial-roof-install.jpg','Roof installation','Workers installing roof panels on a steel building'),
  ('p-commercial-hall-side.jpg','Industrial building','Long single-story steel building'),
  ('storage.jpg','Storage unit','Grey portable storage unit'),
  ('p-restroom-block-brown.jpg','Site facilities','Modular restroom block on site'),
  ('f-single.jpg','Workshop module','Single flat-pack container module')],
 [('Warehouses','Large-span steel structures'),('Storage Units','Secure, weather-resistant'),('Workshop Buildings','Power, light and ventilation'),('Industrial Buildings','Factories and plant rooms'),
  ('Site Facilities','Restrooms, showers, canteens'),('Guard Houses','Security and gate units'),('Fast Assembly','Bolted steel systems'),('Relocatable','Move to the next site')]))

# 18 INSTITUTIONAL
pages.append(category_page('Institutional', 'Institutional', 'Institutional solutions', 'Classrooms, clinics and staff housing.',
 'Modular buildings for education, healthcare and workforce accommodation, delivered on tight schedules.',
 [('p-kindergarten-glass.jpg','Kindergarten','Modular kindergarten with glass walls and a garden','m-big'),
  ('p-classroom-1.jpg','Classroom','Classroom inside a modular building'),
  ('p-clinic-corridor.jpg','Medical clinic','Bright corridor inside a modular clinic'),
  ('p-clinic-modules-aerial.jpg','Healthcare facility','Aerial view of a two-story modular healthcare building'),
  ('p-staff-housing-aerial.jpg','Staff accommodation','Aerial view of modular staff housing blocks'),
  ('p-labor-camp-wide.jpg','Labor camp','Large workforce camp with red roofs')],
 [('Schools','Full campuses or extensions'),('Classrooms','Bright, insulated rooms'),('Training Centers','Flexible open plans'),('Medical Clinics','Clean, easy-to-wash finishes'),
  ('Healthcare Facilities','Wards and isolation units'),('Labor Camps','Housing at any scale'),('Staff Accommodation','Rooms, kitchens, laundry'),('Public Service','Visa and service centers')]))

# 19 INTERIORS (existing)
interiors = s[s.index('<section class="page" aria-label="Interiors">'):]
interiors = interiors[:interiors.index('</section>') + len('</section>')]
pages.append(interiors)

# 20 CUSTOMIZATION
swatch6 = '<div class="vis swatch6"><i style="background:#F4F4F1"></i><i style="background:#1D2022"></i><i style="background:#5C6266"></i><i style="background:repeating-linear-gradient(90deg,#9A6233 0 .5cqw,#A86C3A .5cqw 1.1cqw,#8F5A2E 1.1cqw 1.5cqw)"></i><i style="background:#B9BDB8"></i><i style="background:#CDBFA6"></i></div>'
mats = '<div class="vis mats"><div class="m-wood">Woodgrain</div><div class="m-metal">Metal cladding</div><div class="m-bamboo">Bamboo-wood</div><div class="m-panel">Sandwich panel</div></div>'
sizes = '<div class="vis sizes">' + ''.join('<div class="row"><span>%d FT</span><div class="bar">%s</div></div>' % (10*n, '<i></i>'*n) for n in (1,2,3,4)) + '</div>'
c8 = [
 ('<img class="vis" src="img/floorplan.jpg" alt="Top-down floor plan with living area and bedrooms">', 'Floor Plans', 'Open plan or one to three bedrooms, arranged around how you live.'),
 ('<img class="vis contain" src="img/cutaway.jpg" alt="3D cutaway of a one-bedroom layout">', 'Interior Layout', 'Move walls, kitchens and bathrooms. Add storage and built-ins.'),
 ('<img class="vis" src="img/g-veranda-wood.jpg" alt="House with covered wood veranda">', 'Exterior Design', 'Verandas, canopies, decks, stairs and roof styles.'),
 (swatch6, 'Colors', 'Frame and wall colors from white and black to woodgrain and sand.'),
 ('<img class="vis" src="img/r-sunroom.jpg" alt="House with black frames and large glass windows">', 'Windows', 'Sliding, awning or floor-to-ceiling glass, single or double glazed.'),
 ('<img class="vis" src="img/expandable-open.jpg" alt="House with glass and solid doors open">', 'Doors', 'Steel security, glass sliding or hinged aluminum doors.'),
 (mats, 'Materials', 'Choose wall panels, cladding, flooring and countertops.'),
 (sizes, 'Sizes', 'Standard 10–40 ft modules, combined side by side or stacked.'),
]
c8h = ''.join('<article>%s<h3>%s</h3><p>%s</p></article>' % x for x in c8)
pages.append(page('Customization', 'Customization', '''      <div class="title-block">
        <p class="eyebrow">Customization</p>
        <h2>Make it yours.</h2>
        <p class="pitch">Every KIKFIA building can be changed in eight ways. Combine them to fit your site, budget and style.</p>
      </div>
      <div class="cust8">%s</div>
      <div class="project-band"><strong>Project-based solutions</strong><span>Have drawings or a site plan already? Send them and we will adapt our building systems to your design.</span></div>''' % c8h))

# 21 GALLERY
g = ''.join([
 fig('p-staff-housing-2storey.jpg','Two-story staff residence','Two-story modular residence with blue balconies and garden','g-big'),
 fig('g-capsule-snow.jpg','Capsule cabin in winter','White capsule cabin with icicles','g-tall2'),
 fig('p-camp-row-wide.jpg','Workforce housing','Long row of single-story modular units'),
 fig('p-office-2storey-finished.jpg','Two-story office','Finished two-story modular office'),
 fig('p-visa-center-exterior.jpg','Public service center','Large single-story service building'),
 fig('g-veranda-row.jpg','Homes with verandas','Row of expandable houses with white verandas'),
 fig('p-site-units-black-roof.jpg','Units on site','Folding units installed on site'),
 fig('g-expandable-white.jpg','40 ft expandable house','White 40 ft expandable house on a lawn'),
])
pages.append(page('Project gallery', 'Gallery', '''      <div class="title-block">
        <p class="eyebrow">Project gallery</p>
        <h2>Homes, camps, offices and more.</h2>
      </div>
      <div class="gal">%s</div>
      <div class="stats">
        <div><b>Residential</b><span>Homes, villas and cabins</span></div>
        <div><b>Commercial</b><span>Offices, shops and halls</span></div>
        <div><b>Hospitality</b><span>Resorts and hotel units</span></div>
        <div><b>Institutional</b><span>Schools, clinics, camps</span></div>
      </div>
      <p class="fine">Projects shown include buildings delivered with KIKFIA's manufacturing partners and design renderings. Finishes, sizes and site work vary by project.</p>''' % g))

# 22 PROCESS
steps = [
 ('01','Consultation','We learn about your site, budget, timeline and how the space will be used.','Recommended models and a budget range'),
 ('02','Design','We adapt the floor plan, finishes and options, then send drawings for approval.','Approved drawings and a written quote'),
 ('03','Manufacturing','Your building is made to the approved specification, with progress updates.','Production updates and a pre-shipment check'),
 ('04','Delivery','We arrange packing, freight and delivery to your site or nearest port.','Shipping schedule and documents'),
 ('05','Installation Support','Guides and direct support while your local crew sets the building and connects utilities.','Installation guide and ongoing help'),
]
st = ''.join('<div class="step"><span class="num">%s</span><div><h3>%s</h3><p>%s</p></div><div class="get"><span>You receive</span><b>%s</b></div></div>' % x for x in steps)
strip = ''.join('<figure><div class="ph"><img src="img/%s" alt="%s"></div><figcaption><b>%s</b>%s</figcaption></figure>' % x for x in [
 ('floorplan.jpg','Floor plan drawing','02','Design'),
 ('p-factory-expandable-line.jpg','Finished units in the factory','03','Manufacturing'),
 ('p-export-ship.jpg','Modules loaded on a ship for export','04','Delivery'),
 ('p-clinic-frame-aerial.jpg','Modular frames being installed on site','05','Installation'),
])
pages.append(page('Our process', 'Our process', '''      <div class="title-block">
        <p class="eyebrow">Our process</p>
        <h2>From first call to move-in.</h2>
      </div>
      <div class="steps tight">%s</div>
      <div class="pstrip">%s</div>''' % (st, strip)))

# 23 WHY CUSTOMERS CHOOSE
pill = [
 ('Reliability','We do what we quote, on the schedule we agree, and keep you informed at every step.'),
 ('Customization','Your layout, finishes, colors and size. Every project is adapted to the customer.'),
 ('Quality','Galvanized steel structures, quality finishes and a check before every shipment.'),
 ('Transparency','Itemized quotes listing the model, options, shipping and what is not included.'),
 ('Long-Term Support','Documents, installation guidance and help with questions long after delivery.'),
]
ph = ''.join('<div><h3>%s</h3><p>%s</p></div>' % x for x in pill)
ph += '<div class="note-cell"><h3>Small or large</h3><p>One studio or a 100-unit site, you get the same care and one point of contact.</p></div>'
pages.append(page('Why customers choose KIKFIA', 'Our promise', '''      <div class="title-block">
        <p class="eyebrow">Why customers choose KIKFIA</p>
        <h2>One partner from design to delivery.</h2>
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
          </ul>
        </div>
        <div class="photo"><img src="img/cabin-winter-detail.jpg" alt="White cabin wall and door covered in icicles on a sunny winter day"></div>
      </div>''' % ph))

# 24 CONTACT (existing back page)
back = s[s.index('<section class="page back"'):]
back = back[:back.index('</section>') + len('</section>')]
pages.append(back)

body = '\n\n'.join(pages)
total = body.count('<section class="page')
n = [1]
def ren(m):
    n[0] += 1
    return '<b>%02d / %d</b>' % (n[0], total)
body = re.sub(r'<b>\d\d / \d+</b>', ren, body)
head = s[:s.index('<style>')]
out = head + style + '\n\n' + defs + '\n\n' + body + '\n'
open(SRC, 'w').write(out)
print('pages', total)
