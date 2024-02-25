import "./App.css";
import home from "./assets/home.svg";
import msgIcon from "./assets/message.svg";
import sendBtn from "./assets/send.svg";
import { useState } from "react";
import Axios from "axios";

import Chat from "./Components/Chat.js";
import Schedule from "./Components/Schedule.js";

import calendarIcon from "./assets/calendarIcon.svg";
import emailIcon from "./assets/emailIcon.svg";
import medicalIcon from "./assets/medicalIcon.svg";
import settingsIcon from "./assets/settingsIcon.svg";
import profileIcon from "./assets/profileIcon.svg";
import locationIcon from "./assets/locationIcon.svg";
import logo from "./assets/AccessiChatIcon.jpg";

import Login from "./Pages/Login.js";
import Main from "./Pages/Main.js";
import { Router, Link, Routes, Route } from "react-router-dom";
import Map from "./Pages/Map.js";

function App() {
  return (
    <div className="App">
      <div className="Routing Links">
        <Routes>
          <Route exact path="/" element={<Main />} />
          <Route exact path="/login" element={<Login />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
