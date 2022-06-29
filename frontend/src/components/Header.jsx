import React from "react";
import { Affix, Col, Row } from "antd";
import logo from "../images/logo.png";
import { Button, Space } from "antd";
import { useNavigate } from "react-router-dom";

function Header({ loginStatus }) {
  let navigate = useNavigate();
  return (
    <Affix>
      <Row>
        <div className="homepage-header">
          {/* {logo} */}
          <Col offset={1}>
            <div className="homepage-header-logo">
              <img src={logo} alt="logo" />
            </div>
          </Col>
          <Col offset={3}>
            {/* todo make image and text into one image */}
            <div className="homepage-header-titles">Movie Forever</div>
          </Col>
          <Col flex="auto">
            {loginStatus ? (
              // todo modify welcome msg and layout
              <div>
                Welcome!
                {/* todo add profile and logout button */}
              </div>
            ) : (
              <div>
                <Space size={"middle"} align={"end"}>
                  <Button
                    className="homepage-header-login"
                    onClick={() => navigate("/login")}
                  >
                    login
                  </Button>
                  <Button
                    className="homepage-header-register"
                    onClick={() => navigate("register")}
                  >
                    register
                  </Button>
                </Space>
              </div>
            )}
          </Col>
        </div>
      </Row>
    </Affix>
  );
}
export default Header;
