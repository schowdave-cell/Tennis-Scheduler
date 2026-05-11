import streamlit as st
import pandas as pd
import random
import io
import requests

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Tennis Drop-In Scheduler",
    page_icon="🎾",
    layout="wide",
)

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #0d1117;
    color: #e6edf3;
}

h1, h2, h3 {
    font-family: 'Bebas Neue', sans-serif;
    letter-spacing: 2px;
}

.hero {
    background: linear-gradient(135deg, #1a2332 0%, #0d1117 50%, #162032 100%);
    border: 1px solid #2d9c4a33;
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: "🎾";
    position: absolute;
    right: 2rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 6rem;
    opacity: 0.08;
}

.hero h1 {
    font-size: 3.5rem;
    color: #4ade80;
    margin: 0;
    line-height: 1;
}

.hero p {
    color: #c9d1d9;
    font-size: 1.05rem;
    margin-top: 0.5rem;
    font-weight: 300;
}

.court-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.8rem;
    border-left: 4px solid #4ade80;
    transition: all 0.2s;
}

.court-card:hover {
    border-left-color: #86efac;
    background: #1c2330;
}

.court-label {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    color: #4ade80;
    letter-spacing: 2px;
    margin-bottom: 0.3rem;
}

.match-text {
    font-size: 1.05rem;
    color: #e6edf3;
    font-weight: 500;
}

.match-type-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-left: 8px;
    vertical-align: middle;
}

.badge-doubles {
    background: #1e3a5f;
    color: #60a5fa;
    border: 1px solid #3b82f640;
}

.badge-singles {
    background: #3a1e1e;
    color: #f87171;
    border: 1px solid #ef444440;
}

.round-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.2rem;
    color: #e6edf3;
    letter-spacing: 3px;
    border-bottom: 2px solid #4ade8044;
    padding-bottom: 0.5rem;
    margin-bottom: 1.2rem;
    margin-top: 1.5rem;
}

.stat-pill {
    display: inline-block;
    background: #21262d;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 0.4rem 0.9rem;
    font-size: 0.85rem;
    color: #c9d1d9;
    margin-right: 0.5rem;
    margin-bottom: 0.5rem;
}

.stat-pill span {
    color: #4ade80;
    font-weight: 600;
}

.court-card.imbalanced {
    border-left-color: #f59e0b;
}

.imbalance-flag {
    display: inline-block;
    font-size: 0.75rem;
    color: #fbbf24;
    background: #2d1b0044;
    border: 1px solid #f59e0b55;
    border-radius: 6px;
    padding: 1px 8px;
    margin-left: 6px;
    vertical-align: middle;
}

.bye-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-left: 4px solid #f59e0b;
    border-radius: 12px;
    padding: 0.8rem 1.2rem;
    margin-bottom: 0.8rem;
    color: #fbbf24;
    font-size: 0.9rem;
}

