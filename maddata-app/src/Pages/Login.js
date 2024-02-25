// Import React and other necessary dependencies
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import logo from "../assets/AccessiChatIcon.jpg";
import styles from "./Login.module.css"; // Import your CSS file

// Functional component definition
const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loginStatus, setLoginStatus] = useState("");

  let navigate = useNavigate();

  const handleSubmit = async (event) => {
    navigate("/");
  };

  return (
    <html lang="en">
      <head>
        <title>Login In Box</title>
      </head>

      <body className={styles.body_lg}>
        <div className={styles.background_lg}>
          <div className={styles.shape_lg}></div>
          <div className={styles.shape_lg}></div>
        </div>
        <form className={styles.form_lg}>
          <div className={styles.text_lg}>
            <img src={logo} alt="" className={styles.logo_lg} />
            AccessiChat
          </div>
          <label className={styles.label_lg} htmlFor="username">
            Username
          </label>
          <input
            className={styles.input_lg}
            type="text"
            placeholder="Email or Phone"
            id="username"
          />
          <label className={styles.label_lg} htmlFor="password">
            Password
          </label>
          <input
            className={styles.input_lg}
            type="password"
            placeholder="Password"
            id="password"
          />
          <button className={styles.button_lg} onClick={handleSubmit}>
            Log In
          </button>
          <div className={styles.social_lg}></div>
        </form>
      </body>
    </html>
  );
};

export default Login;
