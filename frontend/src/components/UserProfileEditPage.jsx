import { Link, useParams } from "react-router-dom";
import {
  Button,
  Radio,
  Row,
  Col,
  Space,
  Typography,
  Upload,
  Image,
  Form,
  Input,
} from "antd";
import { useNavigate } from "react-router-dom";
import React, { useState } from "react";
import "../css/UserProfile.css";
import ImgCrop from "antd-img-crop";
import { useInsertionEffect } from "react";
import axios from "axios";
import "../css/UserProfile.css";

const UserProfileEditPage = () => {
  const [fileList, setFileList] = useState([
    {
      uid: "-1",
      name: "image.png",
      status: "done",
      url: "https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png",
    },
  ]);
  const onChange = ({ fileList: newFileList }) => {
    setFileList(newFileList);
  };

  const onPreview = async (file) => {
    let src = file.url;

    if (!src) {
      src = await new Promise((resolve) => {
        const reader = new FileReader();
        reader.readAsDataURL(file.originFileObj);
        reader.onload = () => resolve(reader.result);
      });
    }

    const image = new Image();
    image.src = src;
    const imgWindow = window.open(src);
    imgWindow?.document.write(image.outerHTML);
  };
  const { id } = useParams();
  return (
    <div className="user-profile-edit-page">
      <div className="user-profile-edit-form">
        <Form
          labelCol={{ span: 5 }}
          wrapperCol={{ span: 15 }}
          layout="horizontal"
        >
          {" "}
          <Form.Item label="Head Portrait:">
            <ImgCrop rotate>
              <Upload
                action="https://www.mocky.io/v2/5cc8019d300000980a055e76"
                listType="picture-card"
                fileList={fileList}
                onChange={onChange}
                onPreview={onPreview}
              >
                {fileList.length < 5 && "+ Upload"}
              </Upload>
            </ImgCrop>
          </Form.Item>
          <Form.Item label="UserName">
            <Input></Input>
          </Form.Item>
          <Form.Item label="Personal Signature">
            <Input></Input>
          </Form.Item>
          <Form.Item
            name="password"
            label="current password"
            rules={[
              {
           
                message: "Please input your password!",
              },
            ]}
            hasFeedback
          >
            <Input.Password />
          </Form.Item>
          <Form.Item
            name="password"
            label="new password"
            rules={[
              {
           
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
    </div>
  );
};
export default UserProfileEditPage;
