import React from "react";
import "../App.css";
import { useState } from "react";
import Axios from "axios";
import sendBtn from "../assets/send.svg";

const Chat = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const handleSend = () => {
    Axios.post("http://10.140.122.128:8000/api/openai/", {
      message: input,
    }).then((response) => {
      if (response.data.result === null) {
        setMessages([
          ...messages,
          { text: input, isBot: false },
          {
            text: "Sorry I didn't quite get that. Would you please retry?",
            isBot: true,
          },
        ]);
      } else {
        console.log(response.data.result);
        setMessages([
          ...messages,
          { text: input, isBot: false },
          { text: response.data.result, isBot: true },
        ]);
      }
    });
  };

  return (
    <div className="main">
      <div className="chats">
        {messages.map((messages, i) => {
          return (
            <div key={i} className={messages.isBot ? "chat bot" : "chat"}>
              <img src="" alt="" />
              <p className="txt">{messages.text}</p>
            </div>
          );
        })}
      </div>
      <div className="chatFooter">
        <div className="inp">
          <input
            type="text"
            placeholder="Enter Question Here"
            value={input}
            onChange={(e) => {
              setInput(e.target.value);
            }}
          />
          <button className="send" onClick={handleSend}>
            <img src={sendBtn} alt="Send" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chat;
