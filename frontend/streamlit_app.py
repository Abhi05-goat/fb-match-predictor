from urllib.parse import quote


import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st



DEFAULT_API_BASE_URL = "http://127.0.0.1:8000" # "https://fb-match-predictor.onrender.com" 
PLOT_BG = "rgba(0,0,0,0)"
GRID = "#e6eefb"
INK = "#111827"
MUTED = "#667085"
GREEN = "#0ea5e9"
BLUE = "#2563eb"
GOLD = "#d69b2d"
RED = "#c2414b"

TEAM_DOMAINS = {
    "Inter": "inter.it", "Milan": "acmilan.com", "Juventus": "juventus.com",
    "Roma": "asroma.com", "Napoli": "sscnapoli.it", "Lazio": "sslazio.it",
    "Atalanta": "atalanta.it", "Fiorentina": "acffiorentina.com", "Bologna": "bolognafc.it",
    "Torino": "torinofc.it", "Genoa": "genoacfc.it", "Verona": "hellasverona.it",
    "Sassuolo": "sassuolocalcio.it", "Udinese": "udinese.it", "Monza": "acmonza.com",
    "Lecce": "uslecce.it", "Salernitana": "salernitana.it", "Cagliari": "cagliaricalcio.com",
    "Empoli": "empolifc.com", "Frosinone": "frosinonecalcio.com", "Sampdoria": "sampdoria.it",
    "Spezia": "acspezia.com", "Cremonese": "uscremonese.it", "Venezia": "veneziafc.it",
    "Como": "comofootball.com", "Parma": "parmacalcio1913.com"
}

def get_team_logo_url(team_name: str) -> str:
    domain = TEAM_DOMAINS.get(team_name)
    if domain:
        return f"https://t3.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://{domain}&size=128"
    initials = "".join(part[0] for part in team_name.split()).upper()[:3]
    return f"https://ui-avatars.com/api/?name={initials}&background=0D8ABC&color=fff&rounded=true&bold=true"



st.set_page_config(
    page_title="Serie A Analytics",
    page_icon="SP",
    layout="wide",
    initial_sidebar_state="expanded",
)



