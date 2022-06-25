import { Button, Checkbox, Form, Input } from "antd";
import { Typography } from "antd";
import "../css/Register.css";

const Register = () => {
  const { Title, Text } = Typography;
  const onFinish = (values) => {
    console.log("Success:", values);
  };

  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };

  return (
    <div>
      <Title className="register-title">
        Welcome! Please register your account!
      </Title>
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
        <Form.Item
          label="Name"
          name="Name"
          rules={[
            {
              required: true,
              message: "Please input your Name!",
            },
          ]}
        >
          <Input placeholder="username must be 6-20 characters" />
        </Form.Item>
        {/* <Text calssName="register-username-text">
          username must be 6-20 characters
        </Text> */}
        <Form.Item
          label="Email"
          name="Email"
          rules={[
            {
              required: true,
              message: "Please input your Email!",
            },
          ]}
        >
          <Input placeholder="Please input your Email!" />
        </Form.Item>
        <Form.Item
          label="Password"
          name="password"
          rules={[
            {
              required: true,
              message: "Please input your password!",
            },
          ]}
        >
          <Input.Password placeholder="Please input your password!" />
        </Form.Item>
        <Form.Item
          label="Double Password"
          name="Double password"
          rules={[
            {
              required: true,
              message: "Please double your password!",
            },
          ]}
        >
          <Input.Password placeholder="Please double your password!" />
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
            Submit
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
};
export default Register;
