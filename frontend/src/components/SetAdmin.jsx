import { Select, Layout, Button ,Input} from "antd";
import axios from "axios";
import React,{useState} from "react";
import "../css/AdminPages.css";
import openNotification from "./Notification";
const { Option } = Select;
const children = [];

for (let i = 10; i < 36; i++) {
  children.push(<Option key={i.toString(36) + i}>{i.toString(36) + i}</Option>);
}

const Content = Layout;
const SetAdmin = ({ loginStatus, userInfo }) => {
  const [reviewEmail, setReviewEmail] = useState('');
  const [forumEmail, setForumEmail] = useState('');
  const setReviewAdmin=()=>{
    if (!loginStatus) {
      openNotification({
        "title": "please login first"
      })
      return;
    }
    console.log(userInfo);
    axios
      .post("http://127.0.0.1:8080/review/admin",{
        user_email: reviewEmail,
        admin_email: userInfo.email,
        token: userInfo.token
      })
      .then(function (response) {
        console.log(response.data);
        openNotification({
          "title": "Successful!!!"
        })
      })
      .catch(function (error) {
        console.log(error.response.data);
        openNotification({
          "title": "An error occur",
          "content": error.response.data.message
        })
      });
  }

  const setForumAdmin=()=>{
    if (!loginStatus) {
      openNotification({
        "title": "please login first"
      })
      return;
    }
    axios
      .post("http://127.0.0.1:8080/thread/admin",{
        user_email: reviewEmail,
        admin_email: userInfo.email,
        token: userInfo.token
      })
      .then(function (response) {
        console.log(response.data);
        openNotification({
          "title": "Successful!!!"
        })
      })
      .catch(function (error) {
        console.log(error.response.data);
        openNotification({
          "title": "An error occur",
          "content": error.response.data.message
        })
      });
  }

  const setReviewAdminEmail=event => {
    setReviewEmail(event.target.value)
    console.log(event.target.value)
  }
  
  const setForumAdminEmail=event=>{
    setForumEmail(event.target.value)
    console.log(event.target.value)
  }
  
  return (
    <div className="set-admin-page">
      {" "}
      <Content>
        {" "}
        <div className="set-admin-area">
          <center>
            <div className="set-admin-title">set thread admin</div>
            <div className="set-admin-select">
              {" "}
              <div>please provide target admin email</div>
              <Input onChange={setReviewAdminEmail} value={reviewEmail}></Input>
              <Button onClick={setReviewAdmin}> submit </Button>
            </div>
          </center>
        </div>
        <div className="set-admin-area">
          <center>
            <div className="set-admin-title">set forum admin</div>
            <div className="set-admin-select">
              {" "}
              <div>please provide target admin email</div>
              <Input onChange={setForumAdminEmail} value={forumEmail}></Input>
              <Button onClick={setForumAdmin}> submit </Button>
            </div>
          </center>
        </div>
      </Content>
    </div>
  );
};
export default SetAdmin;
