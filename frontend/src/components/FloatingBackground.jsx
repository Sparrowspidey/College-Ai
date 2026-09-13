export default function FloatingBackground() {
  return (
    <div className="floating-background" aria-hidden="true">
      <div className="orb orb-one" />
      <div className="orb orb-two" />
      <div className="orb orb-three" />

      <span className="particle particle-one">+</span>
      <span className="particle particle-two">○</span>
      <span className="particle particle-three">✦</span>
      <span className="particle particle-four">·</span>
      <span className="particle particle-five">○</span>
      <span className="particle particle-six">+</span>
    </div>
  );
}
