import { useEffect, useState } from "react";
import { getBackendHealth } from "./services/api";

function App() {
  const [backendStatus, setBackendStatus] = useState("Checking...");

  useEffect(() => {
    async function checkBackend() {
      try {
        const data = await getBackendHealth();
        setBackendStatus(data.status);
      } catch (error) {
        console.error("Backend connection failed:", error);
        setBackendStatus("offline");
      }
    }

    checkBackend();
  }, []);

  return (
    <main>
      <h1>AI Interview Platform</h1>

      <h2>System Status</h2>

      <p>Frontend: Online</p>
      <p>Backend: {backendStatus}</p>
    </main>
  );
}

export default App;