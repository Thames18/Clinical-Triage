# ClinicalTriageBench

This directory contains synthetic evaluation cases used to test ClinicalTriage.

## Important

These cases are not real patient records.
They are not medical guidelines.
They are test fixtures designed to evaluate software behavior.

## Case structure

Each case contains:
- patient input
- expected triage level
- emergency classification
- expected red flags
- rationale
- tags

## Safety principle

Emergency cases are treated as safety-critical regression tests.
A code change that introduces an emergency false negative must fail the benchmark.

## Expanding the dataset

New cases should include:
1. Clear expected outcome
2. Explicit rationale
3. Relevant clinical scenario
4. Appropriate edge cases
5. Missing-information cases
6. Cases designed to challenge existing rules

Cases should be independently reviewed before being treated as authoritative clinical evaluation data.