import { useState } from "react";
import "./CampusRandomizer.css";
const places = [
  {
    name: "Central Library",
    icon: "📚",
    category: "Study",
    location: "Aadmin Block",
    bestFor: "Quiet study and research",
    suitableFor: "Individual study",
    tip: "A good choice when you need a distraction-free environment.",
  },
  {
    name: "Migloo",
    icon: "☕",
    category: "Food",
    location: "Near Huts",
    bestFor: "Food and casual breaks",
    suitableFor: "Friends / Groups",
    tip: "want to skip mess try migloo.",
  },
  {
    name: "Sports Ground",
    icon: "⚽",
    category: "Sports",
    location: "Campus Grounds",
    bestFor: "Outdoor activities",
    suitableFor: "Friends / Teams",
    tip: "Ideal for a short evening activity.",
  },
  {
    name: "Hostel Common Area",
    icon: "🛋️",
    category: "Relax",
    location: "Hostel",
    bestFor: "Relaxing and socializing",
    suitableFor: "Friends / Groups",
    tip: "A convenient place to unwind after classes.",
  },
  {
    name: "Computer Lab",
    icon: "💻",
    category: "Study",
    location: "Academic Block",
    bestFor: "Programming and projects",
    suitableFor: "Individual / Group",
    tip: "Useful when you need access to campus computing facilities.",
  },
  {
    name: "Millet",
    icon: "☕",
    category: "Food & Snacks",
    loaction: "Near Mess",
    bestFor: "Food and casual breaks",
    suitableFor: "Friends / Individual",
    tip: "Good spot for a quick break between classes"
  },
];

export default function CampusRandomizer() {
  const [place, setPlace] = useState(null);

  function discoverPlace() {
    const randomIndex = Math.floor(Math.random() * places.length);
    setPlace(places[randomIndex]);
  }

  return (
    <section className="campus-randomizer">
      <div className="randomizer-header">
        <span className="randomizer-label">CAMPUS DISCOVERY</span>

        <h2>Where should you explore today?</h2>

        <p>
          Discover a random campus location based on your mood,
          schedule or free time.
        </p>
      </div>

      {!place ? (
        <div className="randomizer-empty">
          <div className="randomizer-symbol">✦</div>

          <span>Ready to explore?</span>

          <button onClick={discoverPlace}>
            Discover a place
            <span>↗</span>
          </button>
        </div>
      ) : (
        <div className="random-place">
          <div className="place-icon">
            {place.icon}
          </div>

          <div className="place-main">
            <span className="place-category">
              {place.category}
            </span>

            <h3>{place.name}</h3>

            <p className="place-location">
              📍 {place.location}
            </p>

            <div className="place-details">
              <div>
                <span>BEST FOR</span>
                <strong>{place.bestFor}</strong>
              </div>

              <div>
                <span>SUITABLE FOR</span>
                <strong>{place.suitableFor}</strong>
              </div>
            </div>

            <div className="place-tip">
              <span>💡</span>
              {place.tip}
            </div>
          </div>

          <button
            className="discover-again"
            onClick={discoverPlace}
            aria-label="Discover another place"
          >
            ↻
          </button>
        </div>
      )}
    </section>
  );
}