import React from "react";
import { Affix, Col, Row } from "antd";
import logo from "../images/new_logo.png";
import { Button, Space } from "antd";
import { Link, useNavigate } from "react-router-dom";

function Header({ loginStatus, userInfo }) {

  let navigate = useNavigate();
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
            Welcome!
            <Button> logout</Button>
          </div>
          :
          <div>
            <Button className="header-login-btn" onClick={()=>navigate("/login")}>login</Button>
            <Button className="header-register-btn" onClick={()=>navigate("register")}>register</Button>
          </div>
        }
      </div>
    </div>
  </Affix>

  );
}
export default Header;
