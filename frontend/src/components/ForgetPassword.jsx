import React, { Component } from "react";
import { Form, Typography, Col, Row, Input, Button } from "antd";
import "../css/ForgetPassword.css";
import axios from "axios";
import openNotification from "./Notification";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

const ForgetPassword = () => {
  let navigate = useNavigate();
  const { Title, Text } = Typography;
  const [email, setEmail] = useState("");

  const updateEmail = (event) => {
    // console.log(event.target.value);
    setEmail(event.target.value);
  }

  const onFinish = (values) => {
    console.log(values);
    // todo change the url
    axios
      .post("/url", {
        email: values["email"],
        password: values["password"],
        code: values["code"]
      })
      .then(function (response) {
        console.log(response);
        navigate("/login");
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
    openNotification({
      "title": "Please enter all info"
    })
  };

  const sendCode = () => {
    console.log(email);
    // todo change url
    axios
      .post("/url", {
        email: email
      })
      .then(function (response) {
        console.log(response);
        openNotification({
          "title": "Successful",
        })
      })
      .catch(function (error) {
        console.log(error);
        openNotification({
          "title": "An error occur",
          "content": error
        })
      });
  }

  return (
    <div className="forgetpassword-body">
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
        <Form.Item
          name="email"
          label="email"
          rules={[
            {
              type: "email",
              message: "The input is not valid email",
            },
            {
              required: true,
              message: "Please enter your email",
            },
          ]}
        >
          <Input onChange={updateEmail}/>
        </Form.Item>
        <Form.Item
          label="Verfication code"
          extra="Please provide email verfication code"
        >
          <Row gutter={20}>
            <Col span={8}>
              <Form.Item
                name="code"
                noStyle
                rules={[
                  {
                    required: true,
                    message: "Please enter the verification code you got!",
                  },
                ]}
              >
                <Input />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Button onClick={sendCode}>
                Get code
              </Button>
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
          <Button
            type="primary"
            htmlType="submit"
          >
            submit</Button>
        </Form.Item>
      </Form>
    </div>
  );
};

export default ForgetPassword;
