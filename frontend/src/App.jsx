import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  BarChart3,
  CircleDot,
  Goal,
  Shield,
  Sparkles,
  Trophy,
} from "lucide-react";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

const statGroups = [
  {
    title: "Results",
    accent: "gold",
    items: [
      ["Matches", "matches_played"],
      ["Points", "total_points"],
      ["PPM", "points_per_match"],
      ["Record", "record"],
    ],
  },
  {
    title: "Attack",
    accent: "blue",
    items: [
      ["Goals", "goals_scored"],
      ["Avg Goals", "goals_scored_per_match"],
      ["Total xG", "total_xg"],
      ["Avg xG", "average_xg"],
    ],
  },
  {
    title: "Control",
    accent: "green",
    items: [
      ["Avg Elo", "average_elo_score"],
      ["Avg PPDA", "average_ppda"],
      ["Deep Comp.", "total_deep_completions"],
      ["Deep / Match", "deep_completions_per_match"],
    ],
  },
  {
    title: "Discipline",
    accent: "red",
    items: [
      ["Yellow Cards", "total_yellow_cards"],
      ["Yellow / Match", "yellow_cards_per_match"],
      ["Red Cards", "total_red_cards"],
      ["Red / Match", "red_cards_per_match"],
    ],
  },
];

function formatSeason(season) {
  const value = String(season);
  if (value.length !== 4) return value;
  return `${value.slice(0, 2)}/${value.slice(2)}`;
}

function getValue(summary, key) {
  if (key === "record") {
    return `${summary.wins}-${summary.draws}-${summary.losses}`;
  }

  if (key === "goal_difference") {
    return summary.goal_difference > 0
      ? `+${summary.goal_difference}`
      : summary.goal_difference;
  }

  return summary[key];
}

async function fetchJson(path) {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }
  return response.json();
}

function SelectField({ label, value, onChange, disabled, children }) {
  return (
    <label className="selectField">
      <span>{label}</span>
      <select value={value} onChange={onChange} disabled={disabled}>
        {children}
      </select>
    </label>
  );
}

function BigStat({ icon: Icon, label, value, helper, tone }) {
  return (
    <article className={`bigStat ${tone}`}>
      <div className="statIcon">
        <Icon size={20} />
      </div>
      <p>{label}</p>
      <strong>{value}</strong>
      <span>{helper}</span>
    </article>
  );
}

