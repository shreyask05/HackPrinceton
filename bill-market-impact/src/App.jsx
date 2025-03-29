import './App.css';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import BillCard from './components/BillCard';


function Home() {
  const sampleBills = [
    {
      title: "Renewable Energy Incentive Act",
      summary: "Provides tax incentives for renewable energy companies.",
      sector: "Energy",
      sentiment: "Positive",
      impact: "High"
    },
    {
      title: "Big Tech Regulation Act",
      summary: "Introduces stricter regulations on tech monopolies.",
      sector: "Technology",
      sentiment: "Negative",
      impact: "Medium"
    },
    {
      title: "Healthcare Affordability Act",
      summary: "Expands access to affordable healthcare services.",
      sector: "Healthcare",
      sentiment: "Positive",
      impact: "Low"
    }
  ];

  return (
    <main className="main-content">
      <section className="hero">
        <h2>Track Upcoming Bills & Their Market Impact</h2>
        <p>Get real-time predictions on how new bills could impact the stock market.</p>
        <button className="cta-button">Explore Bills</button>
      </section>

      <section className="features">
        {sampleBills.map((bill, index) => (
          <BillCard
            key={index}
            title={bill.title}
            summary={bill.summary}
            sector={bill.sector}
            sentiment={bill.sentiment}
            impact={bill.impact}
          />
        ))}
      </section>
    </main>
  );
}

function Sectors() {
  return (
    <main className="main-content">
      <h2>Sector Impact Analysis</h2>
      <p>Sector-wise predicted impact will appear here soon.</p>
    </main>
  );
}

function About() {
  return (
    <main className="main-content">
      <h2>About This Project</h2>
      <p>We aim to help investors anticipate stock market changes from upcoming bills.</p>
    </main>
  );
}

function App() {
  return (
    <Router>
      <div className="app">
        <header className="header">
          <h1>Bill Market Impact Tracker</h1>
          <nav className="nav-links">
            <Link to="/">Home</Link>
            <Link to="/sectors">Sectors</Link>
            <Link to="/about">About</Link>
          </nav>
        </header>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/sectors" element={<Sectors />} />
          <Route path="/about" element={<About />} />
        </Routes>

        <footer className="footer">
          <p>© 2025 Bill Market Tracker</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
