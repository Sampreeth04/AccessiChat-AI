import home from "../assets/home.svg";
import { useState } from "react";
import Axios from "axios";

import Chat from "../Components/Chat.js";
import Schedule from "../Components/Schedule.js";
import Map from "./Map.js";

import calendarIcon from "../assets/calendarIcon.svg";
import emailIcon from "../assets/emailIcon.svg";
import medicalIcon from "../assets/medicalIcon.svg";
import settingsIcon from "../assets/settingsIcon.svg";
import profileIcon from "../assets/profileIcon.svg";
import locationIcon from "../assets/locationIcon.svg";
import logo from "../assets/AccessiChatIcon.jpg";

function Main() {
  const [input, setInput] = useState("");
  const [botResponse, setBotResponse] = useState("");
  const [messages, setMessages] = useState([]);

  const [chatFlag, setChatFlag] = useState(true);
  const [scheduleFlag, setScheduleFlag] = useState(false);
  const [mapFlag, setMapFlag] = useState(false);

  const handleSchedule = () => {
    setScheduleFlag(true);
    setChatFlag(false);
  };

  const handleChat = () => {
    setScheduleFlag(false);
    setChatFlag(true);
  };

  const handleMap = () => {
    setMapFlag(true);
    setChatFlag(false);
  };

  return (
    <div className="App">
      <div className="sideBar">
        <div className="upperSide">
          <div className="upperSideTop">
            <img src={logo} alt="" className="logo" />
            <span className="software">AccessiChat</span>
          </div>
          <div className="upperSideBottom">
            <button className="sideBarContent" onClick={handleChat}>
              <img src={home} alt="" />
              Home
            </button>
            <button className="sideBarContent" onClick={handleSchedule}>
              <img src={calendarIcon} alt="" />
              Schedule
            </button>
            <button className="sideBarContent" onClick={handleMap}>
              <img src={locationIcon} alt="" />
              Nearby Resources
            </button>
            <button className="sideBarContent">
              <img src={medicalIcon} alt="" />
              Medical Records
            </button>
          </div>
        </div>
        <div className="lowerSide">
          <button className="sideBarContent">
            <img src={emailIcon} alt="" className="listitemsImg" />
            Inbox
          </button>

          <button className="sideBarContent">
            <img src={settingsIcon} alt="" className="listitemsImg" />
            Settings
          </button>
          <button className="sideBarContent">
            <img src={profileIcon} alt="" className="listitemsImg" />
            Profile
          </button>
        </div>
      </div>
      {chatFlag ? <Chat /> : <Map />}
    </div>
  );
}

export default Main;
