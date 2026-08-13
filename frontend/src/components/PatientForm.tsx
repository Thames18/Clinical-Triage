"use client";

import { FormEvent, /*useEffect ,*/ useMemo, useState } from "react";
import {
  Activity,
  AlertTriangle,
  CheckCircle2,
  ClipboardList,
  LogOut,
  ShieldCheck,
} from "lucide-react";
import {api} from "@/lib/api";
 /*import { api, getStoredToken, login, clearStoredToken } from "@/lib/api";  */

type TriageResult = {
  assessment_id?: string;
  created_at?: string | null;
  triage_level: string;
  summary: string;
  red_flags: Array<{
    code: string;
    severity: string;
    title: string;
    explanation: string;
    evidence: string;
  }>;
  recommendations: string[];
  missing_information: Array<{
    field: string;
    reason: string;
    priority: string;
  }>;
  follow_up_questions: Array<{
    field: string;
    question: string;
    priority: string;
    reason?: string;
  }>;
  confidence: number;
  risk_score: number;
  ai_assisted?: boolean;
  evidence_citations?: Array<{
    citation_id: string;
    source_id: string;
    chunk_id: string;
    claim: string;
    supporting_text: string;
    url: string;
  }>;
  evidence_corpus_version?: string | null;
  model_name?: string | null;
  model_version?: string | null;
  prompt_version?: string | null;
  validation_issues?: string[];
};

type PatientPayload = {
  age: number;
  sex: "male" | "female";
  temperature_c: number | null;
  heart_rate: number | null;
  respiratory_rate: number | null;
  systolic_bp: number | null;
  diastolic_bp: number | null;
  oxygen_saturation: number | null;
  consciousness: "alert" | "confused" | "drowsy" | "unresponsive" | "unknown";
  symptoms: string[];
  symptom_duration_hours: number | null;
  medical_history: string[];
  medications: string[];
  allergies: string[];
};

const initialForm = {
  age: "",
  sex: "female",
  temperature: "",
  heart_rate: "",
  respiratory_rate: "",
  systolic_bp: "",
  diastolic_bp: "",
  oxygen_saturation: "",
  consciousness: "unknown",
  symptoms: "",
  duration: "",
};

function toNumber(value: string): number | null {
  if (!value.trim()) return null;
  const number = Number(value);
  return Number.isFinite(number) ? number : null;
}

function levelClass(level: string) {
  return level.toLowerCase().replaceAll("_", "-");
}