function StatGroup({ group, summary }) {
  return (
    <section className={`statGroup ${group.accent}`}>
      <div className="groupHeader">
        <CircleDot size={16} />
        <h3>{group.title}</h3>
      </div>
      <div className="miniGrid">
        {group.items.map(([label, key]) => (
          <div className="miniStat" key={key}>
            <span>{label}</span>
            <strong>{getValue(summary, key)}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}

function PitchPanel({ summary }) {
  const goalMax = Math.max(summary.goals_scored, summary.goals_conceded, 1);
  const scoredWidth = Math.round((summary.goals_scored / goalMax) * 100);
  const concededWidth = Math.round((summary.goals_conceded / goalMax) * 100);

  return (
    <section className="pitchPanel">
      <div className="pitchVisual" aria-hidden="true">
        <div className="pitchLine halfway" />
        <div className="pitchCircle" />
        <div className="box left" />
        <div className="box right" />
      </div>

      <div className="pitchStats">
        <div>
          <span>Goals scored</span>
          <strong>{summary.goals_scored}</strong>
          <div className="meter">
            <i style={{ width: `${scoredWidth}%` }} />
          </div>
        </div>
        <div>
          <span>Goals conceded</span>
          <strong>{summary.goals_conceded}</strong>
          <div className="meter muted">
            <i style={{ width: `${concededWidth}%` }} />
          </div>
        </div>
      </div>
    </section>
  );
}

function Dashboard({ summary }) {
  return (
    <div className="dashboard">
      <section className="clubHero">
        <div>
          <p className="eyebrow">Selected Club</p>
          <h2>{summary.team_name}</h2>
          <div className="chips">
            <span>Season {formatSeason(summary.season)}</span>
            <span>{summary.matches_played} matches</span>
            <span>{summary.wins}W {summary.draws}D {summary.losses}L</span>
          </div>
        </div>
        <div className="crestMark">
          {summary.team_name
            .split(" ")
            .map((part) => part[0])
            .join("")
            .slice(0, 3)}
        </div>
      </section>

      <section className="bigStatsGrid">
        <BigStat
          icon={Trophy}
          label="Total Points"
          value={summary.total_points}
          helper={`${summary.points_per_match} per match`}
          tone="gold"
        />
        <BigStat
          icon={Goal}
          label="Goal Difference"
          value={getValue(summary, "goal_difference")}
          helper={`${summary.goals_scored} for, ${summary.goals_conceded} against`}
          tone="blue"
        />
        <BigStat
          icon={Activity}
          label="Average Elo"
          value={summary.average_elo_score}
          helper="Season strength rating"
          tone="green"
        />
        <BigStat
          icon={Shield}
          label="Average PPDA"
          value={summary.average_ppda}
          helper="Pressing intensity signal"
          tone="red"
        />
      </section>

      <PitchPanel summary={summary} />

      <section className="groupsGrid">
        {statGroups.map((group) => (
          <StatGroup group={group} summary={summary} key={group.title} />
        ))}
      </section>
    </div>
  );
}

export default function App() {
  const [seasons, setSeasons] = useState([]);
  const [teams, setTeams] = useState([]);
  const [selectedSeason, setSelectedSeason] = useState("");
  const [selectedTeam, setSelectedTeam] = useState("");
  const [summary, setSummary] = useState(null);
  const [status, setStatus] = useState("loading");
  const [message, setMessage] = useState("Loading seasons...");

  const orderedSeasons = useMemo(
    () => [...seasons].sort((a, b) => Number(a) - Number(b)),
    [seasons],
  );

  useEffect(() => {
    fetchJson("/seasons")
      .then((data) => {
        setSeasons(data.seasons ?? []);
        setStatus("online");
        setMessage("API connected");
      })
      .catch(() => {
        setStatus("offline");
        setMessage("API offline");
      });
  }, []);

  useEffect(() => {
    if (!selectedSeason) {
      setTeams([]);
      setSelectedTeam("");
      setSummary(null);
      return;
    }

    setMessage("Loading teams...");
    fetchJson(`/seasons/${selectedSeason}/teams`)
      .then((data) => {
        setTeams(data.teams ?? []);
        setSelectedTeam("");
        setSummary(null);
        setStatus("online");
        setMessage("Choose a team");
      })
      .catch(() => {
        setTeams([]);
        setStatus("offline");
        setMessage("Teams unavailable");
      });
  }, [selectedSeason]);

  useEffect(() => {
    if (!selectedSeason || !selectedTeam) {
      setSummary(null);
      return;
    }

    setMessage("Loading summary...");
    fetchJson(
      `/seasons/${selectedSeason}/teams/${encodeURIComponent(selectedTeam)}/summary`,
    )
      .then((data) => {
        setSummary(data);
        setStatus("online");
        setMessage("Dashboard ready");
      })
      .catch(() => {
        setSummary(null);
        setStatus("offline");
        setMessage("Summary unavailable");
      });
  }, [selectedSeason, selectedTeam]);

  return (
    <main className="appShell">
      <section className="topBar">
        <div>
          <p className="eyebrow">SeriePredict Lab</p>
          <h1>Serie A Team Intelligence</h1>
          <p className="lede">
            Historical club analytics powered by your cleaned feature dataset.
          </p>
        </div>

        <div className={`statusPill ${status}`}>
          <Sparkles size={16} />
          <span>{message}</span>
        </div>
      </section>

      <section className="controlDeck">
        <SelectField
          label="Season"
          value={selectedSeason}
          onChange={(event) => setSelectedSeason(event.target.value)}
          disabled={status === "offline" && seasons.length === 0}
        >
          <option value="">Select season</option>
          {orderedSeasons.map((season) => (
            <option value={season} key={season}>
              {formatSeason(season)}
            </option>
          ))}
        </SelectField>

        <SelectField
          label="Team"
          value={selectedTeam}
          onChange={(event) => setSelectedTeam(event.target.value)}
          disabled={!selectedSeason || teams.length === 0}
        >
          <option value="">Select team</option>
          {teams.map((team) => (
            <option value={team} key={team}>
              {team}
            </option>
          ))}
        </SelectField>

        <div className="apiBadge">
          <BarChart3 size={18} />
          <span>{API_BASE_URL}</span>
        </div>
      </section>

      {summary ? (
        <Dashboard summary={summary} />
      ) : (
        <section className="emptyPanel">
          <div className="emptyBall" />
          <h2>Pick a season and club</h2>
          <p>The dashboard will fill with points, Elo, xG, PPDA, discipline, and goal profile stats.</p>
        </section>
      )}
    </main>
  );
}
