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
  Card,
} from "antd";
import { useNavigate } from "react-router-dom";
import React, { useState } from "react";
import "../css/UserProfile.css";
import ImgCrop from "antd-img-crop";
import { useInsertionEffect } from "react";
import axios from "axios";
const { Title, Text } = Typography;
const { Meta } = Card;
const UserProfile = () => {
  let navigate = useNavigate();
  const onFinish = (values) => {
    console.log("Received values of form:", values);
  };
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
  };
  const { id } = useParams();
  const [userInfo, setUserInfo] = useState({});

  return (
    <div className="user-profile-page">
      <div className="user-profile-detail">
        <div className="user-detail">
          <div className="upload-user-picture">
            <Image
              width={120}
              src="https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png"
            />
          </div>
          <div className="user-box">
            <div className="user-name">
              <Text>user name:</Text>
            </div>

            <div className="user-signature">
              <Text>user signature: hello world</Text>
            </div>

            <div className="user-badge-img"></div>
          </div>
          <div className="user-badge">
            <div className="badge-title">
              <Text>user badge:</Text>
            </div>
            <Space>
              <Image
                width={50}
                src="https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png"
              ></Image>
              <Image
                width={50}
                src="https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png"
              ></Image>
            </Space>
          </div>
        </div>
        <div className="user-profile-movie-list">
          <Row>
            <Col span={8}>
              <div className="blacklist">
                <Text>BlackList</Text>

                <Card
                  hoverable
                  style={{ width: 100 }}
                  cover={
                    <img
                      alt="example"
                      src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png"
                    />
                  }
                >
                  <Meta title="Europe Street beat" />
                </Card>
              </div>
            </Col>

            <Col span={8}>
              <div className="watched">
                <Text>watched list</Text>
                <Card
                  hoverable
                  style={{ width: 100 }}
                  cover={
                    <img
                      alt="example"
                      src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png"
                    />
                  }
                >
                  <Meta title="Europe Street beat" />
                </Card>
              </div>
            </Col>
            <Col span={8}>
              <div className="droppedlist">
                <Text>dropped list</Text>
                <Card
                  hoverable
                  style={{ width: 100 }}
                  cover={
                    <img
                      alt="example"
                      src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png"
                    />
                  }
                >
                  <Meta title="Europe Street beat" />
                </Card>
              </div>
            </Col>
          </Row>
        </div>
      </div>

      <div className="user-profile-btn-group">
        <Button onClick={() => navigate(`/userprofile/guesswhatyoulike/id=1`)}>
          Guess what you like
        </Button>
        <Button>Friend List</Button>
        <Button>Edit banned list</Button>
        <Button onClick={() => navigate(`/userprofile/edit/id=1`)}>
          Edit profile
        </Button>
      </div>
    </div>
  );
};
export default UserProfile;
