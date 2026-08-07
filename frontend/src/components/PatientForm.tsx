"use client"

import { useState } from "react"

type TriageResult = {
  triage_level: string
  summary: string
  red_flags: Array<{
    code: string
    severity: string
    title: string
    explanation: string
    evidence: string
  }>
  recommendations: string[]
  missing_information: Array<{
    field: string
    reason: string
    priority: string
  }>
  follow_up_questions: Array<{
    field: string
    question: string
    priority: string
  }>
  confidence: number
  risk_score: number
}

export default function PatientForm() {
  const [result, setResult] = useState<TriageResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  async function submit(
  event: React.SubmitEvent<HTMLFormElement> ) {
    event.preventDefault()

    const form = event.currentTarget as HTMLFormElement
    const formData = new FormData(form)

    setLoading(true)
    setError("")
    setResult(null)

    const symptoms = String(formData.get("symptoms") || "")
      .split(",")
      .map((symptom) => symptom.trim())
      .filter(Boolean)
    const payload = {
      age: Number(formData.get("age")),
      sex: String(formData.get("sex") || "male"),
      temperature_c: formData.get("temperature")
        ? Number(formData.get("temperature"))
        : null,
      heart_rate: formData.get("heart_rate")
        ? Number(formData.get("heart_rate"))
        : null,
      respiratory_rate: formData.get("respiratory_rate")
        ? Number(formData.get("respiratory_rate"))
        : null,
      systolic_bp: formData.get("systolic_bp")
        ? Number(formData.get("systolic_bp"))
        : null,
      diastolic_bp: formData.get("diastolic_bp")
        ? Number(formData.get("diastolic_bp"))
        : null,
      oxygen_saturation: formData.get("oxygen_saturation")
        ? Number(formData.get("oxygen_saturation"))
        : null,
      consciousness: String(
        formData.get("consciousness") || "unknown"
      ),
      symptoms,
      symptom_duration_hours: formData.get("duration")
        ? Number(formData.get("duration"))
        : null,

      medical_history: [],
      medications: [],
      allergies: [],
    }

    try {
      const response = await fetch("/api/triage", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload),
      })
      if (!response.ok) {
        throw new Error("Unable to complete assessment.")
      }
      const data: TriageResult = await response.json()

      setResult(data)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong."
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <form onSubmit={submit}>
        <h2>Patient Information</h2>
        <input
          name="age"
          type="number"
          min="0"
          max="120"
          placeholder="Age"
          required
        />

        <select name="sex" defaultValue="male">
          <option value="male">Male</option>
          <option value="female">Female</option>
        </select>

        <h2>Vital Signs</h2>
        <input
          name="temperature"
          type="number"
          step="0.1"
          placeholder="Temperature °C"
        />
        <input
          name="heart_rate"
          type="number"
          placeholder="Heart rate"
        />
        <input
          name="respiratory_rate"
          type="number"
          placeholder="Respiratory rate"
        />

        <input
          name="systolic_bp"
          type="number"
          placeholder="Systolic BP"
        />

        <input
          name="diastolic_bp"
          type="number"
          placeholder="Diastolic BP"
        />

        <input
          name="oxygen_saturation"
          type="number"
          min="50"
          max="100"
          placeholder="Oxygen saturation %"
        />

        <select
          name="consciousness"
          defaultValue="unknown"
        >
          <option value="unknown">Unknown</option>
          <option value="alert">Alert</option>
          <option value="confused">Confused</option>
          <option value="drowsy">Drowsy</option>
          <option value="unresponsive">
            Unresponsive
          </option>
        </select>

        <h2>Symptoms</h2>

        <textarea
          name="symptoms"
          placeholder="Example: chest pain, shortness of breath"
          required
        />

        <input
          name="duration"
          type="number"
          min="0"
          placeholder="Symptom duration (hours)"
        />

        <button
          type="submit"
          disabled={loading}
        >
          {loading
            ? "Analyzing..."
            : "Analyze Patient"}
        </button>
      </form>

      {error && (
        <div role="alert">
          <h3>Error</h3>
          <p>{error}</p>
        </div>
      )}

      {result && (
        <section aria-live="polite">
          <h2>{result.triage_level}</h2>

          <p>{result.summary}</p>

          <h3>Risk score</h3>
          <p>{result.risk_score}</p>

          <h3>Confidence</h3>
          <p>
            {Math.round(result.confidence * 100)}%
          </p>

          {result.red_flags.length > 0 && (
            <div>
              <h3>Red Flags</h3>

              {result.red_flags.map((flag) => (
                <div key={flag.code}>
                  <strong>{flag.title}</strong>

                  <p>{flag.explanation}</p>

                  <small>{flag.evidence}</small>
                </div>
              ))}
            </div>
          )}

          {result.follow_up_questions.length > 0 && (
            <div>
              <h3>
                Additional Information Needed
              </h3>

              {result.follow_up_questions.map(
                (question) => (
                  <p key={question.field}>
                    {question.question}
                  </p>
                )
              )}
            </div>
          )}

          <h3>Recommendations</h3>
          <ul>
            {result.recommendations.map(
              (recommendation, index) => (
                <li key={index}>
                  {recommendation}
                </li>
              )
            )}
          </ul>
        </section>
      )}
    </div>
  )
}
