"use client";

import { useState } from "react";

type Question = {
  field: string;
  question: string;
  priority: string;
  reason?: string;
};

type Props = {
  questions: Question[];
  onComplete: (answers: Record<string, string>) => void;
};

export default function FollowUpInterview({ questions, onComplete }: Props) {
  const [index, setIndex] = useState(0);
  const [answer, setAnswer] = useState("");
  const [answers, setAnswers] = useState<Record<string, string>>({});

  if (!questions.length) return null;

  const current = questions[index];
  const isLast = index === questions.length - 1;

  function next() {
    const trimmed = answer.trim();
    if (!trimmed) return;

    const nextAnswers = {
      ...answers,
      [current.field]: trimmed,
    };

    if (isLast) {
      onComplete(nextAnswers);
      return;
    }

    setAnswers(nextAnswers);
    setIndex((currentIndex) => currentIndex + 1);
    setAnswer("");
  }

  return (
    <section className="card" aria-labelledby="follow-up-title">
      <div className="card-header">
        <h2 id="follow-up-title">Additional information</h2>
        <p>
          Question {index + 1} of {questions.length}
          {current.priority ? ` · ${current.priority} priority` : ""}
        </p>
      </div>
      <div className="form-body">
        <p style={{ marginTop: 0, fontWeight: 700 }}>{current.question}</p>
        {current.reason && <p className="field-hint">{current.reason}</p>}
        <div className="field">
          <label htmlFor="follow-up-answer">Answer</label>
          <input
            id="follow-up-answer"
            value={answer}
            onChange={(event) => setAnswer(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter") next();
            }}
            autoFocus
          />
        </div>
        <div className="form-actions">
          <span className="field-hint">Answer before continuing.</span>
          <button className="primary-button" type="button" onClick={next} disabled={!answer.trim()}>
            {isLast ? "Complete" : "Next"}
          </button>
        </div>
      </div>
    </section>
  );
}
