function formatText(text) {
  if (!text) return null;

  return text.split("\n").map((line, index) => (
    <span key={index}>
      {line}
      {index < text.split("\n").length - 1 && <br />}
    </span>
  ));
}

export default function Message({ msg }) {
  const isUser = msg.role === "user";

  return (
    <article className={`message ${isUser ? "message-user" : "message-bot"}`}>
      {!isUser && (
        <div className="bot-avatar" aria-hidden="true">
          <span>C</span>
        </div>
      )}

      <div className={`message-column ${isUser ? "user-column" : ""}`}>
        <div className={`bubble ${isUser ? "bubble-user" : "bubble-bot"}`}>
          <div className="bubble-text">{formatText(msg.content)}</div>

          {msg.sources?.length > 0 && (
            <div className="sources">
              <div className="sources-heading">
                <span>Knowledge sources</span>
                <span>{msg.sources.length}</span>
              </div>

              <div className="source-list">
                {msg.sources.map((src, index) => (
                  <a
                    key={index}
                    href={src.url || "#"}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="source-item"
                  >
                    <span className="source-file">▤</span>
                    <span className="source-text">
                      {src.source || src.url || "IIIT Kottayam source"}
                    </span>
                    {typeof src.score === "number" && (
                      <span className="source-score">
                        {(src.score * 100).toFixed(0)}%
                      </span>
                    )}
                  </a>
                ))}
              </div>
            </div>
          )}

          {msg.time_taken && (
            <div className="time-taken">Answered in {msg.time_taken}s</div>
          )}
        </div>
      </div>

      {isUser && <div className="user-avatar">You</div>}
    </article>
  );
}
