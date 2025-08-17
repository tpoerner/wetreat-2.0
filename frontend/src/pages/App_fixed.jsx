import React, { useState } from "react";
import logo from "../assets/wt_logonew_whitecanvas.png";

function App() {
  const [role, setRole] = useState("patient");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = () => {
    alert("Logging in as " + role + " with email: " + email);
    // TODO: Implement actual login call to backend
  };

  return (
    <div style={{ textAlign: "center", paddingTop: "4rem" }}>
      <img src={logo} alt="WeTreat Logo" style={{ width: "180px", marginBottom: "2rem" }} />
      <h1 style={{ fontSize: "1.5rem", marginBottom: "1rem" }}>Welcome to WeTreat</h1>
      <select value={role} onChange={(e) => setRole(e.target.value)} style={{ padding: "0.5rem", marginBottom: "1rem" }}>
        <option value="admin">Admin</option>
        <option value="patient">Patient Input</option>
        <option value="physician">Consulting Physician</option>
      </select>
      <br />
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        style={{ padding: "0.5rem", marginBottom: "0.5rem", width: "200px" }}
      />
      <br />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        style={{ padding: "0.5rem", marginBottom: "1rem", width: "200px" }}
      />
      <br />
      <button onClick={handleLogin} style={{ padding: "0.5rem 1rem" }}>Login</button>
    </div>
  );
}

export default App;
