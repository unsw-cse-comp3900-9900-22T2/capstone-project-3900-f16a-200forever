import { Image, Layout, Rate } from "antd";
import React, { useState } from "react";
import { Typography, List, Card } from "antd";
import "../css/MovieDetail.css";
import { useParams, Link } from "react-router-dom";
import { useEffect } from "react";
import axios from "axios";
import "../css/DirectorPage.css";
const { Meta } = Card;
const { Header, Content, Footer } = Layout;
const desc = ["terrible", "bad", "normal", "good", "wonderful"];
const { Title, Text } = Typography;
const data = [
  {
    src: "https://image.tmdb.org/t/p/w600_and_h900_bestv2/hQ4pYsIbP22TMXOUdSfC2mjWrO0.jpg",
  },
  {
    src: "https://image.tmdb.org/t/p/w600_and_h900_bestv2/hQ4pYsIbP22TMXOUdSfC2mjWrO0.jpg",
  },
];
const DirectorPage = () => {
  return (
    <div className="director-page">
      <div className="director-detail">
        <div className="director-image">
          <Image
            className="image"
            src={
              "https://image.tmdb.org/t/p/w600_and_h900_bestv2/hQ4pYsIbP22TMXOUdSfC2mjWrO0.jpg"
            }
            alt="director-image"
          ></Image>
        </div>
        <div className="director-box">
          <div className="director-name">
            <Title level={3}>Name:{}</Title>
            <Title level={4}>Gender:{}</Title>
          </div>
        </div>
        <div className="director-related-movies">
          <Title level={2}>More movies</Title>
          <List
            grid={{
              gutter: 16,
              xs: 1,
              sm: 2,
              md: 4,
              lg: 4,
              xl: 6,
              xxl: 3,
            }}
            dataSource={data}
            renderItem={(item) => (
              <List.Item>
                <Link to={`/movie/detail/id=1`}>
                  <div className="director-card">
                    {" "}
                    <Card
                      hoverable
                      bordered={false}
                      style={{}}
                      cover={
                        <img
                          alt="example"
                          src={
                            "https://image.tmdb.org/t/p/w600_and_h900_bestv2/hQ4pYsIbP22TMXOUdSfC2mjWrO0.jpg"
                          }
                        />
                      }
                    >
                      <Meta title="MovieName" />
                    </Card>
                  </div>
                </Link>
              </List.Item>
            )}
          ></List>
        </div>
      </div>
    </div>
  );
};
export default DirectorPage;
