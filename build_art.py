#!/usr/bin/env python3
"""Generate the 17 November 2026 front-page image (art.png).

Fresh PIL drawing: masthead, a numbered world-map strip, eleven
featured panels with small pictograms, nineteen numbered briefs,
and a one-line footer. Everything is drawn from the data tables
below; there is no network access and no external image input.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "art.png")
W, H = 1024, 1024
PAPER = (250, 247, 238)
INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (110, 108, 100)
LIGHT = (228, 224, 210)
MAP_FILL = (214, 210, 196)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
F_REG = lambda s: font("DejaVuSans.ttf", s)

# (kicker, headline, deck, source, icon, lon, lat)
FEATURED = [
    ("UKRAINE \u2022 WAR", "KERCH BRIDGE HIT AGAIN",
     "Ukraine struck the bridge to occupied Crimea; a road span "
     "collapsed and traffic was suspended. Moscow vows to rebuild. "
     "Second strike in under 24 hours.",
     "BBC \u00b7 Al Jazeera", "bridge", 34.0, 45.3),
    ("GULF \u2022 ENERGY", "TANKERS HIT BY MINES OFF HORMUZ",
     "Iran's Guard navy says two tankers hit mines and caught fire "
     "south of the strait; its regular navy says more were hit "
     "east. Iran's claim; not verified.",
     "Al Jazeera \u00b7 Reuters", "tanker", 57.0, 26.0),
    ("GULF \u2022 US FORCES", "IRAN DRONES HIT US SITE IN BAHRAIN",
     "Iran fired drones at a US radar site in Bahrain, its third "
     "strike on American targets there in days, after a two-month lull.",
     "PBS NewsHour", "drone", 50.5, 26.0),
    ("ASIA \u2022 DIPLOMACY", "TRUMP IN MANILA; XI\u2013TRUMP\u2013PUTIN MEET IN SHENZHEN",
     "Trump arrived in the Philippines for the ASEAN summit. China "
     "confirmed Xi, Trump and Putin meet Thursday 19 Nov in Shenzhen "
     "on the APEC sidelines.",
     "AP \u00b7 Outlook India", "summit", 121.0, 14.6),
    ("SPACE", "SPACEX CATCHES STARSHIP FROM ORBIT",
     "SpaceX caught the Starship upper stage (Ship 42) with the tower "
     "arms after about fourteen orbits, the first ship recovered "
     "from orbit. The booster was lost.",
     "17 Nov reporting", "ship", -97.0, 25.5),
    ("SPACE \u2022 LAUNCH", "VULCAN ROCKET FAILS, 40 SATELLITES LOST",
     "A ULA Vulcan rocket failed about 10 minutes after launch from "
     "Cape Canaveral, destroying 40 Amazon Leo internet satellites.",
     "ULA \u00b7 Spaceflight Now", "rocket", -80.5, 28.4),
    ("MARKETS", "NVIDIA REPORTS AFTER HUANG EXIT",
     "Nvidia reports earnings after Tuesday's close, its first since "
     "Jensen Huang's resignation as chief.",
     "Market reporting", "chip", -122.0, 37.4),
    ("MONEY \u2022 USA", "JPMORGAN BLAMES SOFTWARE BUG",
     "JPMorgan Chase says a software bug, not a cyberattack, slowed "
     "online banking, branch transactions and Zelle payments on Monday.",
     "ABC News", "bank", -74.0, 40.7),
    ("EUROPE \u2022 SECURITY", "ESTONIA TO SHUT RUSSIA BORDER",
     "Estonia will close all border crossings with Russia from "
     "1 December, citing a foiled Russian plot to bomb a drone plant.",
     "NPR", "border", 25.0, 58.5),
    ("EUROPE \u2022 MIGRATION", "FIVE NATIONS PLAN RWANDA RETURNS HUB",
     "Germany, Denmark, Austria, Greece and the Netherlands announced "
     "a joint return facility in Rwanda for rejected asylum seekers.",
     "17 Nov reporting", "hub", 30.0, -2.0),
    ("SPACE \u2022 SCIENCE", "EUCLID OPENS 900 MILLION GALAXIES",
     "ESA's Euclid telescope released its first major dataset covering "
     "900 million galaxies, including 31 ancient quasars, two of them "
     "record-breaking.",
     "ESA", "galaxy", 10.0, 48.0),
]

BRIEFS = [
    "Houthis say they launched drones at Saudi Arabia's East-West oil pipeline as they push toward Aden. (Houthi claim)",
    "Iraq orders its army into a stronghold of Iran-backed Kataib Hezbollah; the group vows to resist.",
    "Japan scrambled fighter jets and lodged a protest with Moscow.",
    "Microsoft blames last week's global outage on a latent defect plus extra load and reduced server capacity; over 80% of servers hit.",
    "US petrol averages $3.78 a gallon, down about 20 cents in a week.",
    "Singapore seeks trusted access to advanced AI processors amid US export curbs.",
    "US Commerce Dept introduces new licensing for advanced processor sales to data centres across Southeast Asia.",
    "Bus plunges into a ravine in Uttarakhand, India \u2014 NDTV reports 6 dead, 20 hurt; The Hindu reports 8 dead, 26 hurt.",
    "Notre Dame beats Navy 35\u201313 at Gillette Stadium.",
    "Bosnia beats Romania 2\u20131 in Zenica; Romania face a Nations League relegation play-off.",
    "Lamar Jackson has thumb surgery; Ravens set a 6\u201310 week recovery line.",
    "Europe's Hera spacecraft imaged the crater-covered side of asteroid Didymos.",
    "Millions of red crabs begin their annual migration on Christmas Island, Australia.",
    "Two gorillas at Ramat Gan Safari formed a living ladder to reach high branches (Tel Aviv University researchers).",
    "Vitamin B12 largely reverses developmental defects in a worm model of rare Verheij syndrome \u2014 early, animal-level work. (ScienceDaily)",
    "China's thermal power generation fell year on year for a fourth straight month in October as wind and solar grew.",
    "Cape Verde: Jos\u00e9 Maria Neves wins a second term as president, provisional results.",
    "Cervical cancer could become the first cancer ever eliminated, using vaccines, screening and treatment that already exist.",
    "Scientists discover bacteria can manufacture their own metal-organic frameworks (MOFs) \u2014 the first natural MOF. (Diamond Light Source)",
]

LEGEND = [
    "1 Kerch  2 Hormuz  3 Bahrain  4 Manila  5 Gulf of Mexico",
    "6 Cape Canaveral  7 California  8 New York  9 Estonia",
    "10 Rwanda  11 Europe (ESA)",
]


def wrap(draw, text, fnt, width):
    """Greedy word wrap to the given pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill=INK, leading=3):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def icon(draw, kind, cx, cy, s=15):
    """Small black/red pictogram centred at (cx, cy), half-size s."""
    if kind == "bridge":
        draw.arc([cx - s, cy - s, cx + s, cy + s], 200, 340, fill=INK, width=2)
        draw.line([(cx - s, cy + s // 2), (cx + s, cy + s // 2)], fill=INK, width=2)
        for px in (-s // 2, 0, s // 2):
            draw.line([(cx + px, cy), (cx + px, cy + s // 2)], fill=INK, width=2)
    elif kind == "tanker":
        draw.polygon([(cx - s, cy), (cx + s, cy - 2), (cx + s - 3, cy + s // 2),
                      (cx - s + 2, cy + s // 2)], fill=INK)
        draw.line([(cx - s // 3, cy), (cx - s // 3, cy - s // 2)], fill=INK, width=2)
        draw.polygon([(cx - s // 3, cy - s), (cx, cy - s // 2),
                      (cx + s // 3, cy - s)], fill=RED)
    elif kind == "drone":
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=INK)
        for dx, dy in ((-s, -s // 2), (s, -s // 2), (-s, s // 2), (s, s // 2)):
            draw.line([(cx, cy), (cx + dx, cy + dy)], fill=INK, width=2)
            draw.ellipse([cx + dx - 4, cy + dy - 2, cx + dx + 4, cy + dy + 2],
                         outline=INK, width=2)
    elif kind == "summit":
        for i, px in enumerate((-s, 0, s)):
            draw.line([(cx + px, cy - s // 2), (cx + px, cy + s // 2)],
                      fill=INK, width=2)
            draw.polygon([(cx + px, cy - s // 2), (cx + px + 8, cy - s // 4),
                          (cx + px, cy)], fill=RED if i == 1 else INK)
    elif kind == "ship":
        draw.polygon([(cx, cy - s), (cx + 5, cy + 2), (cx - 5, cy + 2)], fill=INK)
        draw.rectangle([cx - 5, cy + 2, cx + 5, cy + s // 2], fill=INK)
        draw.line([(cx - s, cy - 2), (cx - 6, cy - 2)], fill=RED, width=3)
        draw.line([(cx + 6, cy - 2), (cx + s, cy - 2)], fill=RED, width=3)
    elif kind == "rocket":
        draw.polygon([(cx, cy - s), (cx + 5, cy - 2), (cx - 5, cy - 2)], fill=INK)
        draw.rectangle([cx - 5, cy - 2, cx + 5, cy + s // 2], fill=INK)
        for dx, dy in ((-9, -8), (9, -8), (0, -12)):
            draw.line([(cx, cy + s // 2), (cx + dx, cy + dy)], fill=RED, width=2)
    elif kind == "chip":
        draw.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                       outline=INK, width=2)
        draw.rectangle([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
        for px in (-s // 4, 0, s // 4):
            draw.line([(cx + px, cy - s // 2 - 4), (cx + px, cy - s // 2)],
                      fill=INK, width=2)
            draw.line([(cx + px, cy + s // 2), (cx + px, cy + s // 2 + 4)],
                      fill=INK, width=2)
    elif kind == "bank":
        draw.polygon([(cx - s, cy - 2), (cx, cy - s), (cx + s, cy - 2)], fill=INK)
        for px in (-s // 2, 0, s // 2):
            draw.line([(cx + px, cy), (cx + px, cy + s // 2)], fill=INK, width=2)
        draw.line([(cx - s, cy + s // 2), (cx + s, cy + s // 2)], fill=INK, width=2)
        draw.line([(cx + s // 2, cy - s - 4), (cx + s // 2 + 5, cy - s + 2)],
                  fill=RED, width=2)
    elif kind == "border":
        for px in range(-s, s + 1, 6):
            draw.line([(cx + px, cy - s // 2), (cx + px, cy + s // 2)],
                      fill=INK, width=2)
        draw.line([(cx - s, cy), (cx + s, cy)], fill=RED, width=3)
    elif kind == "hub":
        draw.polygon([(cx - s, cy), (cx, cy - s // 2), (cx + s, cy),
                      (cx + s - 3, cy + s // 2), (cx - s + 3, cy + s // 2)],
                     outline=INK, width=2)
        draw.line([(cx - s - 4, cy - s // 2), (cx + s + 4, cy - s // 2)],
                  fill=RED, width=2)
        draw.polygon([(cx + s + 4, cy - s // 2), (cx + s - 2, cy - s // 2 - 4),
                      (cx + s - 2, cy - s // 2 + 4)], fill=RED)
    else:  # galaxy
        draw.ellipse([cx - s, cy - s, cx + s, cy + s], outline=INK, width=2)
        for dx, dy in ((-6, -4), (4, -7), (7, 4), (-4, 6), (0, 0)):
            draw.ellipse([cx + dx - 2, cy + dy - 2, cx + dx + 2, cy + dy + 2],
                         fill=RED if (dx, dy) == (0, 0) else INK)


def lonlat_to_xy(lon, lat, x0, y0, w, h):
    x = x0 + (lon + 180.0) / 360.0 * w
    y = y0 + (90.0 - lat) / 180.0 * h
    return x, y


def draw_map(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], outline=INK, width=1)
    # Rough continent blobs (lon/lat boxes), light fill.
    blobs = [
        [(-168, 72), (-140, 70), (-120, 70), (-95, 68), (-80, 62), (-60, 48),
         (-75, 35), (-95, 20), (-105, 22), (-120, 35), (-135, 55), (-168, 62)],
        [(-80, 10), (-60, 5), (-40, -5), (-35, -25), (-55, -40), (-70, -35),
         (-75, -15), (-80, 0)],
        [(-10, 70), (10, 70), (25, 60), (30, 45), (10, 38), (-5, 37), (-10, 50)],
        [(-15, 35), (10, 37), (30, 32), (35, 12), (40, -5), (35, -25),
         (20, -35), (12, -18), (10, 0), (-5, 5), (-15, 15)],
        [(40, 70), (70, 72), (100, 75), (140, 72), (160, 65), (140, 55),
         (130, 45), (120, 30), (105, 10), (95, 8), (80, 8), (60, 25),
         (45, 35), (40, 55)],
        [(113, -12), (130, -12), (145, -15), (150, -25), (140, -38),
         (130, -32), (115, -32)],
    ]
    for blob in blobs:
        pts = [lonlat_to_xy(lon, lat, x0, y0, w, h) for lon, lat in blob]
        draw.polygon(pts, fill=MAP_FILL, outline=GREY)
    for i, item in enumerate(FEATURED, start=1):
        px, py = lonlat_to_xy(item[5], item[6], x0, y0, w, h)
        # Nudge overlapping pins apart slightly.
        nudges = {2: (0, 7), 3: (0, -7), 5: (0, 6), 6: (0, -8), 8: (10, 3)}
        dx, dy = nudges.get(i, (0, 0))
        px, py = px + dx, py + dy
        draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255))
        draw.text((px, py), str(i), font=F_BOLD(10), fill=(255, 255, 255),
                  anchor="mm")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # --- Masthead ---
    draw.text((512, 18), "THE SEVENTEENTH", font=F_SERIF(52), fill=INK, anchor="ma")
    draw.line([(12, 82), (1012, 82)], fill=INK, width=2)
    draw.line([(12, 86), (1012, 86)], fill=RED, width=2)
    draw.text((12, 90), "TUESDAY 17 NOVEMBER 2026", font=F_BOLD(15), fill=INK)
    draw.text((1012, 90), "30 STORIES \u00b7 6 CONTINENTS", font=F_BOLD(15),
              fill=RED, anchor="ra")

    # --- World map strip + legend ---
    map_x, map_y, map_w, map_h = 12, 112, 640, 62
    draw_map(draw, map_x, map_y, map_w, map_h)
    lx = 664
    draw.text((lx, 112), "WHERE IT HAPPENED", font=F_BOLD(11), fill=RED)
    y = 128
    for line in LEGEND:
        draw.text((lx, y), line, font=F_REG(11), fill=INK)
        y += 15

    # --- Featured grid: 3 columns x 4 rows (11 panels) ---
    grid_x, grid_y = 12, 182
    col_w, row_h, gap = 328, 128, 6
    for idx, item in enumerate(FEATURED):
        kicker, headline, deck, source, kind = item[0], item[1], item[2], item[3], item[4]
        row, col = divmod(idx, 3)
        # Last row: centre the two remaining panels? Keep left-aligned grid;
        # 11th panel spans the last row's first cell, others stay empty.
        px = grid_x + col * (col_w + gap)
        py = grid_y + row * (row_h + gap)
        draw.rectangle([px, py, px + col_w, py + row_h], outline=INK, width=1)
        draw.rectangle([px, py, px + col_w, py + 3], fill=RED)
        # Kicker + pictogram on the top line.
        draw.text((px + 8, py + 8), f"{idx + 1}. {kicker}", font=F_BOLD(10), fill=RED)
        # Pictogram sits beside the kicker, above the headline, so it
        # can never overlap headline text.
        icon(draw, kind, px + col_w - 20, py + 16, s=11)
        # Headline, up to 2 lines at 15px bold.
        hl = wrap(draw, headline, F_BOLD(15), col_w - 16)[:2]
        hy = draw_lines(draw, hl, px + 8, py + 28, F_BOLD(15), leading=1)
        # Deck, up to 3 lines at 11px.
        dl = wrap(draw, deck, F_REG(11), col_w - 16)[:3]
        dy = draw_lines(draw, dl, px + 8, hy + 3, F_REG(11), leading=1)
        # Source pinned to the panel bottom.
        draw.text((px + 8, py + row_h - 16), "Source: " + source,
                  font=F_REG(9), fill=GREY)

    # --- Fill the empty 12th cell with day-in-numbers (all figures
    # taken from the featured stories above; nothing new invented). ---
    nx = grid_x + 2 * (col_w + gap)
    ny = grid_y + 3 * (row_h + gap)
    draw.rectangle([nx, ny, nx + col_w, ny + row_h], outline=INK, width=1)
    draw.rectangle([nx, ny, nx + col_w, ny + 3], fill=RED)
    draw.text((nx + 8, ny + 8), "THE DAY IN NUMBERS", font=F_BOLD(10), fill=RED)
    stats = [
        ("900M", "galaxies in Euclid's first dataset"),
        ("40", "Amazon Leo satellites lost"),
        ("$3.78", "average US petrol price per gallon"),
        ("35\u201313", "Notre Dame over Navy at Gillette Stadium"),
        ("2\u20131", "Bosnia over Romania in Zenica"),
        ("6\u201310 wks", "Ravens' recovery line for Lamar Jackson"),
    ]
    sy = ny + 30
    for big, small in stats:
        draw.text((nx + 8, sy), big, font=F_BOLD(13), fill=INK)
        draw.text((nx + 92, sy + 2), small, font=F_REG(11), fill=INK)
        sy += 16

    # --- Briefs: one numbered line each, full width ---
    by = grid_y + 4 * row_h + 3 * gap + 6
    draw.text((12, by), "IN BRIEF \u2014 19 MORE STORIES", font=F_BOLD(13), fill=INK)
    draw.line([(12, by + 19), (1012, by + 19)], fill=INK, width=1)
    for i, brief in enumerate(BRIEFS):
        yy = by + 26 + i * 13
        draw.text((12, yy), f"{i + 12}.", font=F_BOLD(11), fill=RED)
        lines = wrap(draw, brief, F_REG(11), 1012 - 12 - 30)[:1]
        draw_lines(draw, lines, 42, yy, F_REG(11), leading=1)

    # --- Footer ---
    fy = H - 14
    draw.line([(12, fy - 7), (1012, fy - 7)], fill=INK, width=1)
    draw.text((512, fy), "All stories as reported on 17 November 2026; "
              "contested claims are labelled as claims.",
              font=F_REG(11), fill=INK, anchor="ma")

    img.save(OUT, optimize=True)
    print(f"wrote {OUT} {img.size} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
