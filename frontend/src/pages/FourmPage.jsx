import React from "react";
import "../css/FourmPage.css";
import GenresInHomepage from "../components/GneresComponent";
import { Typography } from "antd";

import { Breadcrumb, Button, Layout, Menu, List } from "antd";

import { Link, useNavigate, useParams } from "react-router-dom";
import { Card, Space } from "antd";
import { useState } from "react";
import axios from "axios";
import openNotification from "../components/Notification";
import { useEffect } from "react";
const { Header, Footer, Sider, Content } = Layout;
const { Meta } = Card;

const ForumPage = () => {
  const { Title } = Typography;
  const [genres, setGenres] = useState([]);
  let navigate = useNavigate();
  useEffect(() => {
    axios
      // todo change url here
      .get("http://127.0.0.1:8080/genre/all", {})
      .then(function (response) {
        console.log(response.data);
        setGenres(response.data.genres);
      })
      // todo handle error
      .catch(function (error) {
        console.log(error.response);
        openNotification({
          title: "Error",
        });
      });
  }, []);

  return (
    // <div className="forum-page">
    //   hello
    //   <div className="category">hello</div>
    //   <div className="post"></div>
    //   <div className="detail"> hello</div>
    // </div>
    <div className="forum-page">
      <div className="new-post-btn">
        <Button onClick={() => navigate("/newpost")}>
          New Post
        </Button>
      </div>
      <div className="wrapper">
        <div className="title-wraper">
          <Title>Forum by genres</Title>
        </div>

        <div className="genres-component-in-HomePage">
          <List
            grid={{
              gutter: 16,
              xs: 1,
              sm: 2,
              md: 4,
              lg: 4,
              xl: 6,
              xxl: 10,
            }}
            dataSource={genres}
            renderItem={(item) => (
              <List.Item>
                <Link to={`/forum/id=${item.id}`}>
                  <Card
                    hoverable
                    bordered={true}
                    // loading={true}
                  >
                    <Meta title={item.name} />
                  </Card>
                </Link>
              </List.Item>
            )}
          />
        </div>
      </div>
    </div>
  );
};

export default ForumPage;
