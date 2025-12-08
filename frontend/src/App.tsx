import { Link, Route, Routes } from "react-router-dom";
import Home from "./Home";
import Calculations from "./Calculations";

function App() {
  return (
    <div style={{ padding: "1rem", fontFamily: "system-ui, sans-serif" }}>
      <nav style={{ marginBottom: "1rem" }}>
        <Link to="/" style={{ marginRight: "1rem" }}>
          Home
        </Link>
        <Link to="/calculations">Calculations</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/calculations" element={<Calculations />} />
      </Routes>
    </div>
  );
}

export default App;