import React from "react";
import { Affix, Col, Row } from "antd";
import logo from "../images/logo.png";
import { Button, Space } from "antd";
import { useNavigate } from "react-router-dom";
import "../css/AdminHeader.css"
function AdminHeader({ loginStatus }) {
  let navigate = useNavigate();
  return (
    <Affix>
      <Row>
        <div className="admin-header">
          {/* {logo} */}
          <Col offset={1}>
            <div className="admin-header-logo">
              <img src={logo} alt="logo" />
            </div>
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
                  <Button className="admin-header-logout">logout</Button>
                </Space>
              </div>
            )}
          </Col>
        </div>
      </Row>
    </Affix>
  );
}
export default AdminHeader;
