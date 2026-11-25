#!/usr/bin/env python3
"""Render the 24 Nov 2026 world-news front page (1024x1024) to entry.png.

Build-time only: uses Pillow. The graded program is main.py (stdlib-only).
Layout follows resubmit-spec-20261124.md; story facts come from
research/stories-24nov.md (40 verified stories, Tuesday 24 November 2026).
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 24                      # side margin
RIGHT = W - M               # 1000
CONTENT_W = RIGHT - M       # 976

PAPER = (251, 248, 241)
INK = (17, 17, 17)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
SEA = (214, 228, 240)
LAND = (232, 224, 204)
GREY = (90, 90, 90)
FAINT = (210, 205, 195)
DARK = (40, 40, 40)
GRATICULE = (190, 205, 220)
LAND_LINE = (120, 110, 90)

FONT_DIR = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif_b(size):
    return font("LiberationSerif-Bold.ttf", size)


def serif(size):
    return font("LiberationSerif-Regular.ttf", size)


def sans(size):
    return font("LiberationSans-Regular.ttf", size)


def sans_b(size):
    return font("LiberationSans-Bold.ttf", size)


def wrap(text, fnt, width):
    """Split text into lines that fit `width` pixels with font `fnt`."""
    lines = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if fnt.getlength(trial) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(d, x, y, lines, fnt, fill, leading):
    """Draw wrapped lines starting at (x, y); return y after the last line."""
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centred(d, cx, y, text, fnt, fill):
    """Draw text centred on cx at height y."""
    w = fnt.getlength(text)
    d.text((cx - w / 2, y), text, font=fnt, fill=fill)


def right_aligned(d, rx, y, text, fnt, fill):
    """Draw text ending at rx at height y."""
    w = fnt.getlength(text)
    d.text((rx - w, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------------------
# The 40 stories. (number, region, title, summary-or-None)
# Titles/summaries are my own wording from research/stories-24nov.md;
# every fact (names, numbers, places, outcomes) is identical to the file.
# ---------------------------------------------------------------------------
REGION_ORDER = [
    "EUROPE", "MIDDLE EAST", "AMERICAS", "ASIA", "AFRICA",
    "TECH & SPACE", "ECONOMY", "SPORT & CULTURE", "CLIMATE",
]

STORIES = [
    (1, "AMERICAS", "HUAWEI GUILTY ON 10 COUNTS",
     "A Brooklyn jury convicts Huawei on 10 of 12 counts \u2014 trade-secret "
     "theft, bank fraud and Iran sanctions violations \u2014 after a "
     "two-month trial. The company is cleared of racketeering and says it "
     "will appeal."),
    (2, "AMERICAS", "NVIDIA SINKS 5.9% AFTER RALLY",
     "A day after the +31.5% comeback rally, shares fall 5.9% to $155.38, "
     "wiping about $233bn of value. Chief executive Jensen Huang "
     "apologises to staff and says he is in therapy."),
    (3, "MIDDLE EAST", "HOUTHI DRONE HITS RIYADH TOWER",
     "A drone strikes the PIF Tower in Riyadh\u2019s financial district, "
     "the second hit in under a week. Eleven people are wounded."),
    (4, "EUROPE", "RUSSIAN DRONE BREACHES POLISH AIRSPACE", None),
    (5, "EUROPE", "ZELENSKY: UKRAINE NEEDS AT LEAST \u20ac115BN IN 2027", None),
    (6, "EUROPE", "EU WARNS 11 STATES OVER SPENDING RULES", None),
    (7, "EUROPE", "EUROPEAN GAS TOPS \u20ac90.50/MWH FOR FOURTH DAY", None),
    (8, "EUROPE", "TURKISH HELICOPTER CRASH KILLS 5 SOLDIERS", None),
    (9, "MIDDLE EAST", "ISRAELI STRIKES KILL AT LEAST 6 IN GAZA", None),
    (10, "MIDDLE EAST", "SAUDI-LED COALITION ORDERS HODEIDAH EVACUATION", None),
    (11, "AMERICAS", "HACKERS BREACH CIA AND ODNI NETWORKS", None),
    (12, "AMERICAS", "ABREGO GARCIA SELF-DEPORTS TO MADRID", None),
    (13, "AMERICAS", "TRUMP PARDONS TURKEYS FREEDOM AND FEATHERS", None),
    (14, "AMERICAS", "BRAZIL APPROVES LULA FISCAL PACKAGE", None),
    (15, "AMERICAS", "IOWA LEAD AZIDE DETONATION CLEARED", None),
    (16, "AMERICAS", "US READIES HIGHER TARIFFS ON CHINA AND EU", None),
    (17, "AMERICAS", "US CONSUMER CONFIDENCE JUMPS TO 103.3", None),
    (18, "ASIA", "RUSSIAN JETS ENTER KOREA AIR DEFENCE ZONE", None),
    (19, "ASIA", "ASIAN MARKETS SURGE ON NVIDIA COMEBACK", None),
    (20, "ASIA", "SOLOMON ISLANDS ENDS CHINA SECURITY PACT", None),
    (21, "ASIA", "PHILIPPINES DEPORTS 139 INDONESIANS", None),
    (22, "ASIA", "AUSTRALIA-SINGAPORE SIGN AI COOPERATION PACT", None),
    (23, "ASIA", "ANWAR: US CHIP CURBS WON\u2019T STOP MALAYSIA", None),
    (24, "ASIA", "CHINA-SINGAPORE WIDEN YUAN FINANCING", None),
    (25, "ASIA", "US BLACKLISTS MEGASPEED OVER CHIP DIVERSION", None),
    (26, "AFRICA", "175 MIGRANTS MISSING AFTER LEAVING DAKAR", None),
    (27, "AFRICA", "MADAGASCAR SEEKS ARREST OF EX-PRESIDENT", None),
    (28, "AFRICA", "DRC ANNOUNCES $965M MINING INVESTMENT", None),
    (29, "AFRICA", "AMNESTY: PROBE TIGRAY ATTACKS AS WAR CRIMES", None),
    (30, "AFRICA", "47,000 WOMEN KILLED BY PARTNERS IN 2025", None),
    (31, "TECH & SPACE", "PROGRESS MS-36 LAUNCHES TO ISS", None),
    (32, "TECH & SPACE", "ARIANE 6 LAUNCHES 36 AMAZON SATELLITES", None),
    (33, "TECH & SPACE", "FALCON 9 LAUNCHES CLASSIFIED USSF-266", None),
    (34, "TECH & SPACE", "SHENZHOU-24 CREW NAMED, FIRST PAKISTANI IN ORBIT", None),
    (35, "ECONOMY", "SANOFI AGREES $41BN BUY OF INSMED", None),
    (36, "SPORT & CULTURE", "CAS RESTORES SENEGAL AFCON TITLE", None),
    (37, "SPORT & CULTURE", "REAL MADRID COME BACK TO BEAT PSV 5-1", None),
    (38, "SPORT & CULTURE", "SOORYAVANSHI, 15, SCORES 204 OFF 53 BALLS", None),
    (39, "SPORT & CULTURE", "WORLD CHESS: GUKESH-SINDAROV DRAW GAME 1", None),
    (40, "CLIMATE", "COP31 POST-MORTEM: FIRST FAILED SUMMIT SINCE 2009", None),
]

# Story counts per region across the 37 grid stories (4..40); the top 3
# are counted in the masthead's "40 STORIES" total.
REGION_COUNTS = [
    ("EUROPE", 5), ("MIDDLE EAST", 2), ("AMERICAS", 7), ("ASIA", 8),
    ("AFRICA", 5), ("TECH & SPACE", 4), ("ECONOMY", 1),
    ("SPORT & CULTURE", 4), ("CLIMATE", 1),
]

NUMBERS = [
    ("$233B", "Nvidia market value lost in a day"),
    ("103.3", "US consumer confidence, highest since Jan 2025"),
    ("10 of 12", "counts Huawei was found guilty on"),
    ("175", "migrants missing after leaving Dakar"),
    ("47,000", "women and girls killed by partners or family in 2025"),
    ("272", "meningitis cases in Gaza in October, 8x normal"),
]

# Map pins: (number, lat, lon, key label)
PINS = [
    (1, 40.68, -73.94, "Brooklyn \u2014 Huawei verdict"),
    (2, 37.37, -121.96, "Santa Clara \u2014 Nvidia plunge"),
    (3, 24.76, 46.64, "Riyadh \u2014 Houthi drone"),
    (4, 51.14, 23.47, "Che\u0142m \u2014 Russian drone"),
    (5, 31.5, 34.47, "Gaza City \u2014 strikes"),
    (6, 14.8, 42.95, "Hodeidah, Yemen \u2014 evacuation"),
    (7, 14.76, -17.44, "Dakar \u2014 175 migrants"),
    (8, 50.45, 30.52, "Kyiv \u2014 \u20ac115B plea"),
    (9, 37.48, 130.91, "Ulleung \u2014 Russian jets"),
    (10, 40.96, 100.29, "Jiuquan \u2014 Shenzhou-24"),
    (11, 45.96, 63.3, "Baikonur \u2014 Progress MS-36"),
]

DATE_CHECK_BODY = (
    "Not 24 November, so left out: Russian corvette Merkury sunk off "
    "Benghazi (22 Nov, confirmed 23 Nov) \u00b7 COP31 collapse itself "
    "(22 Nov) \u00b7 First Houthi strike on Riyadh\u2019s PIF Tower "
    "(19 Nov) \u00b7 FIFA Women\u2019s World Cup hosts announced (23 Nov) "
    "\u00b7 Jensen Huang returns as Nvidia CEO, shares +31.5% (23 Nov) "
    "\u00b7 BepiColombo enters Mercury orbit (21 Nov) \u00b7 NASA lunar "
    "reactor tender (23 Nov) \u00b7 Cikande candy factory fire, Indonesia "
    "(21-22 Nov, reported 23 Nov)."
)

SOURCES_LINE = (
    "Sources: Reuters \u00b7 AP \u00b7 CNN \u00b7 BBC \u00b7 Al Jazeera \u00b7 "
    "The New York Times \u00b7 Le Monde \u00b7 UN News \u00b7 Euronews \u00b7 "
    "AFP \u00b7 USA Today \u00b7 Yonhap. All stories from Tuesday 24 Nov "
    "2026. Built by @drac-ximer."
)

# Continent outlines (lon, lat), drawn as polygons on the map.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-70, 62), (-55, 52), (-60, 46), (-70, 42), (-75, 35),
     (-80, 26), (-85, 20), (-90, 14), (-95, 16), (-100, 20), (-105, 22),
     (-110, 28), (-115, 32), (-120, 34), (-125, 40), (-125, 48),
     (-135, 58), (-150, 60), (-165, 60)],
    [(-55, 60), (-45, 60), (-40, 64), (-30, 68), (-25, 70), (-30, 76),
     (-45, 76), (-58, 70), (-60, 64)],
    [(-80, 10), (-75, 12), (-70, 12), (-60, 8), (-50, 4), (-45, 0),
     (-40, -5), (-35, -8), (-40, -15), (-45, -22), (-50, -28), (-55, -35),
     (-60, -40), (-65, -45), (-70, -52), (-73, -45), (-75, -35),
     (-78, -25), (-80, -15), (-82, -5), (-80, 5)],
    [(-17, 15), (-15, 25), (-10, 30), (-5, 35), (0, 36), (10, 37),
     (15, 32), (20, 32), (30, 31), (35, 28), (40, 20), (43, 12), (48, 10),
     (51, 12), (45, 5), (40, -2), (38, -10), (35, -18), (32, -25),
     (28, -32), (20, -35), (15, -30), (12, -18), (10, -5), (8, 4), (0, 5),
     (-8, 5), (-15, 10)],
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (5, 53), (8, 55),
     (10, 58), (12, 60), (18, 62), (20, 65), (25, 70), (30, 70), (40, 68),
     (50, 69), (60, 70), (70, 72), (80, 73), (90, 75), (100, 76),
     (110, 74), (120, 73), (130, 72), (140, 72), (150, 70), (160, 69),
     (170, 66), (178, 65), (170, 60), (162, 58), (158, 52), (150, 45),
     (142, 40), (140, 35), (135, 33), (130, 31), (127, 35), (122, 38),
     (120, 32), (115, 25), (110, 20), (108, 12), (105, 8), (100, 8),
     (98, 12), (95, 16), (92, 20), (88, 22), (85, 19), (80, 15), (77, 8),
     (75, 12), (72, 20), (68, 23), (65, 25), (60, 25), (57, 26), (54, 27),
     (52, 28), (50, 30), (48, 30), (46, 32), (44, 35), (42, 38), (40, 40),
     (38, 42), (35, 42), (33, 40), (30, 38), (28, 38), (26, 38), (23, 36),
     (20, 38), (18, 40), (15, 40), (12, 42), (10, 44), (8, 44), (5, 43),
     (3, 43), (0, 40), (-2, 37), (-6, 36), (-9, 37)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    [(130, 31), (132, 33), (134, 34), (137, 35), (139, 37), (141, 39),
     (141, 42), (143, 44), (145, 44), (142, 42), (140, 38), (138, 35),
     (136, 33), (133, 32)],
    [(95, 5), (100, 0), (104, -3), (106, -6), (103, -5), (100, 0)],
    [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (113, -4),
     (110, -2)],
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9), (146, -8),
     (141, -8), (136, -4), (132, -2)],
    [(105, -6), (110, -7), (114, -7), (114, -8), (108, -8), (105, -7)],
    [(119, 0), (121, 1), (123, 0), (121, -2), (120, -4), (119, -2)],
    [(114, -22), (114, -30), (115, -33), (118, -35), (124, -33),
     (130, -32), (135, -35), (138, -35), (140, -38), (145, -38),
     (150, -37), (153, -32), (153, -27), (150, -22), (146, -19),
     (142, -15), (142, -11), (137, -12), (135, -15), (132, -12),
     (130, -13), (126, -14), (122, -17), (118, -20)],
    [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38),
     (175, -40), (172, -43), (168, -46)],
]


# ---------------------------------------------------------------------------
# Drawn illustrations for the three top-story cards (original, no photos).
# Each gets the illustration box (bx, by, bw, bh) inside its card.
# ---------------------------------------------------------------------------
def draw_courthouse(d, bx, by, bw, bh):
    """Card 1: Brooklyn courthouse — navy field, white pediment + columns."""
    d.rectangle([bx, by, bx + bw, by + bh], fill=(28, 42, 74))
    cx = bx + bw / 2
    # Pediment triangle at top centre.
    d.polygon([(cx, by + 5), (cx - 42, by + 26), (cx + 42, by + 26)],
              fill=(255, 255, 255))
    # Four columns below the pediment.
    for i in range(4):
        col_x = cx - 36 + i * 20
        d.rectangle([col_x, by + 29, col_x + 7, by + 47],
                    fill=(255, 255, 255))
    # Base line.
    d.rectangle([cx - 44, by + 48, cx + 44, by + 51], fill=(255, 255, 255))
    d.text((bx + 6, by + 4), "BROOKLYN", font=sans_b(10),
           fill=(255, 255, 255))


def draw_chip(d, bx, by, bw, bh):
    """Card 2: Santa Clara chip — green field, chip square, red fall arrow."""
    d.rectangle([bx, by, bx + bw, by + bh], fill=(18, 90, 40))
    cx = bx + bw / 2
    # Chip body with light-green outline, centred slightly left.
    chip = [cx - 52, by + 11, cx - 18, by + 45]
    d.rectangle(chip, fill=(8, 50, 22), outline=(120, 220, 140), width=2)
    # Pins on both sides of the chip.
    for i in range(3):
        py = by + 16 + i * 9
        d.rectangle([chip[0] - 7, py, chip[0] - 1, py + 4],
                    fill=(120, 220, 140))
        d.rectangle([chip[2] + 1, py, chip[2] + 7, py + 4],
                    fill=(120, 220, 140))
    # Bright inner square.
    d.rectangle([cx - 44, by + 19, cx - 26, by + 37], fill=(60, 200, 90))
    # Thick red falling arrow, down-right across the box.
    d.line([(bx + 118, by + 6), (bx + bw - 14, by + 48)], fill=RED, width=5)
    d.polygon([(bx + bw - 14, by + 48), (bx + bw - 30, by + 40),
               (bx + bw - 28, by + 52)], fill=RED)
    d.text((bx + 6, by + 4), "SANTA CLARA", font=sans_b(10),
           fill=(255, 255, 255))


def draw_tower(d, bx, by, bw, bh):
    """Card 3: Riyadh tower — dark blue field, lit tower, yellow starburst."""
    d.rectangle([bx, by, bx + bw, by + bh], fill=(20, 30, 55))
    cx = bx + bw / 2
    # Tall grey-blue tower.
    d.rectangle([cx - 14, by + 4, cx + 14, by + 52], fill=(110, 130, 160))
    # Lit yellow window lines across the tower.
    for wy in range(by + 10, by + 50, 6):
        d.line([(cx - 10, wy), (cx + 10, wy)], fill=(255, 210, 60), width=1)
    # Yellow starburst near the top-right, with a dot at its centre.
    sx, sy = bx + bw - 42, by + 14
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1),
                   (1, 1), (-1, -1), (1, -1), (-1, 1)]:
        d.line([(sx, sy), (sx + dx * 9, sy + dy * 9)],
               fill=(255, 210, 60), width=2)
    d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 210, 60))
    d.text((bx + 6, by + 4), "RIYADH", font=sans_b(10),
           fill=(255, 255, 255))


ILLUSTRATIONS = [draw_courthouse, draw_chip, draw_tower]


# ---------------------------------------------------------------------------
# Sections, top to bottom.
# ---------------------------------------------------------------------------
def draw_masthead(d):
    centred(d, W // 2, 10, "THE WORLD TODAY", serif_b(54), INK)
    d.line([(M, 76), (RIGHT, 76)], fill=INK, width=2)
    d.text((M, 82), "TUESDAY, 24 NOVEMBER 2026", font=sans_b(13), fill=INK)
    right_aligned(d, RIGHT, 82, "40 STORIES  \u00b7  9 REGIONS  \u00b7  ONE DAY",
                  sans_b(13), INK)
    # Red date band.
    d.rectangle([M, 100, RIGHT, 128], fill=RED)
    centred(d, W // 2, 107,
            "THE DAY IN WORLD NEWS  \u2014  TUESDAY 24 NOVEMBER 2026",
            sans_b(15), (255, 255, 255))
    # Region counts line.
    counts = "   \u00b7   ".join(
        "%s %d" % (name, n) for name, n in REGION_COUNTS)
    centred(d, W // 2, 136, counts, sans_b(12), INK)


def draw_numbers(d):
    d.text((M, 160), "THE DAY IN NUMBERS", font=sans_b(14), fill=RED)
    box_w = (CONTENT_W - 5 * 8) // 6
    top, bottom = 182, 232
    for i, (big, label) in enumerate(NUMBERS):
        bx = M + i * (box_w + 8)
        d.rectangle([bx, top, bx + box_w, bottom], outline=INK, width=1)
        d.text((bx + 8, top + 4), big, font=sans_b(18), fill=INK)
        draw_wrapped(d, bx + 8, top + 27, wrap(label, sans(9), box_w - 14),
                     sans(9), GREY, 10)


def draw_top_stories(d):
    d.text((M, 242), "TOP STORIES", font=sans_b(14), fill=RED)
    card_w = (CONTENT_W - 24) // 3
    card_h = 160
    card_y = 258
    for i in range(3):
        num, region, title, summary = STORIES[i]
        cx = M + i * (card_w + 12)
        d.rectangle([cx, card_y, cx + card_w, card_y + card_h],
                    outline=INK, width=1)
        # Drawn illustration box at the top of the card (1px inset).
        ILLUSTRATIONS[i](d, cx + 1, card_y + 1, card_w - 2, 56)
        # Big red number, then the title beside it.
        d.text((cx + 8, card_y + 62), str(num), font=serif_b(20), fill=RED)
        title_lines = wrap(title, serif_b(17), card_w - 38)
        title_end = draw_wrapped(d, cx + 30, card_y + 62, title_lines,
                                 serif_b(17), INK, 20)
        # Summary below the title.
        draw_wrapped(d, cx + 8, title_end + 4,
                     wrap(summary, sans(11), card_w - 16),
                     sans(11), DARK, 14)


def draw_map(d):
    d.text((M, 426), "WHERE IT HAPPENED", font=sans_b(14), fill=RED)
    map_y, map_h = 444, 140
    d.rectangle([M, map_y, RIGHT, map_y + map_h], fill=SEA, outline=INK,
                width=1)

    def project(lon, lat):
        x = M + (lon + 180) / 360.0 * CONTENT_W
        y = map_y + (85 - lat) / 145.0 * map_h
        return (x, y)

    # Graticule every 30 degrees.
    for lon in range(-150, 180, 30):
        x, _ = project(lon, 85)
        d.line([(x, map_y), (x, map_y + map_h)], fill=GRATICULE, width=1)
    for lat in range(60, -61, -30):
        _, y = project(-180, lat)
        d.line([(M, y), (RIGHT, y)], fill=GRATICULE, width=1)
    # Continents.
    for poly in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    # Numbered pins.
    for num, lat, lon, _label in PINS:
        px, py = project(lon, lat)
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((px, py), str(num), font=sans_b(10), fill=(255, 255, 255),
               anchor="mm")
    # Pin key, two lines.
    key1 = "  \u00b7  ".join(
        "%d. %s" % (num, label) for num, _la, _lo, label in PINS[:6])
    key2 = "  \u00b7  ".join(
        "%d. %s" % (num, label) for num, _la, _lo, label in PINS[6:])
    centred(d, W // 2, 588, key1, sans(9), GREY)
    centred(d, W // 2, 600, key2, sans(9), GREY)
    return 600 + 12


def draw_also(d, y):
    d.text((M, y), "ALSO ON TUESDAY 24 NOVEMBER", font=sans_b(14), fill=RED)
    grid = [s for s in STORIES if s[0] >= 4]
    # Flat region-ordered list, split in half by story count.
    half = (len(grid) + 1) // 2
    columns = [grid[:half], grid[half:]]
    col_w = (CONTENT_W - 20) // 2
    col_x = [M, M + col_w + 20]
    bottom = y
    for ci, stories in enumerate(columns):
        cy = y + 18
        current_region = None
        for num, region, title, _summary in stories:
            if region != current_region:
                d.text((col_x[ci], cy), region, font=sans_b(10), fill=RED)
                cy += 14
                current_region = region
            lines = wrap("%d. %s" % (num, title), sans(10), col_w - 12)
            cy = draw_wrapped(d, col_x[ci] + 12, cy, lines, sans(10), INK,
                              12)
        bottom = max(bottom, cy)
    return bottom


def draw_date_check(d, y):
    d.rectangle([M, y, RIGHT, y + 54], outline=RED, width=2)
    d.text((M + 8, y + 5), "DATE CHECK \u2014 LEFT OUT ON PURPOSE",
           font=sans_b(11), fill=RED)
    draw_wrapped(d, M + 8, y + 17, wrap(DATE_CHECK_BODY, sans(10), 960),
                 sans(10), INK, 12)
    return y + 54


def draw_footer(d, y):
    d.line([(M, y), (RIGHT, y)], fill=INK, width=1)
    draw_wrapped(d, M, y + 4, wrap(SOURCES_LINE, sans(8), CONTENT_W),
                 sans(8), GREY, 11)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_numbers(d)
    draw_top_stories(d)
    after_map = draw_map(d)
    grid_bottom = draw_also(d, after_map + 2)
    check_bottom = draw_date_check(d, grid_bottom + 8)
    draw_footer(d, check_bottom + 6)
    return img


def main():
    out = os.environ.get("RENDER_OUT", "entry.png")
    img = render()
    img.save(out)
    print("wrote %s (%dx%d)" % (out, img.width, img.height))


if __name__ == "__main__":
    main()
