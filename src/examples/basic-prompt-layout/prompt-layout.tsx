import React, { useState, useEffect } from "react";
import axios from "axios";

const init = async () => {
  try {
    console.log("init");
    const response = await axios.get("http://52.66.238.200:8080/init");
  } catch (error) {
    console.error(error);
  }
};
init();

const wherebyEmbed = document.createElement("whereby-embed");

const WhisperPage = () => {
  const handleLeave = () => {
    const interval = setInterval(statusCheck, 1000); // Call statusCheck every 1 second
  };

  const [status, setStatus] = useState("");

  useEffect(() => {
    const script = document.createElement("script");
    script.src = "https://cdn.srv.whereby.com/embed/v1.js";
    script.type = "module";

    const style = document.createElement("style");
    style.innerText = "whereby-embed { height: 200px; }";

    wherebyEmbed.setAttribute("minimal", "");
    wherebyEmbed.setAttribute(
      "room",
      "https://etrog.whereby.com/e55a0d5c-2164-4a23-947f-f8299d2b3336?roomKey=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZWV0aW5nSWQiOiI3NTUxOTkxOSIsInJvb21SZWZlcmVuY2UiOnsicm9vbU5hbWUiOiIvZTU1YTBkNWMtMjE2NC00YTIzLTk0N2YtZjgyOTlkMmIzMzM2Iiwib3JnYW5pemF0aW9uSWQiOiIxODQ1MzYifSwiaXNzIjoiaHR0cHM6Ly9hY2NvdW50cy5zcnYud2hlcmVieS5jb20iLCJpYXQiOjE2ODc0MzAyMDYsInJvb21LZXlUeXBlIjoibWVldGluZ0hvc3QifQ.F1WbympD2m2zxEJM8-XIfywxLPCnsa2hqAXj3H0hzS4?timer=on&leaveButton=on"
    );

    const container = document.createElement("div");
    container.appendChild(script);
    container.appendChild(style);
    container.appendChild(wherebyEmbed);

    const embedContainer = document.getElementById("whereby-embed-container");
    if (embedContainer) {
      embedContainer.appendChild(container);
    }
    wherebyEmbed.addEventListener("leave", handleLeave);

    return () => {
      if (embedContainer) {
        embedContainer.innerHTML = "";
      }
      clearInterval(interval);
      wherebyEmbed.removeEventListener("leave", handleLeave);
    };
  }, []);

  const statusCheck = async () => {
    try {
      console.log("status");
      const response = await axios.get(
        "http://52.66.238.200:8080/get_action_items"
      );
      if (response.data.status === "Processing DONE!!") {
        console.log(response.data.action_items);
      }
      setStatus(response.data.status);
    } catch (error) {
      console.error(error);
      setStatus("Error retrieving status");
    }
  };

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        backgroundColor: "#006754",
      }}
    >
      <div
        id="whereby-embed-container"
        style={{
          display: "block",
        }}
      ></div>
      <div
        id="main"
        style={{
          justifyContent: "center",
          alignItems: "center",
          backgroundColor: "#006754",
          width: "100%",
          height: "100%",
        }}
      >
        <p style={{ color: "wheat", display: "block" }}>
          This is status:{status}
        </p>
        <script src="https://cdn.srv.whereby.com/embed/v1.js" type="module" />
      </div>
    </div>
  );
};

export default WhisperPage;
