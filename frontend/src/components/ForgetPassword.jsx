import React, { Component } from "react";
import { Form, Typography, Col, Row, Input, Button } from "antd";
import "../css/ForgetPassword.css";
const ForgetPassword = () => {
  const { Title, Text } = Typography;
  const onFinish = (values) => {};
  const onFinishFailed = (errorInfo) => {};
  return (
    <div>
      <Form
        className="forgetpassword-form"
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
          wrapperCol={{
            offset: 4,
          }}
        >
          <Title className="forgetpassword-title">Forgot passwords</Title>
        </Form.Item>

        {/* email */}
        <Form.Item
          name="email"
          label="E-mail"
          rules={[
            {
              type: "email",
              message: "The input is not valid E-mail",
            },
            {
              required: true,
              message: "Please input your E-mail",
            },
          ]}
        >
          <Input />
        </Form.Item>
        {/* code */}
        <Form.Item
          label="Verfication code"
          extra="Please provide email verfication code"
        >
          <Row gutter={20}>
            <Col span={8}>
              <Form.Item
                name="Verfication code"
                noStyle
                rules={[
                  {
                    required: true,
                    message: "Please input the verification code you got!",
                  },
                ]}
              >
                <Input />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Button>Get code</Button>
            </Col>
          </Row>
        </Form.Item>

        <Form.Item
          name="password"
          label="Password"
          rules={[
            {
              required: true,
              message: "Please input your password!",
            },
          ]}
          hasFeedback
        >
          <Input.Password />
        </Form.Item>

        <Form.Item
          name="confirm"
          label="Confirm Password"
          rules={[
            {
              required: true,
              message: "Please confirm your password!",
            },
            ({ getFieldValue }) => ({
              validator(rule, value) {
                if (!value || getFieldValue("password") === value) {
                  return Promise.resolve();
                }

                return Promise.reject(
                  "The two passwords that you entered do not match!"
                );
              },
            }),
          ]}
          hasFeedback
        >
          <Input.Password />
        </Form.Item>
        <Form.Item
          wrapperCol={{
            offset: 10,
            span: 20,
          }}
        >
          <Button>submit</Button>
        </Form.Item>
      </Form>
    </div>
  );
};

export default ForgetPassword;
