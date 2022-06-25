import React from "react";

import logo from "../images/logo.png";
import { Button } from "antd";
import { useNavigate } from "react-router-dom";

function Header() {
  let navigate = useNavigate();
  return (
    <div className="homepage_header">
      {/* {logo} */}
      <div className="homepage_header_logo">
        <img src={logo} alt="logo" />
      </div>
      <div className="homepage_header_titles">Movie Forever</div>

      <Button className="homepage_header_login" onClick={()=>navigate("/Login")}>login</Button>
      <Button className="homepage_header_register" onClick={()=>navigate("Register")}>register</Button>
    </div>
  );
}
export default Header;
