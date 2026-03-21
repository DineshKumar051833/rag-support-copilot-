import { useState } from "react";

const BASE_URL = "";
    
export default function App() {
  // ---------------- AUTH ----------------
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [message, setMessage] = useState("");

  // ---------------- TASK 1 ----------------
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");

  // ---------------- TASK 2 ----------------
  const [requirement, setRequirement] = useState("");
  const [specOutput, setSpecOutput] = useState("");

  // ---------------- LOGIN ----------------
  const handleLogin = async () => {
    try {
      const res = await fetch(`${BASE_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ username, password })
      });

      const data = await res.json();

      if (data.success) {
        setIsLoggedIn(true);
        setMessage("Login successful");
      } else {
        setMessage(data.message);
      }
    } catch {
      setMessage("Login failed");
    }
  };

  // ---------------- SIGNUP ----------------
  const handleSignup = async () => {
    try {
      const res = await fetch(`${BASE_URL}/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ username, password })
      });

      const data = await res.json();
      setMessage(data.message);
    } catch {
      setMessage("Signup failed");
    }
  };

  // ---------------- LOGOUT ----------------
  const handleLogout = async () => {
    try {
      await fetch(`${BASE_URL}/logout`, {
        method: "POST",
        credentials: "include"
      });

      setIsLoggedIn(false);
      setUsername("");
      setPassword("");
      setQuery("");
      setAnswer("");
      setRequirement("");
      setSpecOutput("");
      setMessage("Logged out successfully");
    } catch {
      setMessage("Logout failed");
    }
  };

  // ---------------- TASK 1: ASK ----------------
  const handleAsk = async () => {
    try {
      const res = await fetch(`${BASE_URL}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ query })
      });

      const data = await res.json();

      if (data.error) {
        setAnswer(data.error);
      } else {
        setAnswer(data.answer);
      }
    } catch {
      setAnswer("Error fetching answer");
    }
  };

  // ---------------- TASK 2: GENERATE SPECS ----------------
  const handleGenerateSpecs = async () => {
    try {
      const res = await fetch(`${BASE_URL}/generate-specs`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ requirement })
      });

      const data = await res.json();

      setSpecOutput(data.output || JSON.stringify(data, null, 2));
    } catch {
      setSpecOutput("Error generating specs");
    }
  };

  return (
    <div style={styles.container}>
      <h2>GenAI Support Copilot</h2>

      {/* ---------------- AUTH ---------------- */}
      {!isLoggedIn && (
        <>
          <input
            style={styles.input}
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />

          <input
            style={styles.input}
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <div>
            <button style={styles.button} onClick={handleLogin}>
              Login
            </button>

            <button style={styles.button} onClick={handleSignup}>
              Signup
            </button>
          </div>

          <p>{message}</p>
        </>
      )}

      {/* ---------------- MAIN APP ---------------- */}
      {isLoggedIn && (
        <>
          <button style={styles.logoutButton} onClick={handleLogout}>
            Logout
          </button>

          {/* ---------------- TASK 1 ---------------- */}
          <h3>Task 1: Ask Question (RAG)</h3>

          <input
            style={styles.input}
            placeholder="Ask your question..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />

          <button style={styles.button} onClick={handleAsk}>
            Ask
          </button>

          <p style={styles.answer}>{answer}</p>

          {/* ---------------- TASK 2 ---------------- */}
          <hr style={{ margin: "30px 0" }} />

          <h3>Task 2: Generate Software Specs</h3>

          <textarea
            style={styles.textarea}
            placeholder="Enter requirement..."
            value={requirement}
            onChange={(e) => setRequirement(e.target.value)}
          />

          <br />

          <button style={styles.button} onClick={handleGenerateSpecs}>
            Generate Specs
          </button>

          <pre style={styles.output}>{specOutput}</pre>
        </>
      )}
    </div>
  );
}

// ---------------- STYLES ----------------
const styles = {
  container: {
    textAlign: "center",
    marginTop: "50px"
  },
  input: {
    display: "block",
    margin: "10px auto",
    padding: "10px",
    width: "300px"
  },
  textarea: {
    width: "400px",
    height: "120px",
    padding: "10px"
  },
  button: {
    margin: "5px",
    padding: "10px 20px",
    cursor: "pointer"
  },
  logoutButton: {
    marginBottom: "20px",
    padding: "8px 16px",
    backgroundColor: "#ff4d4d",
    color: "white",
    border: "none",
    cursor: "pointer"
  },
  answer: {
    marginTop: "20px",
    fontWeight: "bold"
  },
  output: {
    marginTop: "20px",
    textAlign: "left",
    backgroundColor: "#222",
    color: "#0f0",
    padding: "15px",
    whiteSpace: "pre-wrap",
    width: "400px",
    marginLeft: "auto",
    marginRight: "auto"
  }
};