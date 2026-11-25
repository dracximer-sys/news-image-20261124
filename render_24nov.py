#!/usr/bin/env python3
"""Render the 24 November 2026 world-news front page as one 1024x1024 image.

Entry for the make.fun bounty 'Sum up 24 November's world news in one image'
(news-image-20261124). Every story on the page happened on, or was first
reported on, Monday 24 November 2026. Stories from other dates are listed in
the DATE CHECK box and deliberately left out.

Drawn locally with Pillow. The program itself (main.py) is stdlib-only and
embeds the rendered bytes, so grading runs are byte-identical.
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 248, 241)
INK = (17, 17, 17)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
SEA = (214, 228, 240)
LAND = (232, 224, 204)
GREY = (90, 90, 90)
LIGHT_GREY = (210, 205, 195)

FONT_DIR = "/usr/share/fonts/truetype/liberation/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_B = lambda s: font("LiberationSerif-Bold.ttf", s)
SERIF = lambda s: font("LiberationSerif-Regular.ttf", s)
SANS = lambda s: font("LiberationSans-Regular.ttf", s)
SANS_B = lambda s: font("LiberationSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Wrap text to fit max_w pixels, returning a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


# ---------------------------------------------------------------- stories
# (title, summary, region, lat, lon or None)
STORIES = [
    ('HUAWEI GUILTY ON 10 COUNTS',
     'A Brooklyn jury convicts Huawei on 10 of 12 counts — trade-secret '
     'theft, bank fraud and Iran sanctions violations — after a trial of '
     'more than two months. It clears the firm of racketeering; Huawei '
     'will appeal.',
     'AMERICAS', 40.68, -73.94),
    ('NVIDIA SINKS 5.9% AFTER RALLY',
     'A day after the +31.5% comeback rally, Nvidia shares fall 5.9% to '
     '$155.38, wiping about $233 billion off its value. CEO Jensen Huang '
     'apologises to staff and says he is in therapy.',
     'AMERICAS', 37.37, -121.96),
    ('HOUTHI DRONE HITS RIYADH TOWER',
     "A Houthi drone strikes the PIF Tower in Riyadh's financial district "
     '— the second hit in under a week — wounding 11 people. The Saudi-led '
     'coalition vows a firm response.',
     'MIDDLE EAST', 24.76, 46.64),
    ('RUSSIAN DRONE BREACHES POLISH AIRSPACE',
     'A Russian drone enters Polish airspace overnight during strikes on '
     'Ukraine, then turns back east; Poland holds fire over civilian risk. '
     'The second such incident in four days.',
     'EUROPE', 51.14, 23.47),
    ('ZELENSKY: UKRAINE NEEDS €115BN',
     'President Zelensky says Ukraine needs at least €115 billion in '
     'outside support in 2027; €90 billion is secured from the EU, leaving '
     '€25 billion still to find.',
     'EUROPE', 50.45, 30.52),
    ('EU WARNS 11 STATES OVER BUDGETS',
     'The European Commission warns 11 member states risk breaking EU '
     'spending rules as it publishes its autumn package; EU defence '
     'spending is set to rise to 2.1% of GDP.',
     'EUROPE', 48.58, 7.75),
    ('EUROPEAN GAS CLIMBS AS STORAGE DIPS',
     'Dutch TTF gas tops €90.50/MWh for a fourth straight day in a cold '
     'snap, with EU storage only 68.9% full — well below the five-year '
     'average of 89%.',
     'EUROPE', 52.37, 4.9),
    ('TURKISH HELICOPTER CRASH KILLS 5',
     'A Turkish Air Force AS-532 Cougar crashes during a training flight '
     'in Eskişehir province, killing five soldiers; the cause is not yet '
     'announced.',
     'EUROPE', 39.78, 30.52),
    ('GAZA STRIKES KILL HAMAS SECURITY CHIEF',
     'Israeli strikes kill at least six in Gaza, including Hamas internal '
     "security chief Naeem Abu Nahel; Gaza's health ministry declares a "
     'meningitis epidemic alert, with 272 cases in October.',
     'MIDDLE EAST', 31.5, 34.47),
    ('COALITION ORDERS HODEIDAH EVACUATION',
     "The Saudi-led coalition orders civilians to leave Yemen's Hodeidah "
     'port ahead of a possible strike; the Houthis threaten Saudi Red Sea '
     'ports, including Jeddah.',
     'MIDDLE EAST', 14.8, 42.95),
    ('CIA-ODNI SYSTEMS HACKED, DATA EXPOSED',
     'Hackers breach unclassified CIA and ODNI networks used for '
     'open-source intelligence analysis, exposing unclassified data, the '
     'New York Times reports. Classified systems are unaffected.',
     'AMERICAS', 38.95, -77.15),
    ('ABREGO GARCIA SELF-DEPORTS TO SPAIN',
     'Kilmar Abrego Garcia, wrongly deported to El Salvador in 2025, '
     'leaves the US voluntarily for Madrid after a judge orders '
     'self-deportation. His lawyers say Spain is not his final '
     'destination.',
     'AMERICAS', 38.91, -77.04),
    ('TRUMP PARDONS TURKEYS FREEDOM AND FEATHERS',
     'Trump pardons two Thanksgiving turkeys, Freedom and Feathers, in the '
     '79th annual ceremony at the White House — though only Freedom shows '
     "up; Feathers 'ran into the bushes'.",
     'AMERICAS', 38.9, -77.04),
    ('BRAZIL APPROVES R$60BN FISCAL PACKAGE',
     "Brazil's lower house approves Lula's fiscal package, capping real "
     'spending growth at 2% and cutting tax breaks, worth an estimated '
     'R$60 billion in 2027. The bill now goes to Lula to sign.',
     'AMERICAS', -15.79, -47.88),
    ('COURT ALLOWS IOWA LEAD AZIDE BLAST',
     'A federal appeals court lifts the stay, clearing the Army to '
     'detonate 9,500 pounds of degraded lead azide in Iowa on Wednesday '
     'morning; Missouri activates its emergency centre over lead dust.',
     'AMERICAS', 40.82, -91.26),
    ('US READIES NEW TARIFFS ON CHINA, EU',
     'Washington prepares higher tariffs on China, the EU and 14 other '
     'countries over alleged industrial over-subsidisation, with the USTR '
     'expected to announce findings this week.',
     'AMERICAS', 38.89, -77.03),
    ('US CONSUMER CONFIDENCE JUMPS TO 103.3',
     'The Conference Board index surges 11.4 points to 103.3 in November, '
     'its highest since January 2025 and far above the 92.5 consensus; '
     "30.8% call jobs 'plentiful'.",
     'AMERICAS', 40.71, -74.01),
    ('RUSSIAN JETS TRIGGER ULLEUNG ALERT',
     "Russian military aircraft enter Korea's air defence zone near "
     'Ulleung Island, prompting South Korea to scramble fighters; a civil '
     'alert sounds for about three minutes before being lifted.',
     'ASIA', 37.48, 130.91),
    ('ASIAN MARKETS SURGE AFTER NVIDIA',
     "Asia's bourses soar on the Nvidia comeback: Korea's Kospi jumps "
     "6.32% to 5,006, Japan's Nikkei rises 3.91% and Taiwan's Taiex 9.0%, "
     'led by chip stocks.',
     'ASIA', 37.57, 126.98),
    ('SOLOMON ISLANDS ENDS CHINA PACT',
     'Solomon Islands tells China it will not renew its 2022 security pact '
     'when it expires in April 2027, and will sign a new deal making '
     'Australia its preferred defence partner.',
     'ASIA', -9.65, 160.06),
    ('PHILIPPINES DEPORTS 139 INDONESIANS',
     'The Philippines deports 139 Indonesians caught in a Pasay scam-hub '
     'raid, flying them home on a chartered flight from Manila airport; '
     'two remain detained for prosecution.',
     'ASIA', 14.54, 121.0),
    ('AUSTRALIA-SINGAPORE SIGN AI PACT',
     'Prime ministers Albanese and Wong sign a joint AI cooperation '
     'statement in Canberra, plus a cross-border CO2 storage deal and an '
     'essentials-supply pact on fuel, food and medicine.',
     'ASIA', -35.28, 149.13),
    ("ANWAR: US CHIP CURBS WON'T STOP CHINA",
     "Malaysia's PM Anwar Ibrahim tells the South China Morning Post that "
     'US curbs on advanced AI chips will not stop Malaysia working with '
     "Beijing, calling China 'extremely reasonable' on the South China "
     'Sea.',
     'ASIA', 3.14, 101.69),
    ('CHINA-SINGAPORE EXPAND YUAN FINANCING',
     'China and Singapore widen yuan financing for business, including '
     'trade with third countries, in a package of 29 deals at their joint '
     'council meeting; DBS becomes a second RMB clearing bank.',
     'ASIA', 1.35, 103.82),
    ('US BLACKLISTS MEGASPEED OVER NVIDIA CHIPS',
     'The US Commerce Department adds Megaspeed and six affiliates in '
     'Singapore, Malaysia and Thailand to its Entity List, barring '
     'advanced US AI chip purchases over diversion risks to China.',
     'ASIA', 1.35, 103.82),
    ('175 MIGRANTS MISSING AFTER DAKAR DEPARTURE',
     'About 175 migrants are missing after contact is lost with a wooden '
     'boat that left Yoff, Dakar, for Europe around 9-10 November, the '
     'mayor and a local NGO report.',
     'AFRICA', 14.76, -17.44),
    ('MADAGASCAR SEEKS RAJOELINA ARREST WARRANT',
     "Madagascar's anti-corruption prosecutor seeks arrest warrants for "
     'ex-president Rajoelina and ex-PM Ntsay over the transfer of five '
     'Boeing 777s to Iran in July 2025 to dodge sanctions.',
     'AFRICA', -18.88, 47.51),
    ('DRC ANNOUNCES $965M MINING INVESTMENT',
     'A mining forum in Kinshasa announces $965 million in sector '
     'investment; President Tshisekedi insists Congo must process its '
     'minerals at home instead of exporting them raw.',
     'AFRICA', -4.32, 15.31),
    ('AMNESTY: TIGRAY SHELLING POSSIBLE WAR CRIMES',
     'Amnesty International says artillery attacks on civilians in '
     'Alamata, Tigray, in September must be probed as possible war crimes; '
     '14 civilian deaths are verified.',
     'AFRICA', 12.42, 39.55),
    ('UN: FIVE WOMEN KILLED EVERY HOUR',
     'UNODC and UN Women report 47,000 women and girls were killed by '
     'partners or family in 2025 — five an hour. Africa has the highest '
     'rate, 2.9 per 100,000 women.',
     'AFRICA', 40.75, -73.97),
    ('PROGRESS MS-36 LAUNCHES TO ISS',
     'A Soyuz-2.1b lifts off from Baikonur carrying the Progress MS-36 '
     'cargo ship with about 2.5 tonnes of food, fuel and supplies; docking '
     'is set for 26 November.',
     'TECH & SPACE', 45.96, 63.3),
    ('ARIANE 6 LAUNCHES 36 AMAZON SATELLITES',
     'Ariane 64 launches from Kourou with 36 Amazon Leo satellites, the '
     'tenth Ariane 6 flight, bringing the constellation to 432 satellites '
     'in orbit.',
     'TECH & SPACE', 5.16, -52.65),
    ('FALCON 9 LAUNCHES SECRET USSF-266',
     'SpaceX launches the classified US Space Force payload USSF-266 from '
     'Vandenberg after a one-day delay; the first-stage booster lands on a '
     'Pacific drone ship.',
     'TECH & SPACE', 34.58, -120.63),
    ('SHENZHOU-24 CARRIES FIRST PAKISTANI ASTRONAUT',
     'China names the Shenzhou-24 crew: Tang Hongbo, Wu Yi and Muhammad '
     'Zeeshan Ali, who will become the first Pakistani in orbit and the '
     'first foreigner aboard Tiangong station.',
     'TECH & SPACE', 40.96, 100.29),
    ('SANOFI BUYS INSMED FOR $41BN',
     'Sanofi agrees to buy US biotech Insmed for $41 billion in cash at '
     '$175 a share, a 17% premium; Insmed shares rise about 14% and Sanofi '
     'about 5% in Paris.',
     'ECONOMY', 48.85, 2.35),
    ('CAS RESTORES SENEGAL AS AFCON CHAMPIONS',
     "The Court of Arbitration for Sport restores Senegal's 2025 Africa "
     'Cup title, ruling the 1-0 final win over Morocco stands and '
     "overturning CAF's 3-0 forfeit award to Morocco.",
     'SPORT & CULTURE', 46.52, 6.63),
    ('REAL MADRID ROUT PSV 5-1',
     'Real Madrid come back from 1-0 down to beat PSV Eindhoven 5-1 at the '
     'Bernabeu in the Champions League — Valverde, Bellingham, two from '
     'Mbappe and Vinicius. Five wins from five.',
     'SPORT & CULTURE', 40.45, -3.69),
    ('15-YEAR-OLD SMASHES 204 OFF 53 BALLS',
     'Vaibhav Sooryavanshi, 15, scores 204 from 53 balls for India A '
     'against the UAE in Doha — the fastest List A century (28 balls) and '
     'double-century (52), with a record 28 sixes.',
     'SPORT & CULTURE', 25.29, 51.53),
    ('CHESS: GUKESH-SINDAROV GAME 1 DRAWN',
     'Game 1 of the World Chess Championship in Geneva ends in a draw, '
     'Gukesh vs Sindarov finishing 0.5-0.5 after the opening game.',
     'SPORT & CULTURE', 46.2, 6.14),
    ('COP31 POST-MORTEM: FIRST FAILED COP SINCE 2009',
     'Post-summit analysis confirms COP31 in Antalya ended with no deal — '
     'the first failed UN climate summit since Copenhagen 2009 — after '
     'splits over fossil fuels and climate finance. Focus shifts to COP32 '
     'in Addis Ababa.',
     'CLIMATE', 36.9, 30.71),
]

NUMBERS = [
    ('$233B', 'Nvidia market value lost in a day'),
    ('103.3', 'US consumer confidence, highest since Jan 2025'),
    ('10 of 12', 'counts Huawei was found guilty on'),
    ('175', 'migrants missing after leaving Dakar'),
    ('47,000', 'women and girls killed by partners or family in 2025'),
    ('272', 'meningitis cases in Gaza in October, 8x normal'),
]

PINS = [
    (1, 'Brooklyn — Huawei verdict', 40.68, -73.94),
    (2, 'Santa Clara — Nvidia plunge', 37.37, -121.96),
    (3, 'Riyadh — Houthi drone', 24.76, 46.64),
    (4, 'Chełm — Russian drone', 51.14, 23.47),
    (5, 'Gaza City — strikes', 31.5, 34.47),
    (6, 'Hodeidah, Yemen — evacuation', 14.8, 42.95),
    (7, 'Dakar — 175 migrants', 14.76, -17.44),
    (8, 'Kyiv — €115B plea', 50.45, 30.52),
    (9, 'Ulleung — Russian jets', 37.48, 130.91),
    (10, 'Jiuquan — Shenzhou-24', 40.96, 100.29),
    (11, 'Baikonur — Progress MS-36', 45.96, 63.3),
]

DATE_CHECK = (
    "Not 24 November, so left out: Russian corvette Merkury sunk off Benghazi (22 Nov, confirmed 23 Nov) · COP31 collapse itself (22 Nov) · First Houthi strike on Riyadh's PIF Tower (19 Nov) · FIFA Women's World Cup hosts announced (23 Nov) · Jensen Huang returns as Nvidia CEO, shares +31.5% (23 Nov) · BepiColombo enters Mercury orbit (21 Nov) · NASA lunar reactor tender (23 Nov) · Cikande candy factory fire, Indonesia (21-22 Nov, reported 23 Nov)."
)

SOURCES = (
    'Sources: Reuters · AP · CNN · BBC · Al Jazeera · The New York Times · Le Monde · UN News · Euronews · AFP · USA Today · Yonhap. All stories from Tuesday 24 Nov 2026. Built by @drac-ximer.'
)

# ---------------------------------------------------------------- map data
# Simplified continent outlines as (lon, lat) points, equirectangular.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-70, 62), (-55, 52), (-60, 46), (-70, 42), (-75, 35),
     (-80, 26), (-85, 20), (-90, 14), (-95, 16), (-100, 20), (-105, 22),
     (-110, 28), (-115, 32), (-120, 34), (-125, 40), (-125, 48), (-135, 58),
     (-150, 60), (-165, 60)],
    [(-55, 60), (-45, 60), (-40, 64), (-30, 68), (-25, 70), (-30, 76),
     (-45, 76), (-58, 70), (-60, 64)],
    [(-80, 10), (-75, 12), (-70, 12), (-60, 8), (-50, 4), (-45, 0),
     (-40, -5), (-35, -8), (-40, -15), (-45, -22), (-50, -28), (-55, -35),
     (-60, -40), (-65, -45), (-70, -52), (-73, -45), (-75, -35), (-78, -25),
     (-80, -15), (-82, -5), (-80, 5)],
    [(-17, 15), (-15, 25), (-10, 30), (-5, 35), (0, 36), (10, 37), (15, 32),
     (20, 32), (30, 31), (35, 28), (40, 20), (43, 12), (48, 10), (51, 12),
     (45, 5), (40, -2), (38, -10), (35, -18), (32, -25), (28, -32),
     (20, -35), (15, -30), (12, -18), (10, -5), (8, 4), (0, 5), (-8, 5),
     (-15, 10)],
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (5, 53), (8, 55),
     (10, 58), (12, 60), (18, 62), (20, 65), (25, 70), (30, 70), (40, 68),
     (50, 69), (60, 70), (70, 72), (80, 73), (90, 75), (100, 76), (110, 74),
     (120, 73), (130, 72), (140, 72), (150, 70), (160, 69), (170, 66),
     (178, 65), (170, 60), (162, 58), (158, 52), (150, 45), (142, 40),
     (140, 35), (135, 33), (130, 31), (127, 35), (122, 38), (120, 32),
     (115, 25), (110, 20), (108, 12), (105, 8), (100, 8), (98, 12), (95, 16),
     (92, 20), (88, 22), (85, 19), (80, 15), (77, 8), (75, 12), (72, 20),
     (68, 23), (65, 25), (60, 25), (57, 26), (54, 27), (52, 28), (50, 30),
     (48, 30), (46, 32), (44, 35), (42, 38), (40, 40), (38, 42), (35, 42),
     (33, 40), (30, 38), (28, 38), (26, 38), (23, 36), (20, 38), (18, 40),
     (15, 40), (12, 42), (10, 44), (8, 44), (5, 43), (3, 43), (0, 40),
     (-2, 37), (-6, 36), (-9, 37)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    [(130, 31), (132, 33), (134, 34), (137, 35), (139, 37), (141, 39),
     (141, 42), (143, 44), (145, 44), (142, 42), (140, 38), (138, 35),
     (136, 33), (133, 32)],
    [(95, 5), (100, 0), (104, -3), (106, -6), (103, -5), (100, 0)],
    [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (113, -4), (110, -2)],
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9), (146, -8),
     (141, -8), (136, -4), (132, -2)],
    [(105, -6), (110, -7), (114, -7), (114, -8), (108, -8), (105, -7)],
    [(119, 0), (121, 1), (123, 0), (121, -2), (120, -4), (119, -2)],
    [(114, -22), (114, -30), (115, -33), (118, -35), (124, -33), (130, -32),
     (135, -35), (138, -35), (140, -38), (145, -38), (150, -37), (153, -32),
     (153, -27), (150, -22), (146, -19), (142, -15), (142, -11), (137, -12),
     (135, -15), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38),
     (175, -40), (172, -43), (168, -46)],
]


def draw_map(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA, outline=INK, width=1)
    lon0, lon1, lat0, lat1 = -180.0, 180.0, 85.0, -60.0

    def proj(lon, lat):
        px = x0 + (lon - lon0) / (lon1 - lon0) * w
        py = y0 + (lat0 - lat) / (lat0 - lat1) * h
        return (px, py)

    for poly in CONTINENTS:
        draw.polygon([proj(lon, lat) for lon, lat in poly],
                     fill=LAND, outline=(120, 110, 90))
    # graticule
    for lon in range(-150, 181, 30):
        px = x0 + (lon - lon0) / (lon1 - lon0) * w
        draw.line([(px, y0), (px, y0 + h)], fill=(190, 205, 220), width=1)
    for lat in range(-60, 86, 30):
        py = y0 + (lat0 - lat) / (lat0 - lat1) * h
        draw.line([(x0, py), (x0 + w, py)], fill=(190, 205, 220), width=1)
    fnt = SANS_B(11)
    for num, _label, lat, lon in PINS:
        px, py = proj(lon, lat)
        r = 9
        draw.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                     outline=(255, 255, 255), width=1)
        tw = draw.textlength(str(num), font=fnt)
        draw.text((px - tw / 2, py - 6), str(num), font=fnt,
                  fill=(255, 255, 255))
    return proj


def draw_headline_art(draw, box, kind):
    x0, y0, x1, y1 = box
    if kind == 0:  # Huawei verdict: courthouse columns
        draw.rectangle(box, fill=(28, 42, 74))
        cx = (x0 + x1) // 2
        base = y0 + 46
        draw.polygon([(cx - 52, y0 + 8), (cx + 52, y0 + 8), (cx, y0 - 2)],
                     fill=(220, 220, 220))
        for dx in (-36, -12, 12, 36):
            draw.rectangle([cx + dx - 5, y0 + 12, cx + dx + 5, base],
                           fill=(220, 220, 220))
        draw.rectangle([cx - 56, base, cx + 56, base + 4], fill=(220, 220, 220))
        draw.text((x0 + 8, y0 + 4), "BROOKLYN", font=SANS_B(10),
                  fill=(255, 255, 255))
    elif kind == 1:  # Nvidia: chip with falling arrow
        draw.rectangle(box, fill=(18, 90, 40))
        cx, cy = (x0 + x1) // 2 - 30, (y0 + y1) // 2 + 6
        draw.rectangle([cx - 26, cy - 26, cx + 26, cy + 26], fill=(10, 40, 18),
                       outline=(140, 220, 140), width=2)
        draw.rectangle([cx - 12, cy - 12, cx + 12, cy + 12], fill=(30, 140, 60))
        for dx in (-26, 26):
            for dy in (-14, 0, 14):
                draw.line([(cx + dx, cy + dy), (cx + dx + (10 if dx > 0 else -10), cy + dy)],
                          fill=(140, 220, 140), width=2)
        draw.line([(x0 + 205, y0 + 14), (x0 + 235, y1 - 30), (x0 + 262, y1 - 44)],
                  fill=(255, 80, 80), width=4)
        draw.polygon([(x0 + 252, y1 - 34), (x0 + 272, y1 - 34), (x0 + 262, y1 - 20)],
                     fill=(255, 80, 80))
        draw.text((x0 + 8, y0 + 4), "SANTA CLARA", font=SANS_B(10),
                  fill=(255, 255, 255))
    else:  # Riyadh tower: tall tower + drone flash
        draw.rectangle(box, fill=(20, 30, 55))
        tx0, tx1 = x0 + 120, x0 + 175
        draw.rectangle([tx0, y0 + 6, tx1, y1 - 4], fill=(90, 110, 150),
                       outline=(200, 210, 230), width=1)
        for wy in range(y0 + 12, y1 - 8, 8):
            draw.line([(tx0 + 6, wy), (tx1 - 6, wy)], fill=(255, 220, 120), width=2)
        import math
        for ang in range(0, 360, 45):
            a = math.radians(ang)
            draw.line([(x0 + 235, y0 + 22),
                       (x0 + 235 + int(15 * math.cos(a)),
                        y0 + 22 + int(15 * math.sin(a)))], fill=(255, 170, 0), width=3)
        draw.ellipse([x0 + 228, y0 + 15, x0 + 242, y0 + 29], fill=(255, 220, 0))
        draw.text((x0 + 8, y0 + 4), "RIYADH", font=SANS_B(10),
                  fill=(255, 255, 255))

def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24
    x0, x1 = M, W - M

    # ---- masthead
    title = "THE WORLD TODAY"
    f_title = SERIF_B(54)
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 10), title, font=f_title, fill=INK)
    d.line([(x0, 76), (x1, 76)], fill=INK, width=2)
    f_sub = SANS_B(13)
    d.text((x0, 82), "TUESDAY, 24 NOVEMBER 2026", font=f_sub, fill=INK)
    right = "40 STORIES  ·  9 REGIONS  ·  ONE DAY"
    d.text((x1 - d.textlength(right, font=f_sub), 82), right, font=f_sub, fill=INK)

    # ---- red date band
    d.rectangle([x0, 100, x1, 128], fill=RED)
    band = "THE DAY IN WORLD NEWS  —  TUESDAY 24 NOVEMBER 2026"
    fb = SANS_B(15)
    d.text(((W - d.textlength(band, font=fb)) / 2, 107), band, font=fb,
           fill=(255, 255, 255))

    # ---- region counts
    from collections import Counter
    counts = Counter(s[2] for s in STORIES)
    order = ["EUROPE", "MIDDLE EAST", "AMERICAS", "ASIA", "AFRICA",
             "TECH & SPACE", "ECONOMY", "SPORT & CULTURE", "CLIMATE"]
    parts = [f"{r} {counts[r]}" for r in order if counts[r]]
    rc = "   ·   ".join(parts)
    fr = SANS_B(12)
    d.text(((W - d.textlength(rc, font=fr)) / 2, 136), rc, font=fr, fill=INK)

    # ---- the day in numbers
    y = 160
    d.text((x0, y), "THE DAY IN NUMBERS", font=SANS_B(14), fill=RED)
    y += 22
    bw = (x1 - x0 - 5 * 8) // 6
    for i, (num, label) in enumerate(NUMBERS):
        bx = x0 + i * (bw + 8)
        d.rectangle([bx, y, bx + bw, y + 50], outline=INK, width=1)
        d.text((bx + 8, y + 4), num, font=SANS_B(18), fill=INK)
        draw_wrapped(d, bx + 8, y + 27, label, SANS(9), bw - 14, fill=GREY, leading=10)
    y += 50 + 10

    # ---- top stories
    d.text((x0, y), "TOP STORIES", font=SANS_B(14), fill=RED)
    y += 22
    cw = (x1 - x0 - 2 * 12) // 3
    top_y = y
    for i in range(3):
        cx0 = x0 + i * (cw + 12)
        title, summ, _reg, _la, _lo = STORIES[i]
        d.rectangle([cx0, y, cx0 + cw, y + 160], outline=INK, width=1)
        draw_headline_art(d, (cx0 + 1, y + 1, cx0 + cw - 1, y + 57), i)
        d.text((cx0 + 8, y + 62), f"{i + 1}", font=SERIF_B(20), fill=RED)
        ty = draw_wrapped(d, cx0 + 30, y + 62, title, SERIF_B(17), cw - 38,
                          leading=20)
        draw_wrapped(d, cx0 + 8, ty + 2, summ, SANS(11), cw - 16, fill=(40, 40, 40),
                     leading=14)
    y = top_y + 160 + 10

    # ---- world map
    d.text((x0, y), "WHERE IT HAPPENED", font=SANS_B(14), fill=RED)
    y += 22
    map_h = 140
    draw_map(d, x0, y, x1 - x0, map_h)
    y += map_h + 6
    pins_txt = "  ·  ".join(f"{n}. {lab}" for n, lab, _a, _b in PINS[:6])
    pins_txt2 = "  ·  ".join(f"{n}. {lab}" for n, lab, _a, _b in PINS[6:])
    d.text((x0, y), pins_txt, font=SANS(9), fill=GREY)
    y += 12
    d.text((x0, y), pins_txt2, font=SANS(9), fill=GREY)
    y += 12 + 6

    # ---- also on
    d.text((x0, y), "ALSO ON TUESDAY 24 NOVEMBER", font=SANS_B(14), fill=RED)
    y += 22
    groups = {}
    for idx, s in enumerate(STORIES[3:], start=4):
        groups.setdefault(s[2], []).append((idx, s))
    col_w = (x1 - x0 - 20) // 2
    col_y = [y, y]
    col_x = [x0, x0 + col_w + 20]
    # split groups across two columns by story count
    flat = []
    for r in ["EUROPE", "MIDDLE EAST", "AMERICAS", "ASIA", "AFRICA",
              "TECH & SPACE", "ECONOMY", "SPORT & CULTURE", "CLIMATE"]:
        flat.extend([(r, idx, s) for idx, s in groups.get(r, [])])
    half = (len(flat) + 1) // 2
    for ci, chunk in enumerate([flat[:half], flat[half:]]):
        cy = col_y[ci]
        cx = col_x[ci]
        cur_reg = None
        for reg, idx, s in chunk:
            if reg != cur_reg:
                d.text((cx, cy), reg, font=SANS_B(10), fill=RED)
                cy += 12
                cur_reg = reg
            line = f"{idx}. {s[0]}"
            yy = draw_wrapped(d, cx + 12, cy, line, SANS(10), col_w - 12,
                              leading=12)
            cy = yy
        col_y[ci] = cy
    y = max(col_y) + 6

    # ---- date check
    d.rectangle([x0, y, x1, y + 54], outline=RED, width=2)
    d.text((x0 + 8, y + 5), "DATE CHECK — LEFT OUT ON PURPOSE",
           font=SANS_B(11), fill=RED)
    draw_wrapped(d, x0 + 8, y + 19, DATE_CHECK, SANS(10), x1 - x0 - 16,
                 fill=INK, leading=12)
    y += 54 + 6

    # ---- footer
    d.line([(x0, y), (x1, y)], fill=INK, width=1)
    y += 4
    draw_wrapped(d, x0, y, SOURCES, SANS(8), x1 - x0, fill=GREY, leading=11)
    return img


if __name__ == "__main__":
    import os
    out = os.environ.get("RENDER_OUT", "entry.png")
    img = render()
    img.save(out, optimize=True)
    print("saved", out, img.size)
