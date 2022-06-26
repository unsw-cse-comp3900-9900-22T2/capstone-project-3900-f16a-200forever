import React from "react";
import { Affix } from "antd";
import logo from "../images/logo.png";
import { Button } from "antd";
import { useNavigate } from "react-router-dom";

function Header({ loginStatus }) {
  let navigate = useNavigate();
  return (
    <Affix>    
      {/* todo make header not transparent */}
      <div className="homepage_header">
        {/* {logo} */}
        <div className="homepage_header_logo">
          <img src={logo} alt="logo" />
        </div>
        {/* todo make image and text into one image */}
        <div className="homepage_header_titles">Movie Forever</div>
        { loginStatus ?
          // todo modify welcome msg and layout
          <div> Welcome! 
            {/* todo add profile and logout button */}
          </div> :
          <div>
            <Button className="homepage_header_login" onClick={()=>navigate("/login")}>login</Button>
            <Button className="homepage_header_register" onClick={()=>navigate("register")}>register</Button>
          </div>
        }        
      </div>
    </Affix>
  );
}
export default Header;
