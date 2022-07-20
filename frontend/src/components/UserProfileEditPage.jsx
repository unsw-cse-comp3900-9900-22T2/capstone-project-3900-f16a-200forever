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
import openNotification from "./Notification";
import { useEffect } from "react";

function fileToDataUrl(file) {
  const validFileTypes = [ 'image/jpeg', 'image/png', 'image/jpg' ]
  const valid = validFileTypes.find(type => type === file.type);
  // Bad data, let's walk away.
  if (!valid) {
      throw Error('provided file is not a png, jpg or jpeg image.');
  }
  
  const reader = new FileReader();
  const dataUrlPromise = new Promise((resolve,reject) => {
      reader.onerror = reject;
      reader.onload = () => resolve(reader.result);
  });
  reader.readAsDataURL(file);
  return dataUrlPromise;
}

const UserProfileEditPage = ({ userProfile }) => {

  const [fileList, setFileList] = useState([
    {
      uid: "-1",
      name: "image.png",
      status: "done",
      url: userProfile.profile_picture
      // url: "https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png",
    },
  ]);

  const [base64, setBase64] = useState("");

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

  const haha = (values) => {
    console.log(values);
    // console.log(userProfile)
    console.log(base64);
  }

  const onFinishFailed = () => {
    openNotification({
      "title": "Please finish all"
    })
  };

  return (
    <div className="user-profile-edit-page">
      <div className="user-profile-edit-form">
        <Form
          labelCol={{ span: 5 }}
          wrapperCol={{ span: 15 }}
          layout="horizontal"
          onFinish={haha}
          onFinishFailed={onFinishFailed}
          initialValues={{
            ["username"]: userProfile.username,
            ["signature"]: userProfile.signature
          }}
        >
          {" "}
          <Form.Item 
            label="Head Portrait:">
            <ImgCrop rotate>
              <Upload
                action="https://www.mocky.io/v2/5cc8019d300000980a055e76"
                listType="picture-card"
                fileList={fileList}
                onChange={onChange}
                onPreview={onPreview}
                accept=".png,.jpeg,.jpg"
                beforeUpload={ (file) => {
                  fileToDataUrl(file).
                  then((data) => {
                    setBase64(data);
                  })
                  return false;
                }}
              >
                {fileList.length < 1 && "+ Upload"}
              </Upload>
            </ImgCrop>
          </Form.Item>
          <Form.Item name="username" label="UserName">
            <Input></Input>
          </Form.Item>
          <Form.Item label="Personal Signature"
            name="signature">
            <Input></Input>
          </Form.Item>
          <Form.Item
            name="curr_password"
            label="current password"
            rules={[
              {
                message: "Please input your password!",
              },
            ]}
          >
            <Input.Password />
          </Form.Item>
          <Form.Item
          label="new password"
          name="password"
          rules={[
            {
              message: "Please enter your password",
            },
          ]}
        >
          <Input.Password placeholder="Password" />
        </Form.Item>
        <Form.Item
          name="confirm"
          label="confirm password"
          dependencies={["password"]}
          hasFeedback
          rules={[
            {
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


