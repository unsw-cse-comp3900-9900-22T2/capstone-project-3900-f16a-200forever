import { Select, Layout, Button ,Input} from "antd";
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
              <div>please provide target admin email</div>
              <Input></Input>
              <Button> submit </Button>
            </div>
          </center>
        </div>
      </Content>
    </div>
  );
};
export default SetAdmin;
