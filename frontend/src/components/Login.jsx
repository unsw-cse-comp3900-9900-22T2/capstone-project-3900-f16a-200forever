import { Button, Checkbox, Form, Input, notification } from "antd";
import { Typography } from "antd";
import axios from "axios";
import "../css/Login.css";
const tailLayout = {
  wrapperCol: {
    offset: 8,
    span: 16,
  },
};
const Login = ({ updateLoginStatus }) => {
  const { Title } = Typography;
  const onFinish = (values) => {
    // console.log("Success:", values);
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
      })
      .catch(function (error) {
        console.log(error);
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
    <div>
      <Title className="login-title">Please log in </Title>

      <Form
        className="login-form"
        name="basic"
        labelCol={{
          span: 8,
        }}
        wrapperCol={{
          span: 16,
        }}
        initialValues={{
          remember: true,
        }}
        onFinish={onFinish}
        onFinishFailed={onFinishFailed}
        autoComplete="off"
      >
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
        {/* todo discuss remember me */}
        {/* <Form.Item
          name="remember"
          valuePropName="checked"
          wrapperCol={{
            offset: 8,
            span: 16,
          }}
        >
          <Checkbox>Remember me</Checkbox>
        </Form.Item> */}

        <Form.Item {...tailLayout}>
          <Button
            classname="login-form-button"
            type="primary"
            htmlType="submit"
          >
            LOGIN
          </Button>
          <Button
            classname="login-forget-button"
            
            htmlType="button"
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
