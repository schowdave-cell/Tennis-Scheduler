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
    initial_sidebar_state="expanded",
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
    white-space: nowrap;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* Hide sidebar collapse/expand button — try all known selectors */
[data-testid="collapsedControl"],
[data-testid="baseButton-headerNoPadding"],
[data-testid="stSidebarCollapseButton"],
button[kind="header"],
section[data-testid="stSidebar"] > div > button:first-child,
.st-emotion-cache-h4xjwg,
.st-emotion-cache-1rtdyuf,
.st-emotion-cache-1egp75f {
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
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

/* Fix +/- buttons on number input */
[data-testid="stNumberInput"] button {
    color: #e6edf3 !important;
    background-color: #30363d !important;
    border: 1px solid #444d56 !important;
}

[data-testid="stNumberInput"] button:hover {
    background-color: #444d56 !important;
    color: #4ade80 !important;
}

[data-testid="stNumberInput"] button svg {
    fill: #e6edf3 !important;
    stroke: #e6edf3 !important;
}

/* Fix all form element text in sidebar */
[data-testid="stSidebar"] input {
    color: #e6edf3 !important;
    background-color: #21262d !important;
}

/* Fix expander — prevent white background, fix text color */
[data-testid="stExpander"] {
    background-color: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
}

[data-testid="stExpander"] summary {
    background-color: #161b22 !important;
    color: #e6edf3 !important;
}

[data-testid="stExpander"] summary:hover {
    background-color: #21262d !important;
}

[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span,
[data-testid="stExpander"] p {
    color: #e6edf3 !important;
}

/* Fix file uploader */
[data-testid="stFileUploader"] {
    background-color: #161b22 !important;
    border: 2px dashed #30363d !important;
    border-radius: 12px !important;
}

[data-testid="stFileUploader"] * {
    color: #e6edf3 !important;
}

[data-testid="stFileUploader"] button {
    background-color: #21262d !important;
    color: #e6edf3 !important;
    border: 1px solid #30363d !important;
}

[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span {
    color: #8b949e !important;
}

[data-testid="stFileUploaderDropzone"] {
    background-color: #161b22 !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] {
    color: #c9d1d9 !important;
}


.stDataFrame {
    background: #161b22 !important;
}

/* ── Selectbox / dropdown fixes ── */
[data-testid="stSelectbox"] > div > div {
    background-color: #21262d !important;
    border: 1px solid #4ade8055 !important;
    border-radius: 6px !important;
}

/* Force all text inside selectbox to be clearly visible white */
[data-testid="stSelectbox"] *,
[data-testid="stSelectbox"] div,
[data-testid="stSelectbox"] span,
[data-testid="stSelectbox"] p,
[data-testid="stSelectbox"] input {
    color: #e6edf3 !important;
}

/* Dropdown popup menu */
[data-baseweb="popover"],
[data-baseweb="popover"] *,
[data-baseweb="menu"],
[data-baseweb="menu"] * {
    background-color: #1c2330 !important;
    color: #e6edf3 !important;
}

[data-baseweb="popover"] {
    border: 1px solid #30363d !important;
}

[data-baseweb="option"] {
    background-color: #1c2330 !important;
    color: #e6edf3 !important;
}

[data-baseweb="option"]:hover,
[data-baseweb="option"][aria-selected="true"] {
    background-color: #2d4a3e !important;
    color: #4ade80 !important;
}

/* Load button alignment fix */
.stButton > button,
.stButton > button > div,
.stButton > button p {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    margin: 0 !important;
    line-height: 1 !important;
    width: 100% !important;
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
            return str(row[c])
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

        # Filter out legend/instruction rows — only reject names with emoji or > 50 chars
        raw_level = row[level_col] if level_col and level_col in row.index else ""
        level = parse_level(raw_level)

        if len(name) > 50 or any(ord(c) > 127 for c in name):
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

def form_teams(pool, rng=None, r1_rng=None, avoid_partners=None):
    """
    Phase 1: Form teams of 2 from the pool.
    - Fixed partner pairs become teams immediately (always, both rounds).
    - Free players are paired by closest level (Round 1) or shuffled (Round 2).
    - r1_rng: used in Round 1 to shuffle free players before level-sort pairing,
      so the leftover player rotates on each click rather than always being the same.
    - avoid_partners: set of frozensets {name_a, name_b} to avoid re-pairing in Round 2.
    Returns list of teams (each a list of 2 players) and leftover players (0 or 1).
    """
    avoid_partners = avoid_partners or set()
    remaining = list(pool)
    used = set()
    teams = []

    # Lock fixed partner pairs first
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
        # Round 1: sort by level for best pairing, but shuffle same-level players
        # using r1_rng so the leftover rotates each click
        if r1_rng:
            r1_rng.shuffle(free)
        free.sort(key=lambda x: x["level"])

    unpaired = list(free)

    if len(unpaired) % 2 == 1 and not rng:
        # Round 1 with odd free players: try each player as the sit-out and pick
        # the arrangement that produces the best overall level balance.
        # This prevents the same isolated-level player from always sitting out.
        best_teams = None
        best_score = float("inf")
        best_leftover = None

        for sit_out_idx in range(len(unpaired)):
            candidate_leftover = unpaired[sit_out_idx]
            candidate_pool = unpaired[:sit_out_idx] + unpaired[sit_out_idx+1:]
            candidate_teams = []
            pool_sorted = sorted(candidate_pool, key=lambda x: x["level"])
            i = 0
            while i + 1 < len(pool_sorted):
                candidate_teams.append([pool_sorted[i], pool_sorted[i+1]])
                i += 2
            # Score = total intra-team level gap
            score = sum(abs(t[0]["level"] - t[1]["level"]) for t in candidate_teams)
            if score < best_score:
                best_score = score
                best_teams = candidate_teams
                best_leftover = [candidate_leftover]

        # Among equally-scored options, r1_rng picks randomly
        if r1_rng:
            best_options = []
            for sit_out_idx in range(len(unpaired)):
                candidate_leftover = unpaired[sit_out_idx]
                candidate_pool = unpaired[:sit_out_idx] + unpaired[sit_out_idx+1:]
                pool_sorted = sorted(candidate_pool, key=lambda x: x["level"])
                score = sum(abs(pool_sorted[i]["level"] - pool_sorted[i+1]["level"])
                           for i in range(0, len(pool_sorted)-1, 2))
                if abs(score - best_score) < 0.001:
                    best_options.append(sit_out_idx)
            sit_out_idx = r1_rng.choice(best_options)
            best_leftover = [unpaired[sit_out_idx]]
            candidate_pool = unpaired[:sit_out_idx] + unpaired[sit_out_idx+1:]
            pool_sorted = sorted(candidate_pool, key=lambda x: x["level"])
            best_teams = []
            i = 0
            while i + 1 < len(pool_sorted):
                best_teams.append([pool_sorted[i], pool_sorted[i+1]])
                i += 2

        teams.extend(best_teams)
        leftover = best_leftover
    else:
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
        leftover = unpaired
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
        if rng:
            # Pick randomly among the middle third of teams by level to keep balance
            # while still rotating who sits out
            remaining_sorted = sorted(remaining, key=lambda t: avg_level(t))
            n = len(remaining_sorted)
            lo, hi = max(0, n//3), min(n-1, 2*n//3)
            sit_out_idx = rng.randint(lo, hi)
            sit_out = remaining_sorted[sit_out_idx]
            remaining = [t for t in remaining if t is not sit_out]
            leftover_teams = [sit_out]
        else:
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


def optimize_court_balance(matches):
    """
    Post-matching optimization: for each court, try all single-player swaps
    between the two teams and keep the swap if it reduces the team avg gap.
    Respects fixed partners — never splits a fixed pair.
    """
    optimized = []
    for t1, t2 in matches:
        best_t1, best_t2 = t1, t2
        best_gap = abs(avg_level(t1) - avg_level(t2))

        # Try swapping each player in t1 with each player in t2
        for i, p1 in enumerate(t1):
            for j, p2 in enumerate(t2):
                # Don't swap fixed partners apart
                if p1.get("partner") or p2.get("partner"):
                    continue
                new_t1 = [p if k != i else p2 for k, p in enumerate(t1)]
                new_t2 = [p if k != j else p1 for k, p in enumerate(t2)]
                gap = abs(avg_level(new_t1) - avg_level(new_t2))
                if gap < best_gap - 0.001:  # small epsilon to avoid floating point churn
                    best_gap = gap
                    best_t1, best_t2 = new_t1, new_t2

        optimized.append((best_t1, best_t2))
    return optimized


def make_doubles_matches(pool, fixed_partners, rng=None, r1_rng=None, avoid_matchups=None, avoid_partners=None):
    """
    Form doubles matches from pool using two-phase approach:
      Phase 1 — form_teams: lock fixed pairs, pair free players by level (avoid R1 partners)
      Phase 2 — match teams: optimal (R1) or greedy (R2) to minimize cross-team gap
      Phase 3 — optimize_court_balance: single-player swaps to further improve balance
    Scales efficiently to 25+ players.
    """
    avoid_matchups = avoid_matchups or set()

    teams, leftover_players = form_teams(pool, rng=rng, r1_rng=r1_rng, avoid_partners=avoid_partners)

    if rng is None:
        matches, leftover_teams = optimal_match_teams(teams, rng=r1_rng)
    else:
        matches, leftover_teams = greedy_match_teams(teams, avoid_matchups=avoid_matchups)

    # Phase 3: fine-tune balance by trying single-player swaps within each court
    matches = optimize_court_balance(matches)

    leftover = [p for team in leftover_teams for p in team] + leftover_players
    return matches, leftover

def make_singles_matches(pool, avoid_keys=None):
    """Form singles matches from pool. Returns matches and leftover.
    avoid_keys: set of frozensets of player name pairs to avoid repeating.
    """
    avoid_keys = avoid_keys or set()
    sorted_pool = sorted(pool, key=lambda x: x["level"])
    matches = []
    remaining = list(sorted_pool)

    # If we have avoid constraints, try to shuffle to dodge repeats
    if avoid_keys and len(remaining) >= 2:
        # Try adjacent pairings first, then swap neighbors to break repeats
        used = [False] * len(remaining)
        result = []
        for i in range(len(remaining)):
            if used[i]:
                continue
            # Try pairing with next unused, skip if repeat and a better option exists
            for j in range(i + 1, len(remaining)):
                if used[j]:
                    continue
                pair_key = frozenset([remaining[i]["name"], remaining[j]["name"]])
                is_repeat = pair_key in avoid_keys
                # Accept non-repeat immediately, or accept repeat if no other choice
                next_unused = [k for k in range(i + 1, len(remaining)) if not used[k] and k != j]
                if not is_repeat or not next_unused:
                    result.append((remaining[i], remaining[j]))
                    used[i] = True
                    used[j] = True
                    break
        leftover = [remaining[i] for i in range(len(remaining)) if not used[i]]
        return result, leftover

    # No avoid constraints — simple sequential pairing
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

        singles_pool = [p for p in active_players if p["pref"] == "Singles" and p["name"] not in used and not p["partner"]]
        s_matches, s_leftover = make_singles_matches(singles_pool)
        singles_matches.extend(s_matches)
        for m in s_matches:
            used.add(m[0]["name"])
            used.add(m[1]["name"])
        # Don't put singles leftovers on deck yet — hold for pairing with doubles leftovers

        doubles_pool = [p for p in active_players if p["name"] not in used and p not in s_leftover]
        d_matches, d_leftover = make_doubles_matches(doubles_pool, {}, rng=None, r1_rng=rng)
        doubles_matches.extend(d_matches)
        for m in d_matches:
            for t in m:
                for pl in t:
                    used.add(pl["name"])

        # Combine all leftovers and try singles before on_deck
        all_leftover = s_leftover + d_leftover
        if all_leftover:
            # Players with a fixed partner must never play singles — send them on deck
            singles_eligible = [p for p in all_leftover if not p["partner"]]
            forced_deck = [p for p in all_leftover if p["partner"]]
            extra_s, extra_bye = make_singles_matches(singles_eligible)
            singles_matches.extend(extra_s)
            for m in extra_s:
                used.add(m[0]["name"])
                used.add(m[1]["name"])
            on_deck.extend(extra_bye + forced_deck)
    else:
        # Court-constrained: all doubles, no singles
        d_matches, d_leftover = make_doubles_matches(active_players, {}, rng=None, r1_rng=rng)
        doubles_matches.extend(d_matches)
        for m in d_matches:
            for t in m:
                for pl in t:
                    used.add(pl["name"])
        if d_leftover:
            # Even in court-constrained mode, 2 leftovers can play singles
            extra_s, extra_bye = make_singles_matches(d_leftover)
            singles_matches.extend(extra_s)
            on_deck.extend(extra_bye)

    r1_matchup_keys = {match_key(t1, t2) for t1, t2 in doubles_matches}
    r1_partner_pairs = set()
    for t1, t2 in doubles_matches:
        for team in (t1, t2):
            if not any(p["partner"] for p in team):
                r1_partner_pairs.add(frozenset(p["name"] for p in team))

    # Track singles matchups to detect repeats in Round 2
    r1_singles_keys = {frozenset([m[0]["name"], m[1]["name"]]) for m in singles_matches}

    return singles_matches, doubles_matches, on_deck, r1_matchup_keys, r1_partner_pairs, r1_singles_keys


def plan_r2_singles(singles_players, either_pool, r1_singles_keys, balance_threshold, max_courts, current_doubles_courts, non_singles_count=None, rng=None):
    """
    Decide how to handle singles in Round 2 to avoid R1 repeat matchups.

    Rules:
    - If all R1 singles pairings can be swapped within the singles group
      such that every new pairing is within balance_threshold, do the swap.
    - If no valid swap exists among the singles group (levels too spread),
      keep the same R1 pairings (repeat is unavoidable).
    - If there are exactly 2 singles players (swap impossible), pull Either
      players out of doubles to give each singles player a new opponent.
      Pull 2 if the remaining doubles pool is divisible by 4, otherwise pull 4.
      Only do this if enough courts are available. Otherwise keep same pairing.

    Returns: list of (p1, p2) singles matches, list of Either players pulled out
    """
    n = len(singles_players)
    if n == 0:
        return [], []

    # --- 4+ singles players: try to swap within the group ---
    if n >= 4:
        # Build R1 pairs
        r1_pairs = []
        used = set()
        for i, p1 in enumerate(singles_players):
            if p1["name"] in used:
                continue
            for p2 in singles_players[i+1:]:
                if p2["name"] in used:
                    continue
                if frozenset([p1["name"], p2["name"]]) in r1_singles_keys:
                    r1_pairs.append((p1, p2))
                    used.add(p1["name"])
                    used.add(p2["name"])
                    break

        # Try to find a rotation of pairs where all gaps <= threshold
        # Simple approach: try all permutations of the "right-hand" players
        left = [pair[0] for pair in r1_pairs]
        right = [pair[1] for pair in r1_pairs]

        from itertools import permutations
        best_swap = None
        for perm in permutations(right):
            # No pair can be the same as R1
            if any(frozenset([left[i]["name"], perm[i]["name"]]) in r1_singles_keys
                   for i in range(len(left))):
                continue
            # All gaps must be within threshold
            if all(abs(left[i]["level"] - perm[i]["level"]) <= balance_threshold
                   for i in range(len(left))):
                best_swap = list(zip(left, perm))
                break

        if best_swap:
            return best_swap, []
        else:
            # No valid swap — repeat the same pairings
            return list(r1_singles_keys and [(p1, p2) for p1, p2 in
                        [(s, next((q for q in singles_players if frozenset([s["name"], q["name"]]) in r1_singles_keys), None))
                         for s in left] if p2] or r1_pairs), []

    # --- Exactly 2 singles players ---
    if n == 2:
        p1, p2 = singles_players
        would_repeat = frozenset([p1["name"], p2["name"]]) in r1_singles_keys

        if not would_repeat:
            return [(p1, p2)], []

        # non_singles_count is the number of non-singles players (the raw doubles pool).
        # After pulling 2 Either players into singles, the remaining doubles pool is
        # non_singles_count - 2. If that's divisible by 4, pull 2. Otherwise pull 4.
        pool_size = non_singles_count if non_singles_count is not None else current_doubles_courts * 4
        rem2 = (pool_size - 2) % 4
        rem4 = (pool_size - 4) % 4
        # Pick whichever pull leaves fewer players on deck (smaller remainder)
        # Prefer pull-2 on a tie since it keeps more players in doubles
        need_pull = 2 if rem2 <= rem4 else 4

        enough_courts = (max_courts is None) or (current_doubles_courts >= 2)
        if len(either_pool) < need_pull or not enough_courts:
            return [(p1, p2)], []

        available = list(either_pool)
        if rng:
            rng.shuffle(available)

        # Always pick the closest-level Either player for p1, then for p2
        available.sort(key=lambda e: abs(e["level"] - p1["level"]))
        either_a = available.pop(0)

        available.sort(key=lambda e: abs(e["level"] - p2["level"]))
        either_b = available.pop(0)

        new_singles = [(p1, either_a), (p2, either_b)]
        pulled = [either_a, either_b]

        # If we need 4, pull the closest-level pair from what remains
        if need_pull == 4:
            if len(available) < 2:
                return [(p1, p2)], []
            best_pair = None
            best_gap = float("inf")
            for i in range(len(available)):
                for j in range(i + 1, len(available)):
                    gap = abs(available[i]["level"] - available[j]["level"])
                    if gap < best_gap:
                        best_gap = gap
                        best_pair = (available[i], available[j])
            if best_pair is None:
                return [(p1, p2)], []
            either_c, either_d = best_pair
            new_singles.append((either_c, either_d))
            pulled.extend([either_c, either_d])

        return new_singles, pulled

    # --- Odd number (1 or 3): just match what we can, leftover handled by caller ---
    sorted_s = sorted(singles_players, key=lambda x: x["level"])
    matches = []
    for i in range(0, len(sorted_s) - 1, 2):
        matches.append((sorted_s[i], sorted_s[i+1]))
    return matches, []


def assign_round2(players, rng, r1_matchup_keys=None, r1_partner_pairs=None,
                  r1_singles_keys=None, max_courts=None, balance_threshold=0.5):
    """
    Round 2: reshuffle avoiding R1 repeat matchups.
    Singles repeat-avoidance:
      - 4+ singles players: try to swap within the group (within balance_threshold).
        If no valid swap, repeat same pairings.
      - 2 singles players: pull 4 Either players out of doubles to make 3 singles courts,
        but only if enough courts are available. Otherwise repeat same pairing.
    """
    n = len(players)
    force_all_doubles = False
    on_deck = []
    active_players = list(players)

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
        singles_pool = [p for p in active_players if p["pref"] == "Singles" and not p["partner"]]
        either_pool = [p for p in active_players
                       if p["pref"] in ("Either", "Doubles") and not p["partner"]]

        # How many non-singles players exist (the doubles pool before any pulling)
        # Players with a fixed partner always play doubles even if pref=Singles
        non_singles = [p for p in active_players if p["pref"] != "Singles" or p["partner"]]
        current_doubles_courts = len(non_singles) // 4
        non_singles_count = len(non_singles)

        r2_singles, pulled_either = plan_r2_singles(
            singles_pool, either_pool, r1_singles_keys or set(),
            balance_threshold, max_courts, current_doubles_courts, non_singles_count, rng=rng
        )

        singles_matches.extend(r2_singles)
        for m in r2_singles:
            used.add(m[0]["name"])
            used.add(m[1]["name"])

        # Singles leftovers (odd singles player)
        s_leftover = [p for p in singles_pool if p["name"] not in used]

        # Remaining doubles pool excludes singles players and pulled Either players
        pulled_names = {p["name"] for p in pulled_either}
        doubles_pool = [p for p in active_players
                        if p["name"] not in used
                        and p["name"] not in pulled_names
                        and p not in s_leftover]

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

        all_leftover = s_leftover + d_leftover
        if all_leftover:
            rng.shuffle(all_leftover)
            singles_eligible = [p for p in all_leftover if not p["partner"]]
            forced_deck = [p for p in all_leftover if p["partner"]]
            extra_s, extra_bye = make_singles_matches(singles_eligible, avoid_keys=r1_singles_keys or set())
            singles_matches.extend(extra_s)
            for m in extra_s:
                used.add(m[0]["name"])
                used.add(m[1]["name"])
            on_deck.extend(extra_bye + forced_deck)
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
        if d_leftover:
            extra_s, extra_bye = make_singles_matches(d_leftover)
            singles_matches.extend(extra_s)
            on_deck.extend(extra_bye)

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

@st.cache_data(show_spinner=False)
def load_master_players_cached(url):
    """Fetch and parse Master Players from Google Sheet. Cached by URL so reruns don't re-fetch."""
    df = fetch_sheet_as_df(url, sheet_name="Master Players")
    level_col = find_level_column(df)
    players = []
    if level_col and "Name" in df.columns:
        for _, row in df.iterrows():
            n = clean_str(str(row.get("Name", "")))
            if not n or len(n) > 50 or any(ord(c) > 127 for c in n):
                continue
            players.append({
                "name": n,
                "level": parse_level(str(row[level_col])),
                "pref": clean_str(find_col(row, "Default Preference", "Preference")).capitalize() or "Either",
                "partner": clean_str(find_col(row, "Default Partner", "Partner")),
                "opponent": "",
                "avoid": "",
            })
    players.sort(key=lambda p: p["name"].lower())
    return players


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
        # Only require "Name" — Level may not exist in Session tab anymore
        name_cell_idx = None
        for j, c in enumerate(cells):
            if c == "Name" or (c.endswith("Name") and len(c) > 4):
                name_cell_idx = j
                break
        if name_cell_idx is not None:
            # If Name is embedded in a longer string, trim to just "Name"
            if cells[name_cell_idx] != "Name":
                cells[name_cell_idx] = "Name"
            header_idx = i
            all_rows[i] = cells
            break

    if header_idx is None:
        raise ValueError(
            "Could not find a 'Name' header row in the sheet. "
            "Check that the Session tab has a 'Name' column header."
        )

    headers = all_rows[header_idx]
    data_rows = all_rows[header_idx + 1:]

    # Build DataFrame — all values come from csv.reader as strings already
    df = pd.DataFrame(data_rows, columns=headers)
    # Ensure all columns are string type to prevent type inference issues
    for col in df.columns:
        df[col] = df[col].astype(str)

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
    <p>Connect your Google Sheet → get balanced court assignments in seconds.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    if "seed" not in st.session_state:
        st.session_state.seed = 42
    if "sheet_url" not in st.session_state:
        st.session_state.sheet_url = ""
    if "schedule" not in st.session_state:
        st.session_state.schedule = None

    max_courts = st.number_input("🎾 Number of courts available", min_value=1, max_value=20, value=10, step=1, format="%d")
    st.caption("Maximum courts per round. If players exceed capacity, all matches become doubles and overflow players are shown as On Deck.")
    balance_threshold = st.slider("⚖️ Balance warning threshold (rating gap)", min_value=0.0, max_value=2.0, value=0.5, step=0.25,
        help="Courts where the level gap exceeds this will show a warning flag. Does not affect scheduling.")

# ── Unified data source section ──
st.markdown("### 📡 Connect Your Player Data")

st.markdown("**🔗 Google Sheet URL**")
st.caption("Paste your sharing link — the app reads the Master Players tab automatically. Sheet must be shared as 'Anyone with the link can view'.")
url_col, btn_col = st.columns([6, 1])
with url_col:
    sheet_url_input = st.text_input(
        "Google Sheet URL",
        value=st.session_state.sheet_url,
        placeholder="https://docs.google.com/spreadsheets/d/...",
        label_visibility="collapsed",
    )
with btn_col:
    load_clicked = st.button("Load", use_container_width=True)

if load_clicked and sheet_url_input:
    st.session_state.sheet_url = sheet_url_input
elif sheet_url_input != st.session_state.sheet_url:
    st.session_state.sheet_url = sheet_url_input

st.markdown("""
<div style="font-size:0.82rem; color:#8b949e; margin-top:0.5rem; line-height:1.6;">
Your sheet needs one tab:<br>
<b style="color:#c9d1d9;">Master Players</b> — Name, Level, Default Preference, Default Partner<br>
Player attendance and per-session overrides are managed in the app below.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Load master players ──
master_players = []
source_label = None
uploaded_csv = None

if st.session_state.sheet_url:
    try:
        master_players = load_master_players_cached(st.session_state.sheet_url)
        source_label = f"📊 {len(master_players)} players loaded from Google Sheet"
    except Exception as e:
        st.markdown(f'<div class="warning-box">❌ Could not load Master Players tab: {e}</div>', unsafe_allow_html=True)

# ── Session manager ──
if master_players:
    st.markdown(f'<div class="success-box" id="players-loaded">{source_label}</div>', unsafe_allow_html=True)

    # Init session state
    if "overrides" not in st.session_state:
        st.session_state.overrides = {}
    if "guests" not in st.session_state:
        st.session_state.guests = []
    # Ensure a widget-key entry exists for every player (default unchecked)
    for _p in master_players:
        if f"chk_{_p['name']}" not in st.session_state:
            st.session_state[f"chk_{_p['name']}"] = False

    st.markdown("### 👥 Who's Playing Today?")

    ctrl1, ctrl2 = st.columns([2, 2])
    with ctrl1:
        if st.button("☑️ Select All"):
            for _p in master_players:
                st.session_state[f"chk_{_p['name']}"] = True
            st.rerun()
    with ctrl2:
        if st.button("🗑️ Clear All"):
            for _p in master_players:
                st.session_state[f"chk_{_p['name']}"] = False
            st.session_state.overrides = {}
            st.session_state.guests = []
            st.rerun()

    st.markdown("")

    # all_names: everyone available as a partner/opponent — all master players + guests, sorted
    all_names = sorted(
        [p["name"] for p in master_players] +
        [g["name"] for g in st.session_state.guests]
    )

    # Table header — marked with a unique sentinel div so JS can find and stick it
    st.markdown("<div id='player-table-header-sentinel'></div>", unsafe_allow_html=True)
    h0, h1, h2, h3, h4, h5 = st.columns([0.5, 2, 1, 1.5, 1.5, 1.5])
    h0.markdown("<div style='font-size:0.78rem;color:#4ade80;font-weight:600;'>IN</div>", unsafe_allow_html=True)
    h1.markdown("<div style='font-size:0.78rem;color:#4ade80;font-weight:600;'>NAME</div>", unsafe_allow_html=True)
    h2.markdown("<div style='font-size:0.78rem;color:#4ade80;font-weight:600;'>LEVEL</div>", unsafe_allow_html=True)
    h3.markdown("<div style='font-size:0.78rem;color:#4ade80;font-weight:600;'>PREFERENCE</div>", unsafe_allow_html=True)
    h4.markdown("<div style='font-size:0.78rem;color:#4ade80;font-weight:600;'>PARTNER PREFERENCE</div>", unsafe_allow_html=True)
    h5.markdown("<div style='font-size:0.78rem;color:#4ade80;font-weight:600;'>OPPONENT PREFERENCE (R1)</div>", unsafe_allow_html=True)
    st.markdown("""
    <style>
    /* Sticky player table header */
    #player-table-header-sentinel ~ div [data-testid="stHorizontalBlock"]:first-of-type {
        position: sticky;
        top: 2.75rem;
        z-index: 99;
        background: #0d1117;
        padding-bottom: 6px;
        border-bottom: 1px solid #30363d;
    }
    </style>
    <hr style='margin:4px 0 8px 0;border-color:#30363d;'>
    """, unsafe_allow_html=True)

    for row_idx, p in enumerate(master_players):
        # Alternating row background
        row_bg = "#161b22" if row_idx % 2 == 0 else "#1c2330"
        st.markdown(
            f"<div style='background:{row_bg};border-radius:6px;margin:1px 0;padding:2px 6px;'>",
            unsafe_allow_html=True,
        )
        c0, c1, c2, c3, c4, c5 = st.columns([0.5, 2, 1, 1.5, 1.5, 1.5])

        # Seed override dict from player defaults the first time we see this player
        if p["name"] not in st.session_state.overrides:
            st.session_state.overrides[p["name"]] = {
                "pref": p["pref"] if p["pref"] else "",
                "partner": p["partner"] if p["partner"] else "",
                "opponent": "",
            }
        ov = st.session_state.overrides[p["name"]]

        with c0:
            st.checkbox("", key=f"chk_{p['name']}", label_visibility="collapsed")

        with c1:
            st.markdown(f"<div style='padding-top:0.4rem;color:#e6edf3;font-weight:500;'>{p['name']}</div>", unsafe_allow_html=True)

        with c2:
            st.markdown(f"<div style='padding-top:0.4rem;color:#c9d1d9;'>{p['level']}</div>", unsafe_allow_html=True)

        with c3:
            pref_opts = ["", "Singles", "Doubles", "Either"]
            cur_pref = ov.get("pref", "") or ""
            new_pref = st.selectbox("", pref_opts,
                index=pref_opts.index(cur_pref) if cur_pref in pref_opts else 0,
                key=f"pref_{p['name']}", label_visibility="collapsed",
            )
            ov["pref"] = new_pref

        with c4:
            show_partner = new_pref == "Doubles"
            if show_partner:
                partner_opts = [""] + [n for n in all_names if n != p["name"]]
                cur_partner = ov.get("partner", p["partner"]) or p["partner"]
                partner_idx = partner_opts.index(cur_partner) if cur_partner in partner_opts else 0
                new_partner = st.selectbox("", partner_opts,
                    index=partner_idx,
                    key=f"partner_{p['name']}", label_visibility="collapsed",
                )
            else:
                new_partner = ""
                st.markdown("<div style='padding-top:0.4rem;color:#4a5568;font-size:0.8rem;'>—</div>", unsafe_allow_html=True)
            ov["partner"] = new_partner

        with c5:
            show_opponent = new_pref == "Singles"
            if show_opponent:
                opp_opts = [""] + [n for n in all_names if n != p["name"]]
                cur_opp = ov.get("opponent", "") or ""
                opp_idx = opp_opts.index(cur_opp) if cur_opp in opp_opts else 0
                new_opp = st.selectbox("", opp_opts,
                    index=opp_idx,
                    key=f"opp_{p['name']}", label_visibility="collapsed",
                )
            else:
                new_opp = ""
                st.markdown("<div style='padding-top:0.4rem;color:#4a5568;font-size:0.8rem;'>—</div>", unsafe_allow_html=True)
            ov["opponent"] = new_opp
            ov["opponent"] = new_opp

        st.session_state.overrides[p["name"]] = ov
        st.markdown("</div>", unsafe_allow_html=True)

    # Guest players
    st.markdown("---")
    st.markdown("### ➕ Add Guest Player")

    # Guest partner/opponent dropdowns use all_names (all master players + guests)
    guest_name_opts = [""] + all_names

    if "guest_add_counter" not in st.session_state:
        st.session_state.guest_add_counter = 0
    _gc = st.session_state.guest_add_counter

    g1, g2, g3, g4 = st.columns([2.5, 1.8, 1.8, 1.2])
    with g1:
        st.markdown("<div style='padding-bottom:4px;font-size:0.78rem;color:#4ade80;font-weight:600;'>NAME</div>", unsafe_allow_html=True)
        guest_name = st.text_input("Name", key=f"guest_name_{_gc}", placeholder="First Last", label_visibility="collapsed")
    with g2:
        st.markdown("<div style='padding-bottom:4px;font-size:0.78rem;color:#4ade80;font-weight:600;'>LEVEL</div>", unsafe_allow_html=True)
        guest_level = st.number_input("Level", min_value=1.0, max_value=7.0, value=3.5, step=0.5, key=f"guest_level_{_gc}", label_visibility="collapsed", format="%.1f")
    with g3:
        st.markdown("<div style='padding-bottom:4px;font-size:0.78rem;color:#4ade80;font-weight:600;'>PREFERENCE</div>", unsafe_allow_html=True)
        guest_pref = st.selectbox("Preference", ["Either", "Singles", "Doubles"], key=f"guest_pref_{_gc}", label_visibility="collapsed")
    with g4:
        st.markdown("<div style='padding-bottom:4px;font-size:0.78rem;color:#4ade80;font-weight:600;'>&nbsp;</div>", unsafe_allow_html=True)
        if st.button("Add Guest", use_container_width=True):
            name = guest_name.strip()
            if name:
                st.session_state.guests.append({
                    "name": name,
                    "level": float(guest_level),
                    "pref": guest_pref,
                    "partner": "",
                    "opponent": "",
                    "avoid": "",
                })
                st.session_state.guest_add_counter += 1  # resets the form fields
                st.rerun()

    if st.session_state.guests:
        st.markdown("<div style='font-size:0.78rem;color:#8b949e;margin:8px 0 4px 0;'>Set partner or opponent after adding both players:</div>", unsafe_allow_html=True)

        # Header
        gh0, gh1, gh2, gh3, gh4, gh5 = st.columns([2.0, 1.2, 1.5, 2.0, 2.0, 0.8])
        gh0.markdown("<div style='font-size:0.75rem;color:#4ade80;font-weight:600;'>GUEST</div>", unsafe_allow_html=True)
        gh1.markdown("<div style='font-size:0.75rem;color:#4ade80;font-weight:600;'>LEVEL</div>", unsafe_allow_html=True)
        gh2.markdown("<div style='font-size:0.75rem;color:#4ade80;font-weight:600;'>PREF</div>", unsafe_allow_html=True)
        gh3.markdown("<div style='font-size:0.75rem;color:#4ade80;font-weight:600;'>PARTNER</div>", unsafe_allow_html=True)
        gh4.markdown("<div style='font-size:0.75rem;color:#4ade80;font-weight:600;'>OPPONENT (R1)</div>", unsafe_allow_html=True)

        for i, g in enumerate(st.session_state.guests):
            opts = [""] + [n for n in all_names if n != g["name"]]
            gc0, gc1, gc2, gc3, gc4, gc5 = st.columns([2.0, 1.2, 1.5, 2.0, 2.0, 0.8])
            with gc0:
                st.markdown(f"<div style='padding-top:0.4rem;color:#e6edf3;font-weight:500;'>{g['name']}</div>", unsafe_allow_html=True)
            with gc1:
                st.markdown(f"<div style='padding-top:0.4rem;color:#c9d1d9;'>{g['level']}</div>", unsafe_allow_html=True)
            with gc2:
                pref_opts = ["Either", "Singles", "Doubles"]
                cur_gpref = g.get("pref", "Either")
                new_gpref = st.selectbox("", pref_opts,
                    index=pref_opts.index(cur_gpref) if cur_gpref in pref_opts else 0,
                    key=f"gpref_{i}", label_visibility="collapsed")
                g["pref"] = new_gpref
            with gc3:
                if new_gpref == "Doubles":
                    cur_partner = g.get("partner", "")
                    partner_idx = opts.index(cur_partner) if cur_partner in opts else 0
                    new_partner = st.selectbox("", opts, index=partner_idx,
                        key=f"gpartner_{i}", label_visibility="collapsed")
                    if new_partner != cur_partner:
                        g["partner"] = new_partner
                        for other in st.session_state.guests:
                            if other["name"] == new_partner and not other.get("partner"):
                                other["partner"] = g["name"]
                    else:
                        g["partner"] = new_partner
                else:
                    g["partner"] = ""
                    st.markdown("<div style='padding-top:0.4rem;color:#4a5568;font-size:0.8rem;'>—</div>", unsafe_allow_html=True)
            with gc4:
                if new_gpref == "Singles":
                    cur_opp = g.get("opponent", "")
                    opp_idx = opts.index(cur_opp) if cur_opp in opts else 0
                    new_opp = st.selectbox("", opts, index=opp_idx,
                        key=f"gopp_{i}", label_visibility="collapsed")
                    g["opponent"] = new_opp
                else:
                    g["opponent"] = ""
                    st.markdown("<div style='padding-top:0.4rem;color:#4a5568;font-size:0.8rem;'>—</div>", unsafe_allow_html=True)
            with gc5:
                if st.button("✕", key=f"remove_guest_{i}"):
                    st.session_state.guests.pop(i)
                    st.rerun()

    # Build final player list
    players = []
    for p in master_players:
        if st.session_state.get(f"chk_{p['name']}", False):
            ov = st.session_state.overrides.get(p["name"], {})
            players.append({
                "name": p["name"],
                "level": p["level"],
                "pref": ov.get("pref") or p["pref"],
                "partner": ov.get("partner") or p["partner"],
                "opponent": ov.get("opponent") or p["opponent"],
                "avoid": p["avoid"],
            })
    players.extend(st.session_state.guests)

    # Enforce bidirectional partner links — if A has partner=B, ensure B also has partner=A
    name_to_player = {p["name"]: p for p in players}
    for p in players:
        if p["partner"]:
            other = name_to_player.get(p["partner"])
            if other and not other["partner"]:
                other["partner"] = p["name"]

    st.markdown("---")

    if not players:
        st.markdown('<div class="warning-box">⚠️ No players selected — check at least one player above.</div>', unsafe_allow_html=True)
    else:
        n_singles = sum(1 for p in players if p["pref"] == "Singles")
        n_doubles = sum(1 for p in players if p["pref"] == "Doubles")
        n_either = sum(1 for p in players if p["pref"] == "Either")
        n_fp = sum(1 for p in players if p["partner"])
        n_fo = sum(1 for p in players if p["opponent"])

        st.markdown(f"""
        <div>
            <span class="stat-pill">Playing today: <span>{len(players)}</span></span>
            <span class="stat-pill">Singles-only: <span>{n_singles}</span></span>
            <span class="stat-pill">Doubles-only: <span>{n_doubles}</span></span>
            <span class="stat-pill">Either: <span>{n_either}</span></span>
            <span class="stat-pill">Fixed partners: <span>{n_fp}</span></span>
            <span class="stat-pill">Fixed opponents: <span>{n_fo}</span></span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        col_btn, col_info = st.columns([2, 3])
        with col_btn:
            generate = st.button("🎾 Generate Matchups")
        with col_info:
            if st.session_state.seed > 42:
                st.caption(f"Click again for a different arrangement. (seed {st.session_state.seed})")

        if generate:
            try:
                seed = st.session_state.seed
                st.session_state.seed += 1
                rng = random.Random(seed)

                r1_singles, r1_doubles, r1_on_deck, r1_matchup_keys, r1_partner_pairs, r1_singles_keys = assign_round1(players, rng=rng, max_courts=max_courts)
                r1_courts, _ = render_schedule(r1_singles, r1_doubles, [], 1, balance_threshold)

                r2_singles, r2_doubles, r2_on_deck = assign_round2(players, rng, r1_matchup_keys, r1_partner_pairs, r1_singles_keys=r1_singles_keys, max_courts=max_courts, balance_threshold=balance_threshold)
                r2_courts, _ = render_schedule(r2_singles, r2_doubles, [], 2, balance_threshold)

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

                all_names_set = set(p["name"] for p in players)
                r1_missing = all_names_set - r1_names
                r2_missing = all_names_set - r2_names

                st.session_state.schedule = {
                    "r1_courts": r1_courts,
                    "r2_courts": r2_courts,
                    "r1_on_deck": r1_on_deck,
                    "r2_on_deck": r2_on_deck,
                    "r1_missing": r1_missing,
                    "r2_missing": r2_missing,
                    "n_players": len(players),
                }
            except Exception as e:
                import traceback
                st.markdown(f'<div class="warning-box">❌ Error generating schedule: {e}<br><pre>{traceback.format_exc()}</pre></div>', unsafe_allow_html=True)

        if "schedule" in st.session_state and st.session_state.schedule:
            sched = st.session_state.schedule
            r1_courts = sched["r1_courts"]
            r2_courts = sched["r2_courts"]
            r1_on_deck = sched["r1_on_deck"]
            r2_on_deck = sched["r2_on_deck"]

            if sched["r1_missing"] or sched["r2_missing"]:
                st.markdown(f'<div class="warning-box">⚠️ Integrity check failed. Missing in R1: {sched["r1_missing"]}. Missing in R2: {sched["r2_missing"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="success-box">✅ All {sched["n_players"]} players accounted for in both rounds.</div>', unsafe_allow_html=True)

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
            export_str = export_text(r1_courts, r1_on_deck, r2_courts, r2_on_deck)
            st.download_button(
                "📄 Export Schedule as .txt",
                data=export_str.encode(),
                file_name="tennis_schedule.txt",
                mime="text/plain",
            )