.warning-box {
    background: #2d1b00;
    border: 1px solid #f59e0b55;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    color: #fbbf24;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

.success-box {
    background: #0d2818;
    border: 1px solid #4ade8055;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    color: #4ade80;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

.stButton > button {
    background: #4ade80;
    color: #0d1117;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    letter-spacing: 2px;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 2rem;
    width: 100%;
    cursor: pointer;
    transition: all 0.2s;
}

.stButton > button:hover {
    background: #86efac;
    transform: translateY(-1px);
}

.stDownloadButton > button {
    background: #21262d;
    color: #4ade80;
    border: 1px solid #4ade8044;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    border-radius: 8px;
    padding: 0.4rem 1rem;
    width: 100%;
}

.stDownloadButton > button:hover {
    background: #2d3748;
}

div[data-testid="stFileUploader"] {
    background: #161b22;
    border: 2px dashed #30363d;
    border-radius: 12px;
    padding: 1.5rem;
}

div[data-testid="stFileUploader"]:hover {
    border-color: #4ade80;
}

.sidebar .stSelectbox, .sidebar .stSlider {
    background: #161b22;
}

[data-testid="stSidebar"] {
    background: #0d1117;
    border-right: 1px solid #21262d;
}

[data-testid="stSidebar"] * {
    color: #e6edf3 !important;
}

[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {
    color: #e6edf3 !important;
}

[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] small {
    color: #c9d1d9 !important;
}

/* Hide Streamlit's default header/toolbar */
header[data-testid="stHeader"] {
    display: none !important;
}

#MainMenu, footer, header {
    visibility: hidden !important;
    height: 0 !important;
}

/* Fix number input and all input text colors */
input[type="number"], input[type="text"], input {
    color: #e6edf3 !important;
    background-color: #21262d !important;
    border: 1px solid #30363d !important;
}

[data-testid="stNumberInput"] input {
    color: #e6edf3 !important;
    background-color: #21262d !important;
}

/* Fix all form element text in sidebar */
[data-testid="stSidebar"] input {
    color: #e6edf3 !important;
    background-color: #21262d !important;
}


    background: #161b22;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #30363d;
}

.stDataFrame {
    background: #161b22 !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Data structures & helpers
# ─────────────────────────────────────────────

def clean_str(val):
    if pd.isna(val) or str(val).strip() == "":
        return ""
    return str(val).strip()

def parse_level(val):
    try:
        return float(str(val).strip())
    except Exception:
        return 3.5  # default level

def find_level_column(df):
    """Accept 'Level', 'USTA Level', 'Usta Level', 'level', etc."""
    for col in df.columns:
        if col.strip().lower().replace("usta ", "") == "level":
            return col
    return None

def find_col(row, *candidates):
    """Return the first matching column value from a list of candidate names."""
    for c in candidates:
        if c in row.index and not pd.isna(row[c]) and str(row[c]).strip() != "":
            return row[c]
    return ""

def load_players(df):
    # Normalize column names (strip whitespace)
    df.columns = [c.strip() for c in df.columns]
    level_col = find_level_column(df)

    players = []
    for _, row in df.iterrows():
        name = clean_str(row.get("Name", ""))
        if not name:
            continue

        # Filter out legend/instruction rows — real player names are short
        # and parse_level on their Level cell should succeed
        raw_level = row[level_col] if level_col and level_col in row.index else ""
        level = parse_level(raw_level)

        # Skip rows where name is suspiciously long (legend text) or level didn't parse
        if len(name) > 50:
            continue
        if str(raw_level).strip() == "" or level == 3.5 and not str(raw_level).strip().replace(".", "").isdigit():
            # Level is blank — only accept if name looks like a real name (short, no emoji)
            if len(name) > 30 or any(ord(c) > 127 for c in name):
                continue

        # Preference: default to "Either" if blank
        pref = clean_str(find_col(row, "Preference")).capitalize()
        if pref not in ("Singles", "Doubles", "Either"):
            pref = "Either"

        players.append({
            "name": name,
            "level": level,
            "pref": pref,
            "partner": clean_str(find_col(row, "Fixed Partner", "Partner")),
            "opponent": clean_str(find_col(row, "Fixed Opponent", "Opponent")),
            "avoid": clean_str(find_col(row, "Avoid")),
        })
    return players

# ─────────────────────────────────────────────
# Scheduling logic
# ─────────────────────────────────────────────

def find_player(name, players):
    for p in players:
        if p["name"].lower() == name.lower():
            return p
    return None

def avg_level(group):
    return sum(p["level"] for p in group) / len(group)

def team_balance_score(t1, t2):
    """Lower is better balanced."""
    return abs(avg_level(t1) - avg_level(t2))

def match_key(t1, t2):
    """Canonical frozenset key for a doubles matchup, order-independent."""
    return frozenset([
        frozenset(p["name"] for p in t1),
        frozenset(p["name"] for p in t2),
    ])

def form_teams(pool, rng=None, avoid_partners=None):
    """
    Phase 1: Form teams of 2 from the pool.
    - Fixed partner pairs become teams immediately (always, both rounds).
    - Free players are paired by closest level (Round 1) or shuffled (Round 2).
    - avoid_partners: set of frozensets {name_a, name_b} to avoid re-pairing in Round 2.
      Soft constraint — respected if a valid alternative exists, ignored otherwise.
    Returns list of teams (each a list of 2 players) and leftover players (0 or 1).
    """
    avoid_partners = avoid_partners or set()
    remaining = list(pool)
    used = set()
    teams = []

    # Lock fixed partner pairs first — never affected by avoid_partners
    for p in remaining:
        if p["name"] in used or not p["partner"]:
            continue
        partner = find_player(p["partner"], remaining)
        if partner and partner["name"] not in used:
            teams.append([p, partner])
            used.add(p["name"])
            used.add(partner["name"])

    free = [p for p in remaining if p["name"] not in used]

    if rng:
        rng.shuffle(free)
    else:
        free.sort(key=lambda x: x["level"])

    # Greedy pairing of free players, avoiding Round 1 partners where possible.
    # For each unpaired player, find the best available partner:
    #   prefer (not a repeat partner, closest level) over (repeat partner, closest level)
    unpaired = list(free)
    while len(unpaired) >= 2:
        p = unpaired.pop(0)
        best_idx = None
        best_score = None
        for i, candidate in enumerate(unpaired):
            gap = abs(p["level"] - candidate["level"])
            is_repeat = frozenset([p["name"], candidate["name"]]) in avoid_partners
            score = (1 if is_repeat else 0, gap)
            if best_score is None or score < best_score:
                best_score = score
                best_idx = i
        partner = unpaired.pop(best_idx)
        teams.append([p, partner])

    leftover = unpaired  # 0 or 1 player remaining
    return teams, leftover


def optimal_match_teams(teams, rng=None):
    """
    Globally optimal team matching for Round 1.
    Finds the pairing of all teams that minimizes the TOTAL level gap across all courts.
    Uses recursive search with pruning — efficient up to ~14 teams (7 courts).
    Falls back to greedy for larger groups.
    rng: if provided, shuffles teams before search so equally-optimal solutions
         come out in different orders on repeated clicks.
    Returns (matches, leftover_teams) — leftover_teams is [] or [one_team].
    """
    if len(teams) > 14:
        return greedy_match_teams(teams, avoid_matchups=None)

    remaining = list(teams)

    # Shuffle before search so tied solutions surface in different orders each click
    if rng:
        rng.shuffle(remaining)

    leftover_teams = []
    if len(remaining) % 2 == 1:
        remaining.sort(key=lambda t: avg_level(t))
        mid = len(remaining) // 2
        leftover_teams = [remaining.pop(mid)]

    if not remaining:
        return [], leftover_teams

    best_result = [None]
    best_score = [float("inf")]

    def search(unmatched, current_matches, current_score):
        if not unmatched:
            if current_score < best_score[0]:
                best_score[0] = current_score
                best_result[0] = list(current_matches)
            return
        if current_score >= best_score[0]:
            return
        first = unmatched[0]
        rest = unmatched[1:]
        for i, other in enumerate(rest):
            gap = abs(avg_level(first) - avg_level(other))
            new_unmatched = rest[:i] + rest[i+1:]
            search(new_unmatched, current_matches + [(first, other)], current_score + gap)

    search(remaining, [], 0)
    return best_result[0] or [], leftover_teams


def greedy_match_teams(teams, avoid_matchups=None):
    """
    Greedy team matching for Round 2.
    Sorts by avg level, pairs highest with closest non-repeat opponent.
    """
    avoid_matchups = avoid_matchups or set()
    remaining = sorted(teams, key=lambda t: avg_level(t), reverse=True)
    matches = []

    while len(remaining) >= 2:
        top = remaining.pop(0)
        best_idx = None
        best_score = None

        for i, candidate in enumerate(remaining):
            gap = abs(avg_level(top) - avg_level(candidate))
            is_repeat = match_key(top, candidate) in avoid_matchups
            score = (1 if is_repeat else 0, gap)
            if best_score is None or score < best_score:
                best_score = score
                best_idx = i

        opponent = remaining.pop(best_idx)
        matches.append((top, opponent))

    leftover_teams = remaining
    return matches, leftover_teams


def make_doubles_matches(pool, fixed_partners, rng=None, r1_rng=None, avoid_matchups=None, avoid_partners=None):
    """
    Form doubles matches from pool using two-phase approach:
      Phase 1 — form_teams: lock fixed pairs, pair free players by level (avoid R1 partners)
      Phase 2 — match teams:
        Round 1 (rng=None): optimal global matching to minimize total level gap
        Round 2 (rng set):  greedy matching, also avoids R1 opponent repeats
    Scales efficiently to 25+ players.
    """
    avoid_matchups = avoid_matchups or set()

    teams, leftover_players = form_teams(pool, rng=rng, avoid_partners=avoid_partners)

    if rng is None:
        matches, leftover_teams = optimal_match_teams(teams, rng=r1_rng)
    else:
        matches, leftover_teams = greedy_match_teams(teams, avoid_matchups=avoid_matchups)

    leftover = [p for team in leftover_teams for p in team] + leftover_players
    return matches, leftover

def make_singles_matches(pool):
    """Form singles matches from pool. Returns matches and leftover."""
    sorted_pool = sorted(pool, key=lambda x: x["level"])
    matches = []
    i = 0
    while i + 1 < len(sorted_pool):
        matches.append((sorted_pool[i], sorted_pool[i+1]))
        i += 2
    leftover = sorted_pool[i:] if i < len(sorted_pool) else []
    return matches, leftover

def players_needed(n_singles, n_doubles):
    """Total players needed for n singles + n doubles courts."""
    return n_singles * 2 + n_doubles * 4


def assign_round1(players, rng=None, max_courts=None):
    """
    Round 1 scheduling with optional court limit.
    If court limit forces sit-outs, all matches become doubles to maximize court usage.
    Returns: singles_matches, doubles_matches, on_deck (sit-outs), r1_matchup_keys, r1_partner_pairs
    """
    n = len(players)
    # How many courts do we need with normal singles/doubles split?
    n_singles_pref = sum(1 for p in players if p["pref"] == "Singles")
    singles_courts_needed = n_singles_pref // 2
    remaining_after_singles = n - (singles_courts_needed * 2)
    doubles_courts_needed = remaining_after_singles // 4
    # Leftover players (1-3) either get a bye or fold into singles — no extra court
    total_courts_needed = singles_courts_needed + doubles_courts_needed

    # If no court limit or we fit within it, run normally
    force_all_doubles = False
    on_deck = []
    active_players = list(players)

    if max_courts and total_courts_needed > max_courts:
        force_all_doubles = True
        max_players = max_courts * 4
        if n > max_players:
            # Players with hard constraints always get court priority
            constrained = [p for p in players if p["partner"] or p["opponent"]]
            free = [p for p in players if not p["partner"] and not p["opponent"]]
            # Shuffle free players so sitouts rotate on each click
            if rng:
                rng.shuffle(free)
            priority = constrained + free
            active_players = priority[:max_players]
            on_deck = priority[max_players:]

    used = set()
    singles_matches = []
    doubles_matches = []

    if not force_all_doubles:
        # Normal flow: fixed opponent singles → singles-only → doubles
        for p in active_players:
            if p["name"] in used or not p["opponent"]:
                continue
            opp = find_player(p["opponent"], active_players)
            if opp and opp["name"] not in used:
                singles_matches.append((p, opp))
                used.add(p["name"])
                used.add(opp["name"])

        singles_pool = [p for p in active_players if p["pref"] == "Singles" and p["name"] not in used]
        s_matches, s_leftover = make_singles_matches(singles_pool)
        singles_matches.extend(s_matches)
        for m in s_matches:
            used.add(m[0]["name"])
            used.add(m[1]["name"])
        for p in s_leftover:
            used.add(p["name"])
            on_deck.append(p)

        doubles_pool = [p for p in active_players if p["name"] not in used]
        d_matches, d_leftover = make_doubles_matches(doubles_pool, {}, rng=None, r1_rng=rng)
        doubles_matches.extend(d_matches)
        for m in d_matches:
            for t in m:
                for pl in t:
                    used.add(pl["name"])
        if d_leftover:
            extra_s, extra_bye = make_singles_matches(d_leftover)
            singles_matches.extend(extra_s)
            on_deck.extend(extra_bye)
    else:
        # Court-constrained: all doubles, no singles
        d_matches, d_leftover = make_doubles_matches(active_players, {}, rng=None, r1_rng=rng)
        doubles_matches.extend(d_matches)
        for m in d_matches:
            for t in m:
                for pl in t:
                    used.add(pl["name"])
        on_deck.extend(d_leftover)

    r1_matchup_keys = {match_key(t1, t2) for t1, t2 in doubles_matches}
    r1_partner_pairs = set()
    for t1, t2 in doubles_matches:
        for team in (t1, t2):
            if not any(p["partner"] for p in team):
                r1_partner_pairs.add(frozenset(p["name"] for p in team))

    return singles_matches, doubles_matches, on_deck, r1_matchup_keys, r1_partner_pairs


def assign_round2(players, rng, r1_matchup_keys=None, r1_partner_pairs=None, max_courts=None):
    """
    Round 2: reshuffle, no fixed opponent constraint.
    Respects court limit. Forces all-doubles if court-constrained.
    """
    n = len(players)
    force_all_doubles = False
    on_deck = []
    active_players = list(players)

    # Estimate courts needed (no singles pref check — round 2 ignores fixed opponents)
    n_singles_pref = sum(1 for p in players if p["pref"] == "Singles")
    singles_courts_needed = n_singles_pref // 2
    remaining_after_singles = n - (singles_courts_needed * 2)
    doubles_courts_needed = remaining_after_singles // 4
    total_courts_needed = singles_courts_needed + doubles_courts_needed

    if max_courts and total_courts_needed > max_courts:
        force_all_doubles = True
        max_players = max_courts * 4
        if n > max_players:
            constrained = [p for p in players if p["partner"]]
            free = [p for p in players if not p["partner"]]
            rng.shuffle(free)
            priority = constrained + free
            active_players = priority[:max_players]
            on_deck = priority[max_players:]

    used = set()
    singles_matches = []
    doubles_matches = []

    if not force_all_doubles:
        singles_pool = [p for p in active_players if p["pref"] == "Singles"]
        singles_pool.sort(key=lambda x: x["level"])
        s_matches, s_leftover = make_singles_matches(singles_pool)
        singles_matches.extend(s_matches)
        for m in s_matches:
            used.add(m[0]["name"])
            used.add(m[1]["name"])
        for p in s_leftover:
            used.add(p["name"])
            on_deck.append(p)

        doubles_pool = [p for p in active_players if p["name"] not in used]
        d_matches, d_leftover = make_doubles_matches(
            doubles_pool, {}, rng=rng,
            avoid_matchups=r1_matchup_keys,
            avoid_partners=r1_partner_pairs,
        )
        doubles_matches.extend(d_matches)
        for m in d_matches:
            for t in m:
                for pl in t:
                    used.add(pl["name"])
        if d_leftover:
            extra_s, extra_bye = make_singles_matches(d_leftover)
            singles_matches.extend(extra_s)
            on_deck.extend(extra_bye)
    else:
        d_matches, d_leftover = make_doubles_matches(
            active_players, {}, rng=rng,
            avoid_matchups=r1_matchup_keys,
            avoid_partners=r1_partner_pairs,
        )
        doubles_matches.extend(d_matches)
        for m in d_matches:
            for t in m:
                for pl in t:
                    used.add(pl["name"])
        on_deck.extend(d_leftover)

    return singles_matches, doubles_matches, on_deck

def format_team(team):
    return " & ".join(p["name"] for p in team)

def render_schedule(singles_matches, doubles_matches, byes, round_num, balance_threshold=0.5):
    courts = []
    court_num = 1

    for m in singles_matches:
        gap = abs(m[0]["level"] - m[1]["level"])
        courts.append({
            "court": court_num,
            "type": "Singles",
            "display": f"{m[0]['name']} vs {m[1]['name']}",
            "levels": f"{m[0]['level']} / {m[1]['level']}",
            "imbalanced": gap > balance_threshold,
            "gap": round(gap, 2),
        })
        court_num += 1

    for t1, t2 in doubles_matches:
        avg1 = round(avg_level(t1), 2)
        avg2 = round(avg_level(t2), 2)
        gap = abs(avg1 - avg2)
        courts.append({
            "court": court_num,
            "type": "Doubles",
            "display": f"{format_team(t1)} vs {format_team(t2)}",
            "levels": f"Team avg {avg1} vs {avg2}",
            "imbalanced": gap > balance_threshold,
            "gap": round(gap, 2),
        })
        court_num += 1

    return courts, byes

def export_text(r1_courts, r1_byes, r2_courts, r2_byes):
    lines = ["=== ROUND 1 ==="]
    for c in r1_courts:
        flag = f" [⚠️ gap {c['gap']}]" if c["imbalanced"] else ""
        lines.append(f"Court {c['court']} [{c['type']}]: {c['display']}{flag}")
    if r1_byes:
        lines.append(f"On Deck: {', '.join(p['name'] for p in r1_byes)}")
    lines.append("")
    lines.append("=== ROUND 2 ===")
    for c in r2_courts:
        flag = f" [⚠️ gap {c['gap']}]" if c["imbalanced"] else ""
        lines.append(f"Court {c['court']} [{c['type']}]: {c['display']}{flag}")
    if r2_byes:
        lines.append(f"On Deck: {', '.join(p['name'] for p in r2_byes)}")
    return "\n".join(lines)

def sheets_url_to_csv(url, sheet_name="Session"):
    """
    Convert any Google Sheets sharing URL to a direct CSV export URL.
    Supports:
      - Standard share URL: .../spreadsheets/d/SHEET_ID/edit?...
      - Already a gviz/tq URL
    Returns the CSV export URL string.
    """
    import re
    # Extract the sheet ID
    match = re.search(r"/spreadsheets/d/([a-zA-Z0-9_-]+)", url)
    if not match:
        raise ValueError("Could not find a Google Sheets ID in the URL. Make sure you're pasting the sharing link.")
    sheet_id = match.group(1)
    return (
        f"https://docs.google.com/spreadsheets/d/{sheet_id}"
        f"/gviz/tq?tqx=out:csv&sheet={requests.utils.quote(sheet_name)}"
    )

def fetch_sheet_as_df(url, sheet_name="Session"):
    """Fetch a Google Sheet tab as a DataFrame. Raises on any error."""
    import csv as csv_module

    csv_url = sheets_url_to_csv(url, sheet_name)
    resp = requests.get(csv_url, timeout=10)
    if resp.status_code == 403:
        raise PermissionError(
            "Sheet returned 403 Forbidden. Make sure sharing is set to 'Anyone with the link can view'."
        )
    resp.raise_for_status()
    raw = resp.text

    # Parse all rows properly using Python's CSV reader (handles quoted commas correctly)
    reader = csv_module.reader(io.StringIO(raw))
    all_rows = list(reader)

    # Find the header row: the one where any cell is exactly "Name"
    # and another cell is "Level" or "USTA Level"
    header_idx = None
    for i, row in enumerate(all_rows):
        cells = [c.strip() for c in row]
        level_cols = ("Level", "USTA Level")
        has_level = any(c in level_cols for c in cells)
        # Name may be its own cell, or appended to the end of a merged title cell
        name_cell_idx = None
        for j, c in enumerate(cells):
            if c == "Name" or c.endswith("Name"):
                name_cell_idx = j
                break
        if name_cell_idx is not None and has_level:
            # If Name is embedded in a longer string, trim the cell to just "Name"
            cells[name_cell_idx] = "Name"
            header_idx = i
            # Replace all_rows with cleaned header + data rows
            all_rows[i] = cells
            break

    if header_idx is None:
        raise ValueError(
            "Could not find a 'Name' and 'Level' header row in the sheet. "
            "Check that the Session tab has these column headers."
        )

    headers = all_rows[header_idx]
    data_rows = all_rows[header_idx + 1:]

    # Build DataFrame directly from parsed rows — no CSV re-parsing needed
    df = pd.DataFrame(data_rows, columns=headers)

    # Drop blank-name rows (empty dropdown slots)
    df = df[df["Name"].notna() & (df["Name"].astype(str).str.strip() != "")]
    df = df.reset_index(drop=True)
    return df

# ─────────────────────────────────────────────
# UI
# ─────────────────────────────────────────────

st.markdown("""
<div class="hero">
    <h1>Tennis Drop-In Scheduler</h1>
    <p>Connect your Google Sheet or upload a CSV → get balanced court assignments in seconds.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    if "seed" not in st.session_state:
        st.session_state.seed = 42
    if "sheet_url" not in st.session_state:
        st.session_state.sheet_url = ""

    max_courts = st.number_input("🎾 Number of courts available", min_value=1, max_value=20, value=10,
        help="Maximum courts in use per round. If players exceed court capacity, all matches become doubles and overflow players are shown as On Deck.")
    balance_threshold = st.slider("⚖️ Balance warning threshold (rating gap)", min_value=0.0, max_value=2.0, value=0.5, step=0.25,
        help="Courts where the level gap exceeds this will show a warning flag. Does not affect scheduling.")
    st.markdown("---")

    st.markdown("### 🔗 Google Sheet")
    sheet_url_input = st.text_input(
        "Paste sharing URL",
        value=st.session_state.sheet_url,
        placeholder="https://docs.google.com/spreadsheets/d/...",
        help="Paste the Google Sheet sharing link. The sheet must be shared as 'Anyone with the link can view'. The app reads the 'Session' tab automatically.",
    )
    if sheet_url_input != st.session_state.sheet_url:
        st.session_state.sheet_url = sheet_url_input

    st.markdown("---")
    st.markdown("### 📋 CSV Fallback")
    st.markdown("""
Columns needed:
- **Name** *(required)*
- **Level** *(e.g. 3.5)*
- **Preference** *(Singles / Doubles / Either)*
- **Partner** *(optional)*
- **Opponent** *(optional, Round 1 only)*
- **Avoid** *(optional)*
    """)

    # Sample CSV download
    sample_data = pd.DataFrame([
        {"Name": "Alice", "Level": 4.0, "Preference": "Doubles", "Partner": "Bob", "Opponent": "", "Avoid": ""},
        {"Name": "Bob", "Level": 3.5, "Preference": "Doubles", "Partner": "Alice", "Opponent": "", "Avoid": ""},
        {"Name": "Carol", "Level": 4.5, "Preference": "Singles", "Partner": "", "Opponent": "Dave", "Avoid": ""},
        {"Name": "Dave", "Level": 4.0, "Preference": "Singles", "Partner": "", "Opponent": "", "Avoid": ""},
        {"Name": "Eve", "Level": 3.0, "Preference": "Either", "Partner": "", "Opponent": "", "Avoid": ""},
        {"Name": "Frank", "Level": 5.0, "Preference": "Doubles", "Partner": "", "Opponent": "", "Avoid": ""},
        {"Name": "Grace", "Level": 4.5, "Preference": "Either", "Partner": "", "Opponent": "", "Avoid": ""},
        {"Name": "Hank", "Level": 3.5, "Preference": "Doubles", "Partner": "", "Opponent": "", "Avoid": ""},
    ])
    csv_bytes = sample_data.to_csv(index=False).encode()
    st.download_button("📥 Download Sample CSV", data=csv_bytes, file_name="sample_players.csv", mime="text/csv")

# ── Data source: Google Sheet takes priority, then CSV upload ──
df = None
source_label = None

if st.session_state.sheet_url:
    try:
        df = fetch_sheet_as_df(st.session_state.sheet_url, sheet_name="Session")
        source_label = "📊 Loaded from Google Sheet"
    except PermissionError as e:
        st.markdown(f'<div class="warning-box">🔒 {e}</div>', unsafe_allow_html=True)
    except ValueError as e:
        st.markdown(f'<div class="warning-box">⚠️ {e}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f'<div class="warning-box">❌ Could not load sheet: {e}</div>', unsafe_allow_html=True)

if df is None:
    uploaded = st.file_uploader("Or upload a CSV file", type=["csv"])
    if uploaded:
        try:
            df = pd.read_csv(uploaded)
            source_label = "📁 Loaded from CSV upload"
        except Exception as e:
            st.markdown(f'<div class="warning-box">❌ Error reading CSV: {e}</div>', unsafe_allow_html=True)
else:
    # Still show uploader collapsed so organizer can override if needed
    with st.expander("Or upload a CSV instead"):
        uploaded_override = st.file_uploader("Upload CSV (overrides Google Sheet)", type=["csv"])
        if uploaded_override:
            try:
                df = pd.read_csv(uploaded_override)
                source_label = "📁 Loaded from CSV upload (override)"
            except Exception as e:
                st.markdown(f'<div class="warning-box">❌ Error reading CSV: {e}</div>', unsafe_allow_html=True)

if df is not None:
    try:
        players = load_players(df)

        if not players:
            st.markdown('<div class="warning-box">⚠️ No valid players found. Check your CSV or Sheet format.</div>', unsafe_allow_html=True)
            st.stop()

        st.markdown(f'<div class="success-box">{source_label} — {len(players)} players found.</div>', unsafe_allow_html=True)

        # Stats bar
        n_singles = sum(1 for p in players if p["pref"] == "Singles")
        n_doubles = sum(1 for p in players if p["pref"] == "Doubles")
        n_either = sum(1 for p in players if p["pref"] == "Either")
        n_fp = sum(1 for p in players if p["partner"])
        n_fo = sum(1 for p in players if p["opponent"])

        st.markdown(f"""
        <div>
            <span class="stat-pill">Players: <span>{len(players)}</span></span>
            <span class="stat-pill">Singles-only: <span>{n_singles}</span></span>
            <span class="stat-pill">Doubles-only: <span>{n_doubles}</span></span>
            <span class="stat-pill">Either: <span>{n_either}</span></span>
            <span class="stat-pill">Fixed partners: <span>{n_fp}</span></span>
            <span class="stat-pill">Fixed opponents: <span>{n_fo}</span></span>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("👥 View Player Roster"):
            display_df = pd.DataFrame(players)[["name","level","pref","partner","opponent"]]
            display_df.columns = ["Name","Level","Preference","Fixed Partner","Fixed Opponent"]
            st.dataframe(display_df, use_container_width=True, hide_index=True)

        st.markdown("---")

        col_btn, col_info = st.columns([2, 3])
        with col_btn:
            generate = st.button("🎾 Generate Matchups")
        with col_info:
            if st.session_state.seed > 42:
                st.caption(f"Click again to try a different arrangement. (seed {st.session_state.seed})")

        if generate:
            seed = st.session_state.seed
            st.session_state.seed += 1
            rng = random.Random(seed)

            # Round 1 — optimal matching; rng used only for tie-breaking
            r1_singles, r1_doubles, r1_on_deck, r1_matchup_keys, r1_partner_pairs = assign_round1(players, rng=rng, max_courts=max_courts)
            r1_courts, _ = render_schedule(r1_singles, r1_doubles, [], 1, balance_threshold)

            # Round 2 — reshuffled, avoids repeating R1 opponents and partners where possible
            r2_singles, r2_doubles, r2_on_deck = assign_round2(players, rng, r1_matchup_keys, r1_partner_pairs, max_courts=max_courts)
            r2_courts, _ = render_schedule(r2_singles, r2_doubles, [], 2, balance_threshold)

            # Verify all players appear (on court or on deck)
            r1_names = set()
            for c in r1_courts:
                for nm in c["display"].replace(" vs ", " & ").split(" & "):
                    r1_names.add(nm.strip())
            r1_names.update(p["name"] for p in r1_on_deck)

            r2_names = set()
            for c in r2_courts:
                for nm in c["display"].replace(" vs ", " & ").split(" & "):
                    r2_names.add(nm.strip())
            r2_names.update(p["name"] for p in r2_on_deck)

            all_names = set(p["name"] for p in players)
            r1_missing = all_names - r1_names
            r2_missing = all_names - r2_names

            if r1_missing or r2_missing:
                st.markdown(f'<div class="warning-box">⚠️ Player integrity check failed. Missing in R1: {r1_missing}. Missing in R2: {r2_missing}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="success-box">✅ All {len(players)} players accounted for in both rounds.</div>', unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown('<div class="round-header">Round 1</div>', unsafe_allow_html=True)
                for c in r1_courts:
                    badge_class = "badge-singles" if c["type"] == "Singles" else "badge-doubles"
                    imbalance_html = f'<span class="imbalance-flag">⚠️ gap {c["gap"]}</span>' if c["imbalanced"] else ""
                    card_class = "court-card imbalanced" if c["imbalanced"] else "court-card"
                    st.markdown(
                        f'<div class="{card_class}">'
                        f'<div class="court-label">Court {c["court"]}</div>'
                        f'<div class="match-text">{c["display"]}'
                        f'<span class="match-type-badge {badge_class}">{c["type"]}</span>'
                        f'{imbalance_html}</div>'
                        f'<div style="font-size:0.82rem;color:#c9d1d9;margin-top:4px;">{c["levels"]}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                if r1_on_deck:
                    st.markdown(f'<div class="bye-card">⏸ On Deck: {", ".join(p["name"] for p in r1_on_deck)}</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="round-header">Round 2</div>', unsafe_allow_html=True)
                for c in r2_courts:
                    badge_class = "badge-singles" if c["type"] == "Singles" else "badge-doubles"
                    imbalance_html = f'<span class="imbalance-flag">⚠️ gap {c["gap"]}</span>' if c["imbalanced"] else ""
                    card_class = "court-card imbalanced" if c["imbalanced"] else "court-card"
                    st.markdown(
                        f'<div class="{card_class}">'
                        f'<div class="court-label">Court {c["court"]}</div>'
                        f'<div class="match-text">{c["display"]}'
                        f'<span class="match-type-badge {badge_class}">{c["type"]}</span>'
                        f'{imbalance_html}</div>'
                        f'<div style="font-size:0.82rem;color:#c9d1d9;margin-top:4px;">{c["levels"]}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                if r2_on_deck:
                    st.markdown(f'<div class="bye-card">⏸ On Deck: {", ".join(p["name"] for p in r2_on_deck)}</div>', unsafe_allow_html=True)

            st.markdown("---")

            # Export
            export_str = export_text(r1_courts, r1_on_deck, r2_courts, r2_on_deck)
            st.download_button(
                "📄 Export Schedule as .txt",
                data=export_str.encode(),
                file_name="tennis_schedule.txt",
                mime="text/plain",
            )

    except Exception as e:
        st.markdown(f'<div class="warning-box">❌ Error processing player data: {e}</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align:center; padding: 3rem; color: #8b949e;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🎾</div>
        <div style="font-family: 'Bebas Neue', sans-serif; font-size: 1.5rem; letter-spacing: 2px; color: #4ade80;">Ready when you are</div>
        <div style="font-size: 0.9rem; margin-top: 0.5rem; color: #c9d1d9;">Paste a Google Sheet URL in the sidebar, or upload a CSV file below.</div>
    </div>
    """, unsafe_allow_html=True)
