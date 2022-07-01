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

const Login = ({ loginStatus, updateLoginStatus }) => {
  let navigate = useNavigate();
  const { Title } = Typography;
  const onFinish = (values) => {
    // console.log("Success:", values);
    // todo add url
    // todo handle success
    // todo handle error
    // todo forget password?
    axios
      .post("http://127.0.0.1:8080/login", {
        email: values["email"],
        password: values["password"],
        is_admin: true
      })
      .then(function (response) {
        navigate("/admin/control")
      })
      .catch(function (error) {
        console.log(error.response);
        openNotification({
          "title": "An error occur",
          "content": error.response["data"]["message"]
        })
      });
  };

  const onFinishFailed = (errorInfo) => {
    // console.log("Failed:", errorInfo);
    // todo change the error msg
    notification.open({
      message: `Notification`,
      description:
        "This is the content of the notification. This is the content of the notification. This is the content of the notification.",
      placement: "top",
      duration: 3,
      onClick: () => {
        console.log("Notification Clicked!");
      },
    });
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
        <Title>Admin log in here</Title>
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
        </Form.Item>
      </Form>
    </div>
  );
};

function AdminLogin(params) {
  return (
    <div>
      <Login></Login>
    </div>
  );
}
export default AdminLogin;
