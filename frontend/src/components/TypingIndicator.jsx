export default function TypingIndicator() {
  return (
    <article className="message message-bot">
      <div className="bot-avatar">
        <span>C</span>
      </div>

      <div className="bubble bubble-bot typing-bubble">
        <span className="typing-dot" />
        <span className="typing-dot" />
        <span className="typing-dot" />
        <span className="typing-label">College-AI is thinking</span>
      </div>
    </article>
  );
}
