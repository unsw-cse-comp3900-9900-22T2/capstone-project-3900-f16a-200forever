import React from "react";
import { Affix, Col, Row } from "antd";
import logo from "../images/new_logo.png";
import { Button, Space } from "antd";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import openNotification from "./Notification";

function Header({ loginStatus, updateLoginStatus, userInfo, updateUserInfo, cookie, setCookie, sid }) {
  let navigate = useNavigate();
  const do_logout = () => {
    axios
      .post("http://127.0.0.1:8080/logout", {
        email: userInfo["email"],
        token: userInfo["token"]
      })
      .then(function (response) {
        console.log(userInfo)
        console.log(response);
        updateLoginStatus(false);
        updateUserInfo({
          "username": "",
          "token": "",
          "email": ""
        })
        // todo change url here
        navigate("/");
      })
      .catch(function (error) {
        console.log(error);
        openNotification({
          "title": "An error occur",
          // "content": error.response.data.message
        })
      });
  }

  // const haha = () => {
  //   console.log(userInfo);
  //   console.log(userInfo.email)
  //   console.log(userInfo.token)
  //   console.log(sid);
  //   axios.defaults.headers.post['Cookie'] = "session=5b0dc704-3114-465b-a76f-35522701e7d9"
  //   // console.log(document.cookie)
  // }

  return (
    <Affix>    
    <div className="header">
      <Link to={"/"}>
        <div className="header-logo">
          <img src={logo} alt="logo" /> 
        </div>
      </Link>
      <div className="header-top-right-wrapper">
        { loginStatus ?
          <div>
            <span>Welcome!</span>
            {/* <Button onClick={haha}>fjalksdjf</Button> */}
            <Button onClick={do_logout}>logout</Button>
          </div>
          :
          <div>
            <Button className="header-login-btn" onClick={()=>navigate("/login")}>login</Button>
            <Button className="header-register-btn" onClick={()=>navigate("register")}>register</Button>
            <Button className="header-register-btn" onClick={()=>navigate("/userprofile/:id")}>UserProfile</Button>
          </div>
        }
      </div>
    </div>
  </Affix>

  );
}
export default Header;
