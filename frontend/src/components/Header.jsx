import React from "react";
import { Affix } from "antd";
import logo from "../images/logo.png";
import { Button } from "antd";
import { useNavigate } from "react-router-dom";

function Header({ loginStatus, userInfo }) {

  let navigate = useNavigate();
  return (
    <Affix>    
    <div className="header">
      <div className="header-logo">
        <img src={logo} alt="logo" />
      </div>
      <div className="header-top-right-wrapper">
        { loginStatus ?
          <div>
            Welcome!
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
