import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import AboutPage from "./pages/About";
import ExploreBills from "./pages/ExploreBills";
import BillDetail from "./pages/BillDetail";
import Layout from "./components/Layout";

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/explore" element={<ExploreBills />} />
          <Route path="/bill/:id" element={<BillDetail />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
