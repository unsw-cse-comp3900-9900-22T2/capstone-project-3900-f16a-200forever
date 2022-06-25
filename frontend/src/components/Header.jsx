import React from "react";

import logo from "../images/logo.png";
import { Button } from "antd";
function Header() {
  return (
    <div className="homepage_header">
      {/* {logo} */}
      <div className="homepage_header_logo">
        <img src={logo} alt="logo" />
      </div>
      <div className="homepage_header_titles">Movie Forever</div>

      <Button className="homepage_header_login">login</Button>
      <Button className="homepage_header_register">register</Button>
    </div>
  );
}
export default Header;
