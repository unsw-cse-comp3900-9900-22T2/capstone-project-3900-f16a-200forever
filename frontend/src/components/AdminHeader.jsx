import React from "react";
import { Affix, Col, Row } from "antd";
import logo from "../images/new_logo.png";
import { Button, Space } from "antd";
import { Link, useNavigate } from "react-router-dom";
import "../css/AdminHeader.css";
import axios from "axios";
import openNotification from "./Notification";

function AdminHeader({ loginStatus, updateLoginStatus }) {
  let navigate = useNavigate();
  const do_logout = () => {
    axios
      .post("http://127.0.0.1:8080/logout", {
        // email: userInfo["email"],
        // token: userInfo["token"],
      })
      .then(function (response) {
        // console.log(userInfo);
        console.log(response);
        // todo change url here
        navigate("/");
      })
      .catch(function (error) {
        console.log(error);
        openNotification({
          title: "An error occur",
          // "content": error.response.data.message
        });
      });
  };
  return (
    <Affix>
      <div className="header">
        <div className="admin-header-area">
          <Link to={"/"}>
            <div className="header-logo">
              <img src={logo} alt="logo" />
            </div>
          </Link>
        </div>

        <div className="header-top-right-wrapper">
          {loginStatus ? (
            <div>
              <span>Welcome!</span>
              <Button onClick={do_logout}>logout</Button>
            </div>
          ) : (
            <div></div>
          )}
        </div>
      </div>
    </Affix>
  );
}
export default AdminHeader;
