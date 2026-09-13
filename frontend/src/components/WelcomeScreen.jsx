const suggestions = [
  {
    icon: "🎓",
    title: "Academics",
    text: "Courses, fees & curriculum",
    prompt: "What is the fee structure for B.Tech CSE?",
  },
  {
    icon: "📅",
    title: "Timetable",
    text: "Classes & academic schedule",
    prompt: "What is the timetable for my batch?",
  },
  {
    icon: "📢",
    title: "Admissions",
    text: "Admission & eligibility",
    prompt: "How do I apply for admission at IIIT Kottayam?",
  },
  {
    icon: "🏫",
    title: "Campus",
    text: "Hostel & campus facilities",
    prompt: "What facilities are available in the hostel?",
  },
  {
    icon: "💼",
    title: "Placements",
    text: "Careers & placement data",
    prompt: "Tell me about placements at IIIT Kottayam",
  },
  {
    icon: "👨‍🏫",
    title: "Faculty",
    text: "Faculty & departments",
    prompt: "Who are the faculty members at IIIT Kottayam?",
  },
];

export default function WelcomeScreen({ onSuggestion }) {
  return (
    <section className="welcome">
      <div className="welcome-orbit orbit-a" />
      <div className="welcome-orbit orbit-b" />

      <div className="ai-emblem">
        <div className="emblem-core">C</div>
        <span className="emblem-dot dot-a" />
        <span className="emblem-dot dot-b" />
        <span className="emblem-dot dot-c" />
      </div>

      <div className="welcome-copy">
        <p className="eyebrow">
          <span /> IIIT Kottayam&apos;s AI companion
        </p>

        <h1>
          Your campus,
          <br />
          <span>made searchable.</span>
        </h1>

        <p className="welcome-description">
          Ask College-AI anything about IIIT Kottayam — academics, admissions,
          faculty, campus life, placements and more.
        </p>
      </div>

      <div className="quick-grid">
        {suggestions.map((item) => (
          <button
            className="quick-card"
            key={item.title}
            onClick={() => onSuggestion(item.prompt)}
          >
            <span className="quick-icon">{item.icon}</span>
            <span className="quick-content">
              <strong>{item.title}</strong>
              <small>{item.text}</small>
            </span>
            <span className="quick-arrow">↗</span>
          </button>
        ))}
      </div>
    </section>
  );
}
