import { Select, Layout, Button } from "antd";
import React from "react";
import "../css/AdminPages.css";
const { Option } = Select;
const children = [];

for (let i = 10; i < 36; i++) {
  children.push(<Option key={i.toString(36) + i}>{i.toString(36) + i}</Option>);
}

const handleChange = (value) => {
  console.log(`selected ${value}`);
};
const Content = Layout;
const SetAdmin = () => {
  return (
    <div className="set-admin-page">
      {" "}
      <Content>
        {" "}
        <div className="set-admin-area">
          <center>
            <div className="set-admin-title">set admin</div>
            <div className="set-admin-select">
              {" "}
              <Select
                mode="multiple"
                allowClear
                style={{
                  width: "100%",
                }}
                placeholder="Please select"
                defaultValue={["a10", "c12"]}
                onChange={handleChange}
              >
                {children}
              </Select>
              <br />
              <Select
                mode="multiple"
                disabled
                style={{
                  width: "100%",
                }}
                placeholder="Please select"
                defaultValue={["a10", "c12"]}
                onChange={handleChange}
              >
                {children}
              </Select>
              <Button> submit </Button>
            </div>
          </center>
        </div>
      </Content>
    </div>
  );
};
export default SetAdmin;
