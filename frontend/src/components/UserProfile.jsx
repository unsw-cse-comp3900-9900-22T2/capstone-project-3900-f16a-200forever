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
import React, { useEffect, useState } from "react";
import "../css/UserProfile.css";
import ImgCrop from "antd-img-crop";
import { useInsertionEffect } from "react";
import axios from "axios";
import openNotification from "./Notification";
import { UserOutlined } from '@ant-design/icons';
import Avatar from "antd/lib/avatar/avatar";
import UserProfileEditPage from "./UserProfileEditPage";

const { Title, Text } = Typography;
const { Meta } = Card;

const UserProfile = ({ userInfo }) => {
  const navigate = useNavigate();
  const [userProfile, setUserProfile] = useState({});
  const [isEdit, setIsEdit] = useState(false);
  useEffect(() => {
    axios
    // todo change url here
    .get("http://127.0.0.1:8080/user/userprofile", {
      params: {
        "user_id": userInfo.id
      }
    })
    .then(function (response) {
      // console.log(userInfo);
      console.log(response.data);
      setUserProfile(response.data);
    })
    // todo handle error
    .catch(function (error) {
      console.log(error.response);
      openNotification({
        "title": "error",
      })
    });
  }, [])

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

  return (
    <>
      {
        isEdit === false ?
        <div className="user-profile-page">
        <div className="user-profile-detail">
          <div className="user-detail">
            <div className="upload-user-picture">
              {userProfile.profile_picture === null ?
                <Avatar shape="square" size="large" icon={<UserOutlined/>}></Avatar>
                :
                <Image
                width={120}
                src={userProfile.profile_picture}
              />
              }
              
            </div>
            <div className="user-box">
              <div className="user-name">
                <Text>Username: {userProfile.username}</Text>
              </div>
  
              <div className="user-signature">
                <Text>user signature: {userProfile.signature}</Text>
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
          <Button onClick={() => setIsEdit(true)}>
            Edit profile
          </Button>
        </div>
      </div>
        :
        <UserProfileEditPage userProfile={userProfile}></UserProfileEditPage>
      }
    </>
      );
};
export default UserProfile;
