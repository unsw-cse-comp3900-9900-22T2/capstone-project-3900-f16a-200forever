import { Button, Checkbox, Form, Input, notification } from "antd";
import { Typography } from "antd";
import axios from "axios";
import "../css/Register.css";
import openNotification from "./Notification";
import { useNavigate } from "react-router-dom";

const Register = ({ updateLoginStatus, updateUserInfo }) => {
  let navigate = useNavigate();
  const { Title, Text } = Typography;
  const onFinish = (values) => {
    // console.log("Success:", values);
    axios
      .post("http://127.0.0.1:8080/register", {
        name: values["username"],
        email: values["email"],
        password: values["password"],
      })
      .then(function (response) {
        // console.log(response);
        navigate("/login");
        openNotification({
          "title": "You have registered successfully"
        })
      })
      .catch(function (error) {
        // console.log((error.response.data));
        // console.log(typeof(error.response.data))
        openNotification({
          "title": "Register error",
          "content": error.response.data.message
        })
      });
  };

  const displayError = (errorMsg) => {
    // todo modify this msg
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

  const onFinishFailed = (errorInfo) => {
    // console.log("Failed:", errorInfo);
    displayError("Please finish all");
  };

  // todo modify the layout for comfirm password
  return (
    <div className="register-body">
      
      <Form
        className="register-form"
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
        <Title>
          Welcome! Please register!
        </Title>
        <Form.Item
          label="username"
          name="username"
          rules={[
            {
              required: true,
              message: "Please enter your username",
            },
          ]}
        >
          {/* todo make it hover or icon */}
          <Input placeholder="username must be 6-20 characters" />
        </Form.Item>
        {/* <Text calssName="register-username-text">
          username must be 6-20 characters
        </Text> */}
        <Form.Item
          label="email"
          name="email"
          rules={[
            {
              required: true,
              message: "Please enter your Email",
            },
          ]}
        >
          <Input placeholder="Email" />
        </Form.Item>
        <Form.Item
          label="Password"
          name="password"
          rules={[
            {
              required: true,
              message: "Please enter your password",
            },
          ]}
        >
          <Input.Password placeholder="Password" />
        </Form.Item>
        <Form.Item
          name="confirm"
          label="Confirm Password"
          dependencies={["password"]}
          hasFeedback
          rules={[
            {
              required: true,
              message: "Please confirm your password!",
            },
            ({ getFieldValue }) => ({
              validator(_, value) {
                if (!value || getFieldValue("password") === value) {
                  return Promise.resolve();
                }

                return Promise.reject(
                  new Error("The two passwords that you entered do not match!")
                );
              },
            }),
          ]}
        >
          <Input.Password />
        </Form.Item>

        <Form.Item
          wrapperCol={{
            offset: 10,
          }}
        >
          <Button
            classname="register-form-button"
            type="primary"
            htmlType="submit"
          >
            click to register
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
};
export default Register;