st.markdown(
    """
    <style>
    :root {
        --pitch: #1d4ed8;
        --pitch-dark: #102a56;
        --ink: #111827;
        --muted: #667085;
        --panel: #ffffff;
        --line: #dbe7fb;
        --gold: #d69b2d;
        --blue: #2563eb;
        --red: #c2414b;
    }


    .stApp {
        background:
            linear-gradient(180deg, rgba(37, 99, 235, 0.12), rgba(248, 251, 255, 0.55) 360px),
            #f8fbff;
    }


    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f3f8f, #0b1f45);
    }


    section[data-testid="stSidebar"] * {
        color: #effaf4;
    }


    section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
    section[data-testid="stSidebar"] div[data-baseweb="select"] span,
    section[data-testid="stSidebar"] input {
        color: #102a56 !important;
        opacity: 1 !important;
        -webkit-text-fill-color: #102a56 !important;
    }


    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        border-radius: 8px;
        background: #ffffff !important;
        border-color: rgba(219, 231, 251, 0.95);
        box-shadow: 0 10px 24px rgba(15, 63, 143, 0.15);
    }


    section[data-testid="stSidebar"] div[data-baseweb="select"] svg {
        color: #2563eb !important;
    }


    div[data-testid="stMetric"] {
        padding: 18px 18px 14px;
        border: 1px solid var(--line);
        border-radius: 10px;
        background: var(--panel);
        box-shadow: 0 14px 34px rgba(20, 35, 52, 0.08);
    }


    div[data-testid="stMetricLabel"] p {
        color: var(--muted);
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }


    div[data-testid="stMetricValue"] {
        color: var(--ink);
        font-weight: 900;
    }


    .hero {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 22px;
        padding: 24px;
        margin-bottom: 20px;
        border-radius: 12px;
        background:
            linear-gradient(135deg, rgba(29, 78, 216, 0.96), rgba(15, 42, 90, 0.98)),
            #102a56;
        color: white;
        box-shadow: 0 24px 64px rgba(37, 99, 235, 0.22);
    }


    .hero h1 {
        margin: 0 0 8px;
        color: white;
        font-size: clamp(2rem, 5vw, 4.5rem);
        line-height: 0.94;
        letter-spacing: 0;
    }


    .hero p {
        margin: 0;
        color: #cfeadd;
        font-size: 1.02rem;
        line-height: 1.55;
    }


    .crest {
        display: grid;
        place-items: center;
        min-width: 104px;
        width: 104px;
        height: 104px;
        border: 3px solid rgba(255, 255, 255, 0.28);
        border-radius: 50%;
        background: #ffffff;
        color: #06452f;
        font-size: 2rem;
        font-weight: 950;
        overflow: hidden;
    }


    .crest img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        padding: 10px;
    }


    .section-title {
        margin: 10px 0 10px;
        color: #142033;
        font-size: 1.3rem;
        font-weight: 850;
    }


    .card {
        padding: 18px;
        border: 1px solid var(--line);
        border-radius: 10px;
        background: #ffffff;
        box-shadow: 0 12px 30px rgba(20, 35, 52, 0.07);
    }


    .badge-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 14px;
    }


    .badge {
        padding: 7px 10px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.22);
        color: #effaf4;
        font-size: 0.84rem;
        font-weight: 750;
    }


    .empty-panel {
        padding: 48px 24px;
        border: 1px dashed #a8b9af;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.76);
        text-align: center;
    }


    .empty-panel h2 {
        margin-bottom: 8px;
        color: #142033;
    }


    .empty-panel p {
        color: var(--muted);
    }


    .sidebar-card {
        padding: 14px;
        margin: 12px 0 18px;
        border: 1px solid rgba(255, 255, 255, 0.14);
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.08);
    }


    .sidebar-card p {
        margin: 0;
        color: #cfeadd;
        font-size: 0.9rem;
        line-height: 1.45;
    }


    .chart-card {
        padding: 10px 10px 2px;
        border: 1px solid var(--line);
        border-radius: 10px;
        background: #ffffff;
        box-shadow: 0 18px 42px rgba(37, 99, 235, 0.11);
    }


    .insight-card {
        min-height: 120px;
        padding: 18px;
        border: 1px solid var(--line);
        border-radius: 12px;
        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.94), rgba(239, 246, 255, 0.92)),
            #ffffff;
        box-shadow: 0 16px 38px rgba(37, 99, 235, 0.10);
    }


    .insight-card span {
        display: block;
        margin-bottom: 8px;
        color: #64748b;
        font-size: 0.78rem;
        font-weight: 900;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }


    .insight-card strong {
        display: block;
        color: #102a56;
        font-size: 1.8rem;
        line-height: 1;
    }


    .insight-card p {
        margin: 10px 0 0;
        color: #64748b;
        font-weight: 700;
    }


    .comparison-hero {
        margin: 4px 0 18px;
        padding: 22px;
        border: 1px solid #dbe7fb;
        border-radius: 12px;
        background:
            linear-gradient(135deg, rgba(37, 99, 235, 0.12), rgba(255, 255, 255, 0.96)),
            #ffffff;
        box-shadow: 0 18px 44px rgba(37, 99, 235, 0.10);
    }


    .comparison-hero span {
        display: block;
        margin-bottom: 8px;
        color: #2563eb;
        font-size: 0.78rem;
        font-weight: 900;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }


    .comparison-hero h2 {
        margin: 0;
        color: #102a56;
        font-size: clamp(1.8rem, 4vw, 3.4rem);
        line-height: 1;
    }


    .matchup-card {
        padding: 18px;
        border: 1px solid #dbe7fb;
        border-radius: 12px;
        background: #ffffff;
        box-shadow: 0 18px 44px rgba(37, 99, 235, 0.09);
    }


    .matchup-row {
        display: grid;
        grid-template-columns: minmax(130px, 1fr) minmax(120px, 0.8fr) minmax(130px, 1fr);
        align-items: center;
        gap: 12px;
        padding: 12px 0;
        border-bottom: 1px solid #edf3ff;
    }


    .matchup-row:last-child {
        border-bottom: 0;
    }


    .matchup-name {
        color: #667085;
        font-size: 0.76rem;
        font-weight: 900;
        letter-spacing: 0.04em;
        text-align: center;
        text-transform: uppercase;
    }


    .matchup-value {
        padding: 12px 14px;
        border: 1px solid #e5eefc;
        border-radius: 10px;
        background: #f8fbff;
        color: #102a56;
        font-size: 1.28rem;
        font-weight: 900;
        text-align: center;
    }


    .matchup-value.win {
        border-color: rgba(37, 99, 235, 0.28);
        background: rgba(37, 99, 235, 0.10);
        color: #1d4ed8;
        box-shadow: 0 10px 24px rgba(37, 99, 235, 0.12);
    }


    div[data-testid="stTabs"] button p {
        font-weight: 800;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



def format_season(season: int | str) -> str:
    value = str(season)
    if len(value) != 4:
        return value
    return f"{value[:2]}/{value[2:]}"



def team_initials(team_name: str) -> str:
    return "".join(part[0] for part in team_name.split()).upper()[:3]



def get_json(api_base_url: str, path: str):
    response = requests.get(f"{api_base_url}{path}", timeout=10)
    response.raise_for_status()
    return response.json()



def load_seasons(api_base_url: str) -> list[int]:
    data = get_json(api_base_url, "/seasons")
    return sorted(data.get("seasons", []))



def load_teams(api_base_url: str, season: int) -> list[str]:
    data = get_json(api_base_url, f"/seasons/{season}/teams")
    return sorted(data.get("teams", []))



def load_summary(api_base_url: str, season: int, team_name: str) -> dict:
    encoded_team = quote(team_name, safe="")
    return get_json(api_base_url, f"/seasons/{season}/teams/{encoded_team}/summary")

@st.cache_data(ttl=3600)
def load_all_summaries(api_base_url: str, season: int, teams: list[str]) -> list[dict]:
    summaries = []
    for t in teams:
        summaries.append(load_summary(api_base_url, season, t))
    return summaries

def format_ordinal(n: int) -> str:
    if 11 <= (n % 100) <= 13:
        return f"{n}th"
    return f"{n}" + {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")

def get_metric_rank(summaries: list[dict], team_name: str, metric_key: str, higher_is_better: bool = True) -> str:
    if metric_key == "cards_per_match":
        sorted_teams = sorted(summaries, key=lambda x: x["yellow_cards_per_match"] + x["red_cards_per_match"], reverse=higher_is_better)
    else:
        sorted_teams = sorted(summaries, key=lambda x: x[metric_key], reverse=higher_is_better)
    for i, t in enumerate(sorted_teams):
        if t["team_name"] == team_name:
            rank = format_ordinal(i + 1)
            return f"Ranked {rank}"
    return ""



def load_standings(api_base_url: str, season: int) -> list[dict]:
    return get_json(api_base_url, f"/seasons/{season}/teams/standings")







def base_figure_layout(fig: go.Figure, title: str, height: int = 370) -> go.Figure:
    fig.update_layout(
        title={
            "text": f"<b>{title}</b>",
            "font": {"size": 22, "color": INK},
            "x": 0.02,
            "xanchor": "left",
            "y": 0.96,
        },
        height=height,
        margin=dict(l=28, r=28, t=80, b=34),
        paper_bgcolor=PLOT_BG,
        plot_bgcolor=PLOT_BG,
        font={"family": "Inter, Segoe UI, sans-serif", "color": INK},
        showlegend=False,
    )
    fig.update_xaxes(
        gridcolor=GRID,
        zeroline=False,
        linecolor="rgba(17,24,39,0.12)",
        tickfont={"size": 12, "color": MUTED},
        title_font={"color": MUTED},
    )
    fig.update_yaxes(
        gridcolor=GRID,
        zeroline=False,
        linecolor="rgba(17,24,39,0.12)",
        tickfont={"size": 12, "color": MUTED},
        title_font={"color": MUTED},
    )
    return fig







def goals_chart(summary: dict) -> go.Figure:
    labels = ["Goals scored / match", "Average xG"]
    values = [
        summary["goals_scored_per_match"],
        summary["average_xg"],
    ]
    colors = [
        "rgba(37, 99, 235, 0.70)",
        "rgba(14, 165, 233, 0.62)",
    ]


    fig = go.Figure(
        data=[
            go.Bar(
                x=values,
                y=labels,
                orientation="h",
                marker_color=colors,
                marker_line_color="rgba(255,255,255,0.95)",
                marker_line_width=2,
                width=0.52,
                text=[round(value, 2) for value in values],
                textposition="outside",
                textfont={"size": 15, "color": INK},
                hovertemplate="<b>%{y}</b><br>%{x}<extra></extra>",
            )
        ]
    )
    base_figure_layout(fig, "Scoring Output")
    fig.update_xaxes(title="")
    fig.update_yaxes(title="", autorange="reversed")
    return fig



def team_profile_chart(summary: dict) -> go.Figure:
    categories = ["Points", "Goal diff", "xG", "Defense", "Elo", "Control"]
    values = [
        min(summary["points_per_match"] / 3, 1),
        max(min((summary["goal_difference"] + 60) / 120, 1), 0),
        min(summary["average_xg"] / 3, 1),
        max(min((3 - summary["goals_conceded_per_match"]) / 3, 1), 0),
        max(min((summary["average_elo_score"] - 1300) / 800, 1), 0),
        max(min((18 - summary["average_ppda"]) / 18, 1), 0),
    ]
    values.append(values[0])
    categories.append(categories[0])


    fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=values,
                theta=categories,
                fill="toself",
                fillcolor="rgba(37, 99, 235, 0.20)",
                line={"color": BLUE, "width": 3},
                marker={"size": 7, "color": BLUE},
                hovertemplate="<b>%{theta}</b><br>Score: %{r:.2f}<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        title={
            "text": "<b>Team Strength Shape</b>",
            "font": {"size": 22, "color": INK},
            "x": 0.02,
            "xanchor": "left",
        },
        height=390,
        margin=dict(l=28, r=28, t=76, b=28),
        paper_bgcolor=PLOT_BG,
        polar={
            "bgcolor": PLOT_BG,
            "radialaxis": {
                "visible": True,
                "range": [0, 1],
                "showticklabels": False,
                "gridcolor": GRID,
            },
            "angularaxis": {
                "gridcolor": GRID,
                "tickfont": {"size": 12, "color": MUTED},
            },
        },
        showlegend=False,
        font={"family": "Inter, Segoe UI, sans-serif", "color": INK},
    )
    return fig



def discipline_chart(summary: dict) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=summary["average_ppda"],
            title={"text": "Average PPDA"},
            gauge={
                "axis": {"range": [0, 20]},
                "bar": {"color": "rgba(37, 99, 235, 0.72)"},
                "borderwidth": 1,
                "bordercolor": "#dbe7fb",
                "steps": [
                    {"range": [0, 8], "color": "rgba(37, 99, 235, 0.16)"},
                    {"range": [8, 14], "color": "rgba(214, 155, 45, 0.16)"},
                    {"range": [14, 20], "color": "rgba(194, 65, 75, 0.16)"},
                ],
            },
        )
    )
    fig.update_layout(
        height=330,
        margin=dict(l=18, r=18, t=52, b=18),
        paper_bgcolor=PLOT_BG,
        font={"family": "Inter, Segoe UI, sans-serif", "color": INK},
    )
    return fig



def generate_ai_insight(summary: dict) -> list[str]:
    insights = []
    
    # Pressing Profile
    ppda = summary["average_ppda"]
    if ppda < 10.5:
        insights.append(f"🔥 **Aggressive Pressing:** An elite PPDA of {ppda} means they suffocate opponents high up the pitch.")
    elif ppda > 14.5:
        insights.append(f"🛡️ **Low Block:** A PPDA of {ppda} indicates they prefer sitting deep and inviting pressure rather than pressing high.")
    else:
        insights.append(f"⚖️ **Balanced Pressing:** A moderate PPDA of {ppda} shows selective pressing triggers.")
        
    # Attack Profile
    xg = summary["average_xg"]
    goals = summary["goals_scored_per_match"]
    if goals > xg + 0.3:
        insights.append(f"⚽ **Clinical Finishers:** They score {goals} goals/match from only {xg} xG, significantly outperforming their expected output.")
    elif goals < xg - 0.2:
        insights.append(f"📉 **Underperforming Attack:** Creating dangerous chances ({xg} xG) but failing to finish them ({goals} goals/match).")
    else:
        insights.append(f"📊 **Consistent Attack:** Their goal output ({goals}) closely mirrors the quality of chances they create ({xg} xG).")
        
    # Defense Profile
    gd = summary["goal_difference"] / summary["matches_played"]
    if gd > 1.0:
        insights.append("🏰 **Dominant Force:** They win games by a massive average margin of over a goal per game.")
    elif gd < -0.8:
        insights.append("⚠️ **Defensive Crisis:** Vulnerable at the back, frequently bleeding goals and losing games comfortably.")
        
    return insights

def render_insights(summary: dict) -> None:
    st.markdown('<div class="section-title">AI Gen Insights 🔮</div>', unsafe_allow_html=True)
    
    insights = generate_ai_insight(summary)
    for insight in insights:
        st.info(insight, icon="🤖")
        
    st.markdown('<div class="section-title" style="margin-top: 24px;">Quick Reads</div>', unsafe_allow_html=True)
    
    goal_diff_per_match = round(summary["goal_difference"] / summary["matches_played"], 2)
    discipline_load = round(summary["yellow_cards_per_match"] + summary["red_cards_per_match"], 2)


    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(
            f"""
            <div class="insight-card">
                <span>Season Pace</span>
                <strong>{summary["points_per_match"]}</strong>
                <p>Points per match for clean cross-season comparison.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_b:
        st.markdown(
            f"""
            <div class="insight-card">
                <span>Goal Margin</span>
                <strong>{goal_diff_per_match}</strong>
                <p>Goal difference per match, normalized by season length.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_c:
        st.markdown(
            f"""
            <div class="insight-card">
                <span>Discipline Load</span>
                <strong>{discipline_load}</strong>
                <p>Total cards per match across yellow and red cards.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )



def render_team_header(summary: dict) -> None:
    logo_url = get_team_logo_url(summary["team_name"])
    st.markdown(
        f"""
        <div class="hero">
            <div>
                <p>Serie A Analytics</p>
                <h1>{summary["team_name"]}</h1>
                <div class="badge-row">
                    <span class="badge">Season {format_season(summary["season"])}</span>
                    <span class="badge">{summary["matches_played"]} matches</span>
                    <span class="badge">{summary["wins"]}W {summary["draws"]}D {summary["losses"]}L</span>
                </div>
            </div>
            <div class="crest"><img src="{logo_url}" alt="{summary['team_name']}"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )



def render_standings(standings: list[dict], selected_team: str, season: int) -> None:
    st.markdown('<p style="margin:10px 0 10px; color:#142033; font-size:1.3rem; font-weight:850;">Standings</p>', unsafe_allow_html=True)

    rows_html = ""
    for i, row in enumerate(standings, start=1):
        is_selected = row["team_name"] == selected_team

        if i <= 4:
            rank_color = "#2563eb"
        elif i <= 6:
            rank_color = "#d69b2d"
        elif i == 7 and season >= 2122:
            rank_color = "#10b981"
        elif i >= 18:
            rank_color = "#c2414b"
        else:
            rank_color = "#667085"

        row_bg = "background:rgba(37,99,235,0.08);" if is_selected else ""
        team_label = f"<b>{row['team_name']}</b>" if is_selected else row["team_name"]
        gd = f"+{row['goal_difference']}" if row["goal_difference"] > 0 else str(row["goal_difference"])
        
        logo_url = get_team_logo_url(row["team_name"])

        rows_html += f"""
        <tr style="{row_bg}">
            <td style="color:{rank_color};font-weight:900;padding:7px 6px;text-align:center;">{i}</td>
            <td style="padding:7px 6px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <img src="{logo_url}" style="width: 20px; height: 20px; object-fit: contain;">
                    <span style="max-width:90px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{team_label}</span>
                </div>
            </td>
            <td style="text-align:center;padding:7px 4px;color:#667085;">{row['matches_played']}</td>
            <td style="text-align:center;padding:7px 4px;">{row['wins']}</td>
            <td style="text-align:center;padding:7px 4px;color:#667085;">{row['draws']}</td>
            <td style="text-align:center;padding:7px 4px;color:#c2414b;">{row['losses']}</td>
            <td style="text-align:center;padding:7px 4px;color:#667085;">{gd}</td>
            <td style="text-align:center;padding:7px 6px;font-weight:900;color:#102a56;">{row['total_points']}</td>
        </tr>
        """

    hs = "padding:10px 8px;color:#667085;font-size:0.78rem;font-weight:900;letter-spacing:0.05em;text-transform:uppercase;text-align:center;border-bottom:2px solid #dbe7fb;"

    conference_html = '<span style="font-size:0.72rem;color:#10b981;font-weight:800;">&#9632; Conference League</span>' if season >= 2122 else ''

    html = f"""
    <div style="padding:16px 12px;border:1px solid #dbe7fb;border-radius:10px;background:#ffffff;box-shadow:0 12px 30px rgba(20,35,52,0.07);">
        <table style="width:100%;border-collapse:collapse;font-size:0.92rem;font-family:Inter,sans-serif;">
            <thead>
                <tr>
                    <th style="{hs}">#</th>
                    <th style="{hs}text-align:left;">Club</th>
                    <th style="{hs}">MP</th>
                    <th style="{hs}">W</th>
                    <th style="{hs}">D</th>
                    <th style="{hs}">L</th>
                    <th style="{hs}">GD</th>
                    <th style="{hs}">Pts</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
        <div style="display:flex;gap:12px;margin-top:10px;flex-wrap:wrap;">
            <span style="font-size:0.72rem;color:#2563eb;font-weight:800;">&#9632; Champions League</span>
            <span style="font-size:0.72rem;color:#d69b2d;font-weight:800;">&#9632; Europa</span>
            {conference_html}
            <span style="font-size:0.72rem;color:#c2414b;font-weight:800;">&#9632; Relegation</span>
        </div>
    </div>
    """
    st.html(html)

def render_leaderboard(all_summaries: list[dict], metric_key: str, title: str, higher_is_better: bool = True) -> None:
    if metric_key == "goal_difference_per_match":
        sorted_teams = sorted(all_summaries, key=lambda x: x["goal_difference"] / x["matches_played"] if x["matches_played"] > 0 else 0, reverse=higher_is_better)
        values = [round(t["goal_difference"] / t["matches_played"], 2) if t["matches_played"] > 0 else 0 for t in sorted_teams]
    elif metric_key == "cards_per_match":
        sorted_teams = sorted(all_summaries, key=lambda x: x["yellow_cards_per_match"] + x["red_cards_per_match"], reverse=higher_is_better)
        values = [round(t["yellow_cards_per_match"] + t["red_cards_per_match"], 2) for t in sorted_teams]
    else:
        sorted_teams = sorted(all_summaries, key=lambda x: x[metric_key], reverse=higher_is_better)
        values = [round(t[metric_key], 2) for t in sorted_teams]
        
    df = pd.DataFrame({
        "Rank": [i+1 for i in range(len(sorted_teams))],
        "Team": [t["team_name"] for t in sorted_teams],
        title: values
    })
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_summary(summary: dict, all_summaries: list[dict]) -> None:
    render_team_header(summary)

    render_insights(summary)

    st.plotly_chart(team_profile_chart(summary), use_container_width=True)

    st.markdown('<div class="section-title" style="margin-top: 24px; display: flex; justify-content: space-between; align-items: center;"><span>Season Snapshot</span></div>', unsafe_allow_html=True)
    
    with st.expander("📚 Metrics Glossary & Legend", expanded=False):
        st.markdown("""
        - **Grey/Green Text:** Represents absolute totals or contextual definitions, *not* relative improvements.
        - **xG (Expected Goals):** The statistical quality of scoring chances created.
        - **PPDA:** Passes allowed Per Defensive Action. A lower number means the team presses more intensely.
        - **Deep Completions:** Successful passes into the final 20 yards of the pitch.
        - **Elo Rating:** A dynamic skill rating system where 1500 is average.
        """)

    attack_tab, defense_tab, control_tab = st.tabs(["⚔️ Attack", "🛡️ Defense", "🎛️ Control"])

    with attack_tab:
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Goals Scored / Match", summary["goals_scored_per_match"], get_metric_rank(all_summaries, summary["team_name"], "goals_scored_per_match", True), delta_color="off")
        col_b.metric("Average xG", summary["average_xg"], get_metric_rank(all_summaries, summary["team_name"], "average_xg", True), delta_color="off")
        col_c.metric("Deep Comp. / Match", summary["deep_completions_per_match"], get_metric_rank(all_summaries, summary["team_name"], "deep_completions_per_match", True), delta_color="off")
        
        with st.expander("🔬 View Attack Visualizations"):
            st.plotly_chart(goals_chart(summary), use_container_width=True)
            
        with st.expander("🏆 Attack Leaderboards"):
            l_t1, l_t2, l_t3, l_t4 = st.tabs(["Goals Scored", "Goals / Match", "Total xG", "xG / Match"])
            with l_t1: render_leaderboard(all_summaries, "goals_scored", "Goals Scored", True)
            with l_t2: render_leaderboard(all_summaries, "goals_scored_per_match", "Goals / Match", True)
            with l_t3: render_leaderboard(all_summaries, "total_xg", "Total xG", True)
            with l_t4: render_leaderboard(all_summaries, "average_xg", "xG / Match", True)

    with defense_tab:
        col_a, col_b = st.columns(2)
        total_goals_conceded = int(round(summary["goals_conceded_per_match"] * summary["matches_played"]))
        col_a.metric("Goals Conceded / Match", summary["goals_conceded_per_match"], get_metric_rank(all_summaries, summary["team_name"], "goals_conceded_per_match", False), delta_color="off")
        col_b.metric("Total Goals Conceded", total_goals_conceded, get_metric_rank(all_summaries, summary["team_name"], "goals_conceded", False), delta_color="off")

        with st.expander("🏆 Defense Leaderboards"):
            l_t1, l_t2, l_t3, l_t4 = st.tabs(["Goals Conceded", "Conceded / Match", "Goal Diff", "GD / Match"])
            with l_t1: render_leaderboard(all_summaries, "goals_conceded", "Goals Conceded", False)
            with l_t2: render_leaderboard(all_summaries, "goals_conceded_per_match", "Conceded / Match", False)
            with l_t3: render_leaderboard(all_summaries, "goal_difference", "Goal Diff", True)
            with l_t4: render_leaderboard(all_summaries, "goal_difference_per_match", "GD / Match", True)

    with control_tab:
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Average PPDA", summary["average_ppda"], get_metric_rank(all_summaries, summary["team_name"], "average_ppda", False), delta_color="off")
        col_b.metric("Average Elo", summary["average_elo_score"], get_metric_rank(all_summaries, summary["team_name"], "average_elo_score", True), delta_color="off")
        col_c.metric("Cards / Match", round(summary["yellow_cards_per_match"] + summary["red_cards_per_match"], 2), get_metric_rank(all_summaries, summary["team_name"], "cards_per_match", False), delta_color="off")
        
        with st.expander("🔬 View Control Visualizations"):
            st.plotly_chart(discipline_chart(summary), use_container_width=True)
            
        with st.expander("🏆 Control Leaderboards"):
            l_t1, l_t2, l_t3 = st.tabs(["Average PPDA", "Deep Completions", "Average Elo"])
            with l_t1: render_leaderboard(all_summaries, "average_ppda", "PPDA (Lower=Better)", False)
            with l_t2: render_leaderboard(all_summaries, "total_deep_completions", "Deep Completions", True)
            with l_t3: render_leaderboard(all_summaries, "average_elo_score", "Average Elo", True)



COMPARISON_METRICS = [
    ("Points / Match", "points_per_match", True),
    ("Goals For / Match", "goals_scored_per_match", True),
    ("Goals Against / Match", "goals_conceded_per_match", False),
    ("Average xG", "average_xg", True),
    ("Average Elo", "average_elo_score", True),
    ("Average PPDA", "average_ppda", False),
    ("Deep Comp. / Match", "deep_completions_per_match", True),
    ("Cards / Match", "cards_per_match", False),
]


METRICS_PER_MATCH = [
    ("Points / Match", "points_per_match", True),
    ("Goals For / Match", "goals_scored_per_match", True),
    ("Goals Against / Match", "goals_conceded_per_match", False),
    ("Average xG", "average_xg", True),
    ("Deep Comp. / Match", "deep_completions_per_match", True),
    ("Cards / Match", "cards_per_match", False),
]


METRICS_PPDA = [
    ("Average PPDA", "average_ppda", False),
]


METRICS_ELO = [
    ("Average Elo", "average_elo_score", True),
]



def comparison_value(summary: dict, key: str) -> float:
    if key == "cards_per_match":
        return round(summary["yellow_cards_per_match"] + summary["red_cards_per_match"], 2)
    return summary[key]



def _grouped_bar_chart(
    team_a: dict,
    team_b: dict,
    metrics: list[tuple[str, str, bool]],
    title: str,
    y_title: str,
    height: int = 390,
    y_range: list | None = None,
) -> go.Figure:
    labels = [m[0] for m in metrics]
    values_a = [comparison_value(team_a, m[1]) for m in metrics]
    values_b = [comparison_value(team_b, m[1]) for m in metrics]


    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=labels,
            y=values_a,
            name=team_a["team_name"],
            marker_color="rgba(37, 99, 235, 0.66)",
            marker_line_color="rgba(255,255,255,0.9)",
            marker_line_width=2,
            width=0.34,
            text=[round(v, 2) for v in values_a],
            textposition="outside",
            hovertemplate=f"<b>{team_a['team_name']}</b><br>%{{x}}: %{{y}}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=labels,
            y=values_b,
            name=team_b["team_name"],
            marker_color="rgba(14, 165, 233, 0.54)",
            marker_line_color="rgba(255,255,255,0.9)",
            marker_line_width=2,
            width=0.34,
            text=[round(v, 2) for v in values_b],
            textposition="outside",
            hovertemplate=f"<b>{team_b['team_name']}</b><br>%{{x}}: %{{y}}<extra></extra>",
        )
    )
    base_figure_layout(fig, title, height)
    fig.update_layout(
        barmode="group",
        showlegend=True,
        legend={"orientation": "h", "y": 1.12, "x": 0.02},
    )
    fig.update_yaxes(title=y_title)
    fig.update_xaxes(title="", tickangle=-12)
    if y_range is not None:
        fig.update_yaxes(range=y_range)
    return fig



def comparison_per_match_chart(team_a: dict, team_b: dict) -> go.Figure:
    return _grouped_bar_chart(
        team_a, team_b,
        METRICS_PER_MATCH,
        "Per-Match Metrics",
        "Value per match",
        height=390,
    )



def comparison_ppda_chart(team_a: dict, team_b: dict) -> go.Figure:
    return _grouped_bar_chart(
        team_a, team_b,
        METRICS_PPDA,
        "Pressing Intensity (PPDA)",
        "PPDA (lower = more intense)",
        height=340,
        y_range=[0, 22],
    )



def elo_comparison_chart(team_a: dict, team_b: dict) -> go.Figure:
    values = [team_a["average_elo_score"], team_b["average_elo_score"]]
    names = [team_a["team_name"], team_b["team_name"]]
    y_min = max(min(values) - 80, 0)
    y_max = max(values) + 80


    fig = go.Figure(
        data=[
            go.Bar(
                x=names,
                y=values,
                marker_color=["rgba(37, 99, 235, 0.68)", "rgba(14, 165, 233, 0.56)"],
                marker_line_color="rgba(255,255,255,0.95)",
                marker_line_width=2,
                width=0.46,
                text=values,
                textposition="outside",
                hovertemplate="<b>%{x}</b><br>Average Elo: %{y}<extra></extra>",
            )
        ]
    )
    base_figure_layout(fig, "Average Elo Strength", 360)
    fig.update_yaxes(title="Average Elo", range=[y_min, y_max])
    fig.update_xaxes(title="")
    return fig



def comparison_radar_chart(team_a: dict, team_b: dict) -> go.Figure:
    categories = ["PPM", "Attack", "Defense", "xG", "Elo", "Control"]


    def normalized(summary: dict) -> list[float]:
        return [
            min(summary["points_per_match"] / 3, 1),
            min(summary["goals_scored_per_match"] / 3, 1),
            max(min((3 - summary["goals_conceded_per_match"]) / 3, 1), 0),
            min(summary["average_xg"] / 3, 1),
            max(min((summary["average_elo_score"] - 1300) / 800, 1), 0),
            max(min((18 - summary["average_ppda"]) / 18, 1), 0),
        ]


    values_a = normalized(team_a)
    values_b = normalized(team_b)
    values_a.append(values_a[0])
    values_b.append(values_b[0])
    categories.append(categories[0])


    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values_a,
            theta=categories,
            fill="toself",
            name=team_a["team_name"],
            fillcolor="rgba(37, 99, 235, 0.18)",
            line={"color": BLUE, "width": 3},
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=values_b,
            theta=categories,
            fill="toself",
            name=team_b["team_name"],
            fillcolor="rgba(14, 165, 233, 0.16)",
            line={"color": "#0ea5e9", "width": 3},
        )
    )
    fig.update_layout(
        title={
            "text": "<b>Profile Shape Comparison</b>",
            "font": {"size": 22, "color": INK},
            "x": 0.02,
            "xanchor": "left",
        },
        height=430,
        margin=dict(l=28, r=28, t=76, b=28),
        paper_bgcolor=PLOT_BG,
        polar={
            "bgcolor": PLOT_BG,
            "radialaxis": {
                "visible": True,
                "range": [0, 1],
                "showticklabels": False,
                "gridcolor": GRID,
            },
            "angularaxis": {
                "gridcolor": GRID,
                "tickfont": {"size": 12, "color": MUTED},
            },
        },
        showlegend=True,
        legend={"orientation": "h", "y": 1.08, "x": 0.02},
        font={"family": "Inter, Segoe UI, sans-serif", "color": INK},
    )
    return fig



def render_comparison(team_a: dict, team_b: dict) -> None:
    logo_a = get_team_logo_url(team_a["team_name"])
    logo_b = get_team_logo_url(team_b["team_name"])
    
    st.markdown(
        f"""
        <div class="comparison-hero" style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span>Team vs Team</span>
                <h2>{team_a["team_name"]} vs {team_b["team_name"]}</h2>
            </div>
            <div style="display: flex; gap: 20px; align-items: center;">
                <img src="{logo_a}" style="width: 70px; height: 70px; object-fit: contain;">
                <span style="font-size: 1.5rem; font-weight: bold; color: #64748b;">VS</span>
                <img src="{logo_b}" style="width: 70px; height: 70px; object-fit: contain;">
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown('<div class="section-title">Key Differences</div>', unsafe_allow_html=True)


    rows_html = []
    for label, key, higher_is_better in COMPARISON_METRICS:
        value_a = comparison_value(team_a, key)
        value_b = comparison_value(team_b, key)
        a_wins = value_a > value_b if higher_is_better else value_a < value_b
        b_wins = value_b > value_a if higher_is_better else value_b < value_a
        rows_html.append(
            f"""
            <div class="matchup-row">
                <div class="matchup-value {'win' if a_wins else ''}">{value_a}</div>
                <div class="matchup-name">{label}</div>
                <div class="matchup-value {'win' if b_wins else ''}">{value_b}</div>
            </div>
            """
        )


    matchup_html = f"""
        <div class="matchup-card">
            <div class="matchup-row">
                <div class="matchup-name">{team_a["team_name"]}</div>
                <div></div>
                <div class="matchup-name">{team_b["team_name"]}</div>
            </div>
            {''.join(rows_html)}
        </div>
    """


    col_left, col_right = st.columns([1, 1.15])
    with col_left:
        st.html(matchup_html)
    with col_right:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(comparison_radar_chart(team_a, team_b), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(comparison_per_match_chart(team_a, team_b), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


    col_ppda, col_elo = st.columns(2)
    with col_ppda:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(comparison_ppda_chart(team_a, team_b), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col_elo:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(elo_comparison_chart(team_a, team_b), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)



def render_empty_state() -> None:
    st.markdown(
        """
        <div class="empty-panel">
            <h2>Select a season and team</h2>
            <p>
                The dashboard will load points, record, goals, Elo, xG, PPDA,
                deep completions, and discipline stats from your FastAPI backend.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )



if "selected_season" not in st.session_state:
    st.session_state.selected_season = None


if "selected_team" not in st.session_state:
    st.session_state.selected_team = None


if "compare_team_a" not in st.session_state:
    st.session_state.compare_team_a = None


if "compare_team_b" not in st.session_state:
    st.session_state.compare_team_b = None



with st.sidebar:
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap: 14px; margin-bottom: 12px;">
           <img src="https://a.espncdn.com/i/leaguelogos/soccer/500/12.png" width="38" style="object-fit:contain;">
           <h1 style="margin:0; padding:0; font-size: 1.8rem; line-height:1.1;">Serie A<br>Analytics</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Historical Serie A analytics")
    st.markdown(
        """
        <div class="sidebar-card">
            <p>Pick a completed season, choose a club, and explore its engineered match profile.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


    api_base_url = DEFAULT_API_BASE_URL


    try:
        seasons = load_seasons(api_base_url)
        st.success("API connected")
    except requests.RequestException:
        seasons = []
        st.error("FastAPI backend is not reachable.")
        st.caption("Run: uvicorn backend.app.main:app --reload")


    selected_mode = st.radio(
        "View",
        ["Dashboard", "Compare Teams"],
        horizontal=True,
        key="sidebar_view_mode",
    )
    selected_season = None
    selected_team = None
    compare_team_a = None
    compare_team_b = None


    if seasons:
        season_labels = {format_season(season): season for season in seasons}
        season_values = list(season_labels.values())
        if st.session_state.selected_season not in season_values:
            st.session_state.selected_season = season_values[-1]


        selected_season_index = season_values.index(st.session_state.selected_season)
        season_label = "Season" if selected_mode == "Dashboard" else "Comparison Season"
        selected_season_label = st.selectbox(
            season_label,
            list(season_labels.keys()),
            index=selected_season_index,
            key="season_selectbox",
        )
        selected_season = season_labels[selected_season_label]
        st.session_state.selected_season = selected_season


    teams = []
    if selected_season is not None:
        try:
            teams = load_teams(api_base_url, selected_season)
        except requests.RequestException:
            st.error("Teams could not be loaded.")


    if teams:
        if selected_mode == "Dashboard":
            if st.session_state.selected_team not in teams:
                st.session_state.selected_team = teams[0]


            selected_team_index = teams.index(st.session_state.selected_team)
            selected_team = st.selectbox(
                "Team",
                teams,
                index=selected_team_index,
                key="team_selectbox",
            )
            st.session_state.selected_team = selected_team


        else:
            st.markdown("#### Team vs Team")
            if st.session_state.compare_team_a not in teams:
                st.session_state.compare_team_a = teams[0]


            available_team_b_default = teams[1] if len(teams) > 1 else teams[0]
            if st.session_state.compare_team_b not in teams or st.session_state.compare_team_b == st.session_state.compare_team_a:
                st.session_state.compare_team_b = available_team_b_default


            team_a_index = teams.index(st.session_state.compare_team_a)
            compare_team_a = st.selectbox(
                "Team A",
                teams,
                index=team_a_index,
                key="compare_team_a_selectbox",
            )
            st.session_state.compare_team_a = compare_team_a


            team_b_options = [team for team in teams if team != compare_team_a]
            if st.session_state.compare_team_b not in team_b_options:
                st.session_state.compare_team_b = team_b_options[0] if team_b_options else None


            if team_b_options:
                team_b_index = team_b_options.index(st.session_state.compare_team_b)
                compare_team_b = st.selectbox(
                    "Team B",
                    team_b_options,
                    index=team_b_index,
                    key="compare_team_b_selectbox",
                )
                st.session_state.compare_team_b = compare_team_b


    st.divider()
    st.caption("Current version uses historical completed seasons only.")



st.markdown(
    """
    <div style="margin-bottom: 24px; display: flex; align-items: center; gap: 18px;">
        <img src="https://a.espncdn.com/i/leaguelogos/soccer/500/12.png" style="height: 68px; object-fit: contain; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));">
        <div>
            <p style="margin: 0 0 6px; color: #2563eb; font-weight: 900; letter-spacing: 0.08em; text-transform: uppercase;">
                Serie A Analytics
            </p>
            <h1 style="margin: 0; line-height: 0.95; letter-spacing: 0;">
                Team Season Intelligence
            </h1>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)



if selected_mode == "Compare Teams":
    if selected_season is None or compare_team_a is None or compare_team_b is None:
        render_empty_state()
    else:
        try:
            team_a_summary = load_summary(api_base_url, selected_season, compare_team_a)
            team_b_summary = load_summary(api_base_url, selected_season, compare_team_b)
            render_comparison(team_a_summary, team_b_summary)
        except requests.RequestException as exc:
            st.error("Team comparison could not be loaded.")
            st.code(str(exc))
else:
    if selected_season is None or selected_team is None:
        render_empty_state()
    else:
        try:
            summary = load_summary(api_base_url, selected_season, selected_team)
            all_summaries = load_all_summaries(api_base_url, selected_season, teams)
            standings = load_standings(api_base_url, selected_season)
            
            if str(selected_season) == "2223":
                for row in standings:
                    if row["team_name"] == "Juventus":
                        row["total_points"] = 62
                standings.sort(key=lambda x: (x["total_points"], x["goal_difference"], x["goals_scored"]), reverse=True)

            main_col, standings_col = st.columns([2.2, 1])
            with main_col:
                render_summary(summary, all_summaries)
            with standings_col:
                st.markdown("<div style='height: 220px'></div>", unsafe_allow_html=True)
                render_standings(standings, selected_team, int(selected_season))

        except requests.RequestException as exc:
            st.error("Team summary could not be loaded.")
            st.code(str(exc))