export default function PatientForm() {
/*  const [token, setToken] = useState<string | null>(null);*/
  const [form, setForm] = useState(initialForm);
/*  const [loginState, setLoginState] = useState({ username: "", password: "" }); */
/*  const [loginLoading, setLoginLoading] = useState(false); */
/*  const [loginError, setLoginError] = useState(""); */
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<TriageResult | null>(null);

/*  useEffect(() => {
     setToken(getStoredToken()); 
  }, []);*/

  const hasResult = Boolean(result);
  const confidence = useMemo(
    () => (result ? Math.round(result.confidence * 100) : 0),
    [result],
  );

  function updateField(name: keyof typeof initialForm, value: string) {
    setForm((current) => ({ ...current, [name]: value }));
  }

/*  async function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoginLoading(true);
    setLoginError("");

    try {
      const accessToken = await login(loginState.username, loginState.password);
      setToken(accessToken);
    } catch {
      setLoginError("Login failed. Check the configured credentials and try again.");
    } finally {
      setLoginLoading(false);
    }
  }

  function logout() {
    clearStoredToken();
    setToken(null);
    setResult(null);
  } */

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    const symptoms = form.symptoms
      .split(",")
      .map((symptom) => symptom.trim())
      .filter(Boolean);

    if (!symptoms.length) {
      setError("Enter at least one symptom.");
      setLoading(false);
      return;
    }

    const systolic = toNumber(form.systolic_bp);
    const diastolic = toNumber(form.diastolic_bp);

    if (systolic !== null && diastolic !== null && systolic < diastolic) {
      setError("Systolic blood pressure must be greater than diastolic blood pressure.");
      setLoading(false);
      return;
    }

    const payload: PatientPayload = {
      age: Number(form.age),
      sex: form.sex as PatientPayload["sex"],
      temperature_c: toNumber(form.temperature),
      heart_rate: toNumber(form.heart_rate),
      respiratory_rate: toNumber(form.respiratory_rate),
      systolic_bp: systolic,
      diastolic_bp: diastolic,
      oxygen_saturation: toNumber(form.oxygen_saturation),
      consciousness: form.consciousness as PatientPayload["consciousness"],
      symptoms,
      symptom_duration_hours: toNumber(form.duration),
      medical_history: [],
      medications: [],
      allergies: [],
    };

    try {
 /* no longer needed      const response = await api.post<TriageResult>("/triage", payload, {
        headers: { Authorization: `Bearer ${token}` },
      });*/
      const response = await api.post<TriageResult>(
          "/triage",  payload );
      setResult(response.data);
    } catch (err) {
      const status =
        typeof err === "object" && err !== null && "response" in err
          ? (err as { response?: { status?: number } }).response?.status
          : undefined;

/* 401 error no longer needed     if (status === 401) {
        clearStoredToken();
        setToken(null);
        setError("Your session expired. Please sign in again.");
      } else {
        setError(
          "The assessment could not be completed. Check the API connection and try again.",
        );
      }*/
      setError(
        "The assessment could not be completed. Check the API connection and try again.",
      );
    } finally {
      setLoading(false);
    }
  }

  /* Secure access temporarily disabled — login/sign-in gate commented out.
  if (!token) {
    return (
      <section className="card login-card">
        <div className="card-header">
          <h2>Sign in to ClinicalTriage AI</h2>
          <p>Authenticated access is required before submitting a patient assessment.</p>
        </div>
        <div className="login-body">
          <form className="login-form" onSubmit={handleLogin}>
            <label className="login-label">
              Username
              <input
                className="login-input"
                value={loginState.username}
                onChange={(event) =>
                  setLoginState((current) => ({
                    ...current,
                    username: event.target.value,
                  }))
                }
                autoComplete="username"
                required
              />
            </label>
            <label className="login-label">
              Password
              <input
                className="login-input"
                type="password"
                value={loginState.password}
                onChange={(event) =>
                  setLoginState((current) => ({
                    ...current,
                    password: event.target.value,
                  }))
                }
                autoComplete="current-password"
                required
              />
            </label>
            {loginError && <div className="login-error">{loginError}</div>}
            <button className="primary-button" type="submit" disabled={loginLoading}>
              {loginLoading ? "Signing in…" : "Sign in"}
            </button>
          </form>
        </div>
      </section>
    );
  }
  */

  return (
    <div className="dashboard-grid">
      <section className="card">
        <div className="card-header">
          <div>
              <h2>Patient assessment</h2>
              <p>Provide the information currently available. Optional vitals can be left blank.</p>
            </div>
        </div>

        <form className="form-body" onSubmit={submit}>
          <p className="section-label">Patient</p>
          <div className="field-grid">
            <div className="field">
              <label htmlFor="age">Age</label>
              <input
                id="age"
                type="number"
                min="0"
                max="130"
                value={form.age}
                onChange={(event) => updateField("age", event.target.value)}
                required
              />
            </div>
            <div className="field">
              <label htmlFor="sex">Sex</label>
              <select
                id="sex"
                value={form.sex}
                onChange={(event) => updateField("sex", event.target.value)}
              >
                <option value="female">Female</option>
                <option value="male">Male</option>
              </select>
            </div>
          </div>

          <div style={{ height: 24 }} />

          <p className="section-label">Vital signs</p>
          <div className="field-grid three">
            <div className="field">
              <label htmlFor="temperature">Temperature</label>
              <input
                id="temperature"
                type="number"
                step="0.1"
                min="25"
                max="45"
                placeholder="°C"
                value={form.temperature}
                onChange={(event) => updateField("temperature", event.target.value)}
              />
            </div>
            <div className="field">
              <label htmlFor="heart_rate">Heart rate</label>
              <input
                id="heart_rate"
                type="number"
                min="20"
                max="250"
                placeholder="bpm"
                value={form.heart_rate}
                onChange={(event) => updateField("heart_rate", event.target.value)}
              />
            </div>
            <div className="field">
              <label htmlFor="respiratory_rate">Respiratory rate</label>
              <input
                id="respiratory_rate"
                type="number"
                min="4"
                max="80"
                placeholder="breaths/min"
                value={form.respiratory_rate}
                onChange={(event) => updateField("respiratory_rate", event.target.value)}
              />
            </div>
            <div className="field">
              <label htmlFor="systolic_bp">Systolic BP</label>
              <input
                id="systolic_bp"
                type="number"
                min="40"
                max="260"
                placeholder="mmHg"
                value={form.systolic_bp}
                onChange={(event) => updateField("systolic_bp", event.target.value)}
              />
            </div>
            <div className="field">
              <label htmlFor="diastolic_bp">Diastolic BP</label>
              <input
                id="diastolic_bp"
                type="number"
                min="20"
                max="160"
                placeholder="mmHg"
                value={form.diastolic_bp}
                onChange={(event) => updateField("diastolic_bp", event.target.value)}
              />
            </div>
            <div className="field">
              <label htmlFor="oxygen_saturation">Oxygen saturation</label>
              <input
                id="oxygen_saturation"
                type="number"
                min="50"
                max="100"
                step="0.1"
                placeholder="%"
                value={form.oxygen_saturation}
                onChange={(event) => updateField("oxygen_saturation", event.target.value)}
              />
            </div>
          </div>

          <div style={{ height: 24 }} />

          <p className="section-label">Clinical presentation</p>
          <div className="field-grid">
            <div className="field">
              <label htmlFor="consciousness">Level of consciousness</label>
              <select
                id="consciousness"
                value={form.consciousness}
                onChange={(event) => updateField("consciousness", event.target.value)}
              >
                <option value="unknown">Unknown</option>
                <option value="alert">Alert</option>
                <option value="confused">Confused</option>
                <option value="drowsy">Drowsy</option>
                <option value="unresponsive">Unresponsive</option>
              </select>
            </div>
            <div className="field">
              <label htmlFor="duration">Symptom duration</label>
              <input
                id="duration"
                type="number"
                min="0"
                max="8760"
                step="0.5"
                placeholder="hours"
                value={form.duration}
                onChange={(event) => updateField("duration", event.target.value)}
              />
            </div>
            <div className="field full">
              <label htmlFor="symptoms">Symptoms</label>
              <textarea
                id="symptoms"
                placeholder="Example: chest pain, shortness of breath, dizziness"
                value={form.symptoms}
                onChange={(event) => updateField("symptoms", event.target.value)}
                required
              />
              <p className="field-hint">Separate multiple symptoms with commas.</p>
            </div>
          </div>

          {error && (
            <div className="error-card" role="alert">
              <strong>Assessment error</strong>
              <p>{error}</p>
            </div>
          )}

          <div className="form-actions">
            <span className="field-hint">
              Deterministic safety checks run before AI reasoning.
            </span>
            <button className="primary-button" type="submit" disabled={loading}>
              {loading ? "Analyzing…" : "Run assessment"}
            </button>
          </div>
        </form>
      </section>

      <aside className="result-stack">
        {!hasResult && !loading && (
          <section className="card">
            <div className="loading-state">
              <ClipboardList size={26} />
              <span>Assessment results will appear here.</span>
            </div>
          </section>
        )}

        {loading && (
          <section className="card">
            <div className="loading-state" aria-live="polite">
              <div className="spinner" />
              <span>Running safety checks and clinical reasoning…</span>
            </div>
          </section>
        )}

        {result && (
          <section className="card result-card" aria-live="polite">
            <div className={`result-banner ${levelClass(result.triage_level)}`}>
              <div>
                <p className="result-level">{result.triage_level.replaceAll("_", " ")}</p>
                <p className="result-banner-copy">
                  {result.ai_assisted
                    ? "AI-assisted assessment passed the configured safety and evidence validation checks."
                    : "This assessment was produced without relying on an AI recommendation."}
                </p>
              </div>
              <div className="result-score">
                <strong>{result.risk_score}</strong>
                <span>risk score</span>
              </div>
            </div>

            <div className="result-content">
              <p className="summary">{result.summary}</p>

              <div className="metric-grid">
                <div className="metric">
                  <div className="metric-label">Confidence</div>
                  <div className="metric-value">{confidence}%</div>
                </div>
                <div className="metric">
                  <div className="metric-label">Safety engine</div>
                  <div className="metric-value">
                    {result.red_flags.length ? "Flags found" : "No flags"}
                  </div>
                </div>
              </div>

              {result.red_flags.length > 0 && (
                <div className="result-section">
                  <h3>
                    <AlertTriangle size={14} style={{ verticalAlign: "middle", marginRight: 6 }} />
                    Safety findings
                  </h3>
                  <ul className="flag-list">
                    {result.red_flags.map((flag) => (
                      <li className="flag" key={`${flag.code}-${flag.evidence}`}>
                        <div className="flag-title">
                          <span>{flag.title}</span>
                          <span className="severity">{flag.severity}</span>
                        </div>
                        <p>{flag.explanation}</p>
                        <small>{flag.evidence}</small>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {result.recommendations.length > 0 && (
                <div className="result-section">
                  <h3>
                    <ShieldCheck size={14} style={{ verticalAlign: "middle", marginRight: 6 }} />
                    Recommendations
                  </h3>
                  <ul className="recommendation-list">
                    {result.recommendations.map((recommendation, index) => (
                      <li className="recommendation" key={`${recommendation}-${index}`}>
                        <span className="recommendation-number">{index + 1}</span>
                        <span>{recommendation}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {result.follow_up_questions.length > 0 && (
                <div className="result-section">
                  <h3>Additional information</h3>
                  <div className="question-list">
                    {result.follow_up_questions.map((question) => (
                      <div className="question" key={question.field}>
                        {question.question}
                        {question.reason && <small>{question.reason}</small>}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {result.missing_information.length > 0 && (
                <div className="result-section">
                  <h3>Missing information</h3>
                  <ul className="missing-list">
                    {result.missing_information.map((item) => (
                      <li className="missing-item" key={item.field}>
                        <strong>
                          {item.field.replaceAll("_", " ")} · {item.priority}
                        </strong>
                        <p>{item.reason}</p>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {result.evidence_citations && result.evidence_citations.length > 0 && (
                <div className="result-section">
                  <h3>Evidence used</h3>
                  <ul className="citation-list">
                    {result.evidence_citations.map((citation) => (
                      <li className="citation" key={citation.citation_id}>
                        <strong>{citation.claim}</strong>
                        <p>{citation.supporting_text}</p>
                        <a href={citation.url} target="_blank" rel="noreferrer">
                          View source
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {result.validation_issues && result.validation_issues.length > 0 && (
                <div className="validation-warning">
                  <strong>Validation issues</strong>
                  <ul>
                    {result.validation_issues.map((issue) => (
                      <li key={issue}>{issue}</li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="result-section">
                <h3>Assessment metadata</h3>
                <p className="field-hint">
                  {result.assessment_id ? `Assessment ID: ${result.assessment_id}` : ""}
                  {result.model_version ? ` · Model: ${result.model_version}` : ""}
                  {result.prompt_version ? ` · Prompt: ${result.prompt_version}` : ""}
                </p>
              </div>
            </div>
          </section>
        )}

        <section className="card">
          <div className="card-header">
            <h3>Workflow</h3>
            <p>Safety checks are intentionally separated from model reasoning.</p>
          </div>
          <div className="form-body">
            <div className="recommendation">
              <Activity size={16} />
              <span>Validate patient inputs and detect deterministic red flags.</span>
            </div>
            <div className="recommendation">
              <ShieldCheck size={16} />
              <span>Use reviewed evidence before invoking AI reasoning.</span>
            </div>
            <div className="recommendation">
              <CheckCircle2 size={16} />
              <span>Validate AI output and citations before displaying it.</span>
            </div>
          </div>
        </section>
      </aside>
    </div>
  );
}
