"use client"
import { useState } from "react"

type Question = {
  field: string
  question: string
  priority: string
  reason?: string
}

type Props = {
  questions: Question[]
  onComplete: (
    answers: Record<string, string>
  ) => void
}

export default function FollowUpInterview({
  questions,
  onComplete
}: Props) {

  const [index, setIndex] =
    useState(0)

  const [answer, setAnswer] =
    useState("")

  const current =
    questions[index]

  function next() {
    if (!answer.trim()) {
      return
    }

    const answers = {
      [current.field]: answer
    }


    if (
      index === questions.length - 1
    ) {
      onComplete(answers)
      return
    }

    setIndex(
      index + 1
    )
    setAnswer("")
  }

  return (
    <section>
      <p>
        Question {index + 1} of{" "}
        {questions.length}
      </p>

      <h2> {current.question} </h2>

      {current.reason && (
        <p> {current.reason} </p>
      )}

      <input
        value={answer}
        onChange={
          (event) =>
            setAnswer(
              event.target.value
            )
        }
      />

      <button
        type="button"
        onClick={next}
      >
        {index === questions.length - 1
          ? "Continue"
          : "Next"
        }
      </button>
    </section>
  )
}