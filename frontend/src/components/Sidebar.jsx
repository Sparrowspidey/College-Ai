const menuItems = [
  { icon: "⌂", label: "Home" },
  { icon: "◫", label: "Academics" },
  { icon: "◷", label: "Timetable" },
  { icon: "▣", label: "Notices" },
  { icon: "◎", label: "Campus" },
];

export default function Sidebar({ open, onClose, onNewChat, hasMessages }) {
  return (
    <>
      <div
        className={`sidebar-overlay ${open ? "visible" : ""}`}
        onClick={onClose}
      />

      <aside className={`sidebar ${open ? "open" : ""}`}>
        <div className="sidebar-top">
          <div className="sidebar-brand">
            <div className="mini-logo">C</div>
            <div>
              <strong>College-AI</strong>
              <span>IIIT Kottayam</span>
            </div>
          </div>

          <button className="close-sidebar" onClick={onClose} aria-label="Close menu">
            ×
          </button>
        </div>

        <button className="new-chat-btn" onClick={onNewChat}>
          <span>＋</span>
          New chat
        </button>

        <div className="sidebar-section">
          <span className="sidebar-label">Explore</span>

          {menuItems.map((item) => (
            <button className="side-item" key={item.label} onClick={onClose}>
              <span className="side-icon">{item.icon}</span>
              {item.label}
            </button>
          ))}
        </div>

        <div className="sidebar-section">
          <span className="sidebar-label">Your chat</span>

          {hasMessages ? (
            <button className="side-item active-chat">
              <span className="side-icon">✦</span>
              Current conversation
            </button>
          ) : (
            <p className="no-chats">Your conversations will appear here.</p>
          )}
        </div>

        <div className="sidebar-footer">
          <div className="sidebar-footer-card">
            <span className="footer-glow" />
            <strong>Built by Sparrowspidey & Team</strong>
            <span>College-AI · IIIT Kottayam </span>
          </div>
        </div>
      </aside>
    </>
  );
}
