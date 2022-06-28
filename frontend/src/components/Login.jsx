import { Button, Checkbox, Form, Input, notification } from "antd";
import { Typography } from "antd";
import axios from "axios";
import "../css/Login.css";
import { useNavigate } from "react-router-dom";
import openNotification from "./Notification";

const tailLayout = {
  wrapperCol: {
    offset: 8,
    span: 16,
  },
};

const Login = ({ updateLoginStatus, updateUserInfo }) => {
  let navigate = useNavigate();
  const { Title } = Typography;
  const onFinish = (values) => {
    console.log("Success:", values);
    // todo add url
    // todo handle success
    // todo handle error
    // todo forget password?
    axios
      .post("/url", {
        email: values["email"],
        password: values["password"],
      })
      .then(function (response) {
        console.log(response);
        updateLoginStatus(true);
        updateUserInfo({
          "username": response["username"],
          "token": response["token"]
        })
        // todo change url here
        navigate("/");
      })
      .catch(function (error) {
        console.log(error);
        openNotification({
          "title": "An error occur",
          "content": error
        })
      });
  };

  const onFinishFailed = () => {
    // console.log("Failed:", errorInfo);
    // todo change the error msg
    openNotification({
      "title": "Please enter all info"
    })
  };

  return (
    <div className="login-body">
      <Form
        className="login-form"
        name="basic"
        labelCol={{
          span: 8,
        }}
        wrapperCol={{
          span: 20,
        }}
     
        onFinish={onFinish}
        onFinishFailed={onFinishFailed}
        autoComplete="off"
      >
        <Title>Please log in here</Title>
        <Form.Item
          label="Email"
          name="email"
          rules={[
            {
              required: true,
              message: "Please enter your email!",
            },
          ]}
        >
          <Input placeholder="Please enter your username!" />
        </Form.Item>

        <Form.Item
          label="Password"
          name="password"
          rules={[
            {
              required: true,
              message: "Please enter your password!",
            },
          ]}
        >
          <Input.Password placeholder="Please enter your password!" />
        </Form.Item>
        <Form.Item {...tailLayout}>
          <Button
            classname="login-form-button"
            type="primary"
            htmlType="submit"
          >
            LOGIN
          </Button>

          <Button
            classname="login-form-to-register"
            onClick={()=>navigate("/register")}
            htmlType="button"
          >
            do not have account? Click to register
          </Button>
          <Button
            classname="login-forget-button"
            type="link"
            htmlType="button"
            onClick={()=>navigate("/forgetpassword")}
          >
            Forget Password
          </Button>
          
          {/* todo add forget button */}
        </Form.Item>
      </Form>
    </div>
  );
};

export default Login;
