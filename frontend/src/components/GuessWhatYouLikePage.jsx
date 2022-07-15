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
  Layout,
  List,
  Card,
  Pagination,
} from "antd";
import { useNavigate } from "react-router-dom";
import React, { useState } from "react";
import "../css/UserProfile.css";
import ImgCrop from "antd-img-crop";
import { useInsertionEffect } from "react";
import axios from "axios";
import "../css/UserProfile.css";
import Title from "antd/lib/skeleton/Title";
const { Header, Content, Footer } = Layout;
const { Meta } = Card;
const GuessWhatYouLikePage = () => {
  const { type, keywords, order } = useParams();
  const [showList, setShowList] = useState([]);
  const type_val = type.replace("type=", "")
  return (
    <div className="guess-what-you-like-page">
      <Content
        style={{
          paddingTop: 100,
          background: "white",
        }}
      >
        <div className="guess-what-you-like-title">Guess what you like</div>
        <div className="guess-you-like-card-wrap">
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
        dataSource={showList}
        renderItem={(item) => (
          <List.Item>
            {
              type_val === "director" ?
              <Link to={`/director/id=${item.id}`}>
                <Card
                  hoverable
                  bordered={false}
                  style={{}}
                  cover={
                    <img
                      src={item.backdrop}
                      alt="example"
                    />
                  }
                >
                  <Meta title={item.title}/>
                </Card>   
              </Link>
                :
              <Link to={`/movie/detail/id=${item.id}`}>
                <Card
                  hoverable
                  bordered={false}
                  style={{}}
                  cover={
                    <img
                      alt="example"
                      src={item.backdrop}
                    />
                  }
                >
                  <Meta title={item.title} description={`rating: 0`} />
                </Card>
              </Link>
            }
          </List.Item>
        )}
      />
         
        </div>
      </Content>
    </div>
  );
};

export default GuessWhatYouLikePage;
