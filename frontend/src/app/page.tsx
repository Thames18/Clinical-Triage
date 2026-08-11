import PatientForm from "@/components/PatientForm";

export default function Home() {
  return (
    <main className="app-shell">
      <header className="site-header">
        <div className="brand">
          <div className="brand-mark" aria-hidden="true">CT</div>
          <div>
            <p className="brand-name">ClinicalTriage AI</p>
            <p className="brand-subtitle">Safety-first clinical assessment assistant</p>
          </div>
        </div>
        <div className="header-badge">
          <span className="status-dot" aria-hidden="true" />
          Decision support
        </div>
      </header>

      <section className="hero">
        <div>
          <p className="eyebrow">CLINICAL DECISION SUPPORT</p>
          <h1>Assess a patient with clarity and confidence.</h1>
          <p className="hero-copy">
            Enter the available patient information below. Deterministic safety
            checks run before evidence-grounded AI reasoning and are displayed
            alongside the final assessment.
          </p>
        </div>
        <aside className="safety-note">
          <span className="safety-icon" aria-hidden="true">!</span>
          <div>
            <strong>Safety notice</strong>
            <p>
              This application is a decision-support prototype and does not replace a qualified clinician or emergency services.
            </p>
          </div>
        </aside>
      </section>

      <PatientForm />

      <footer className="site-footer">
        <span>ClinicalTriage AI</span>
        <span>For research and educational decision support only.</span>
      </footer>
    </main>
  );
}
