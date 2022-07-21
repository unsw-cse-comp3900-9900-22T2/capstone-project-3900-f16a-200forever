import { Select, Layout, Button ,Input} from "antd";
import axios from "axios";
import React,{useState} from "react";
import "../css/AdminPages.css";
const { Option } = Select;
const children = [];

for (let i = 10; i < 36; i++) {
  children.push(<Option key={i.toString(36) + i}>{i.toString(36) + i}</Option>);
}


const Content = Layout;
const SetAdmin = () => {
  const [reviewAdmin, setReviewEmail] = useState('');
  const [forum, setForumEmail] = useState('');
  const setReviewAdmin=()=>{
    axios.post("http://127.0.0.1:8080/review/admin",{
      user_email:reviewAdmin,
      // admin_email: daotingc@gmail.com,
      token:"I am a fake token"
    })
    console.log(reviewAdmin)
  }
  const setForumAdmin=()=>{
    axios.post("http://127.0.0.1:8080/thread/admin" , {
      user_email:forum,
      // admin_email:daotingc@gmail.com,
      token:"I am a fake token"
    })
    console.log("hihi")
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
              <Input onChange={setReviewAdminEmail} value={reviewAdmin}></Input>
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
              <Input onChange={setForumAdminEmail} value={forum}></Input>
              <Button onClick={setForumAdmin}> submit </Button>
            </div>
          </center>
        </div>
      </Content>
    </div>
  );
};
export default SetAdmin;
