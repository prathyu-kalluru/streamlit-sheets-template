"""Step 2: Read any public Google Sheet and build a dashboard.

Paste a Google Sheet URL into the app — no source editing, no secrets.
The app figures out the spreadsheet ID and tab (gid) from whatever URL
you paste, turns it into a CSV export URL, loads it with pandas, and
visualises it.

The sheet has to be readable without logging in — either:
  * "Published to web" as CSV (File -> Share -> Publish to web -> CSV), or
  * shared as "Anyone with the link -> Viewer".

Expected columns (header row of the sheet):
  timestamp | workshop | rating | comments | status
"""

import re
from urllib.parse import parse_qs, urlparse

import pandas as pd
import streamlit as st

# Just a starting value in the input box — paste your own URL to replace it.
# A normal "Copy link" sheet URL works: the app extracts the id and builds the
# CSV export URL itself. (A "Publish to web" .../pub?output=csv link works too.)
DEFAULT_SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1n0elq13sj-OVoTSgQUKYaNau_7QPGZp6jrxdoE6WTi0/edit"
)
#prtahyusha
def parse_sheet_url(url: str) -> dict:
    """Pull the spreadsheet id + tab out ofa Google Sheets URL and derive a CSV URL.

    Recognises the two links students actually paste:
      * Published-to-web:  .../spreadsheets/d/e/<TOKEN>/pub?output=csv
      * Normal / shared:   .../spreadsheets/d/<ID>/edit#gid=<GID>
    Returns {kind, id, gid, csv_url}; csv_url is None if we can't make sense of it.
    """
    url = url.strip()
    parsed = urlparse(url)
    # gid (the tab) can ride in the query (?gid=) or the fragment (#gid=).
    gid = (
        parse_qs(parsed.query).get("gid", [None])[0]
        or parse_qs(parsed.fragment).get("gid", [None])[0]
    )

    # Published-to-web token: /spreadsheets/d/e/<TOKEN>/pub...  (check this first;
    # the bare /d/<id> pattern below would otherwise grab the literal "e").
    published = re.search(r"/spreadsheets/d/e/([\w-]+)/pub", url)
    if published:
        token = published.group(1)
        csv_url = (
            f"https://docs.google.com/spreadsheets/d/e/{token}/pub?output=csv"
        )
        if gid:
            csv_url += f"&gid={gid}&single=true"
        return {"kind": "Published to web", "id": token, "gid": gid, "csv_url": csv_url}

    # Normal / link-shared sheet: /spreadsheets/d/<ID>/...
    shared = re.search(r"/spreadsheets/d/([\w-]+)", url)
    if shared:
        sheet_id = shared.group(1)
        csv_url = (
            f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        )
        if gid:
            csv_url += f"&gid={gid}"
        return {"kind": "Shared link (CSV export)", "id": sheet_id, "gid": gid, "csv_url": csv_url}

    # Already a direct CSV link of some other shape — just use it as given.
    if "output=csv" in url or "format=csv" in url:
        return {"kind": "Direct CSV URL", "id": None, "gid": gid, "csv_url": url}

    return {"kind": None, "id": None, "gid": gid, "csv_url": None}


@st.cache_data(ttl=60)
def load_data(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    if "rating" in df.columns:
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    return df


st.set_page_config(page_title="Step 2: Feedback dashboard", page_icon="📊", layout="wide")
st.title("📊 the great Sai Badrik")
st.caption("Step 2 — paste a public Google Sheet URL below. Data refreshes every 60 seconds.")

url_input = st.text_input(
    "Google Sheet URL",
    value=DEFAULT_SHEET_URL,
    help="A 'Publish to web' CSV link, or a normal sheet link shared as "
    "'Anyone with the link → Viewer'.",
)

if not url_input.strip():
    st.info("Paste a Google Sheet URL above to load its data.")
    st.stop()

info = parse_sheet_url(url_input)

if not info["csv_url"]:
    st.error(
        "That doesn't look like a Google Sheets URL. Paste something like "
        "`https://docs.google.com/spreadsheets/d/.../edit` or a published "
        "`.../pub?output=csv` link."
    )
    st.stop()

# --- What we pulled out of the URL (the new "extract info" bit) ---
with st.expander("ℹ️ Sheet info (read from the URL)", expanded=True):
    i1, i2, i3 = st.columns(3)
    i1.markdown(f"**Link type**  \n{info['kind']}")
    i2.markdown(f"**Spreadsheet ID**  \n`{info['id'] or '—'}`")
    i3.markdown(f"**Tab (gid)**  \n`{info['gid'] or 'first / default'}`")
    st.markdown("**CSV URL the app will read:**")
    st.code(info["csv_url"], language="text")

try:
    df = load_data(info["csv_url"])
except Exception as e:
    st.error(
        "Couldn't load the sheet. Is it published to web, or shared as "
        f"'Anyone with the link'?\n\n{e}"
    )
    st.stop()

if df.empty:
    st.warning("The sheet loaded but has no rows. Add data below the header row and refresh.")
    st.stop()

st.success(
    f"Loaded **{len(df)} rows** × **{len(df.columns)} columns**: "
    f"{', '.join(df.columns)}"
)

with st.sidebar:
    st.header("Filters")
    rating_min, rating_max = st.slider("Rating range", 1, 5, (1, 5))
    workshop_search = st.text_input("Workshop name contains", "")

filtered = df.copy()
if "rating" in filtered.columns:
    filtered = filtered[filtered["rating"].between(rating_min, rating_max, inclusive="both")]
if workshop_search and "workshop" in filtered.columns:
    filtered = filtered[filtered["workshop"].astype(str).str.contains(workshop_search, case=False, na=False)]

c1, c2, c3 = st.columns(3)
c1.metric("Total responses", len(filtered))
c2.metric("Mean rating", f"{filtered['rating'].mean():.2f}" if len(filtered) and "rating" in filtered.columns else "—")
c3.metric("Distinct workshops", filtered["workshop"].nunique() if "workshop" in filtered.columns else 0)

c4, c5 = st.columns(2)
with c4:
    st.subheader("Rating distribution")
    if "rating" in filtered.columns and len(filtered):
        st.bar_chart(filtered["rating"].value_counts().sort_index())
    else:
        st.info("No rating data to chart.")
with c5:
    st.subheader("Submissions per day")
    if "timestamp" in filtered.columns and filtered["timestamp"].notna().any():
        per_day = filtered.groupby(filtered["timestamp"].dt.date).size()
        st.line_chart(per_day)
    else:
        st.info("No timestamp data to chart.")

with st.expander("Show raw data"):
    st.dataframe(filtered, width="stretch", hide_index=True)
