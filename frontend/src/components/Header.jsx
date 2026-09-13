export default function Header({ apiStatus, onMenu }) {
  const statusText =
    apiStatus === "ok"
      ? "College-AI online"
      : apiStatus === "checking"
      ? "Connecting..."
      : "Backend offline";

  return (
    <header className="header">
      <div className="header-left">
        <button className="mobile-menu" onClick={onMenu} aria-label="Open menu">
          <span />
          <span />
          <span />
        </button>

        <div className="brand-mark">
          <span className="brand-dot" />
          <span className="brand-ring" />
        </div>

        <div className="brand-copy">
          <div className="brand-title">
            College<span>-AI</span>
          </div>
          <div className="brand-subtitle">IIIT Kottayam</div>
        </div>
      </div>

      <div className={`status-pill status-${apiStatus}`}>
        <span className="status-dot" />
        <span>{statusText}</span>
      </div>
    </header>
  );
}
