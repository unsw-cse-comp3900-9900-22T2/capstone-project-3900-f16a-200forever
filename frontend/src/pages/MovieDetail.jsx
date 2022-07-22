import { Image, Layout, Rate, List, Row, Col } from "antd";
import React, { useState } from "react";
import { Typography } from "antd";
import "../css/MovieDetail.css";
import { Link, useParams } from "react-router-dom";
import { useEffect } from "react";
import axios from "axios";
import RecommendationInMovie from "../components/RecommendationInMovie";
import MovieReview from "../components/MovieReview";
import openNotification from "../components/Notification";
import UserProfile from "../components/UserProfile";

const { Header, Content, Footer } = Layout;
const desc = ["terrible", "bad", "normal", "good", "wonderful"];
const { Title, Text } = Typography;

function MovieDetail({ userInfo, loginStatus }) {
  const { id } = useParams();
  const [movieInfo, setMovieInfo] = useState({});
  const [rating, setRating] = useState(0.0);
  const [a, seta] = useState(0);

  useEffect(() => {
    axios
      // todo change url here
      .get("http://127.0.0.1:8080/movie/moviedetails", {
        params: {
          movie_id: id.replace("id=", ""),
        },
      })
      .then(function (response) {
        console.log(response.data);
        setMovieInfo(response.data);
        // console.log(response.data["total rating"] / response.data["rating count"])
        setRating(parseFloat(response.data["total rating"] / response.data["rating count"]).toFixed(2))
        seta(Math.floor(response.data["total rating"] / response.data["rating count"]));
      })
      // todo handle error
      .catch(function (error) {
        console.log(error.response);
        openNotification({
          "title": "Viewing page error",
        })
      });
  }, []);

  return (
    <div>
      <div className="movie-detail-page">
        <div className="movie-detail">
          <div className="movie-image">
            <Image
              className="image"
              src={movieInfo.backdrop}
              alt="movie-image"
            ></Image>
          </div>
          <div className="movie-box">
            <div className="movie-title">
              <Title level={3}>Movie Name:{movieInfo.name}</Title>
              <span>
                <Text strong>
                  Director:
                  <List
                    dataSource={movieInfo.directors}
                    renderItem={(item) => (
                      <List.Item>
                        <Link to={"/"}>
                          <span> {item.name}</span>
                        </Link>
                      </List.Item>
                    )}
                  />
                </Text>
              </span>
            </div>
            <div className="runtime">
              <Text>Runtime:{movieInfo.runtime} min(s)</Text>
            </div>
            <div className="genres">
              <Text>
                Genres:
                <List
                  dataSource={movieInfo.genres}
                  renderItem={(item) => (
                    <List.Item>
                      <Link to={"/"}>
                        <span> {item}</span>
                      </Link>
                    </List.Item>
                  )}
                />
              </Text>
            </div>
            <div className="actors">
              <Text>
                Actors:
                <List
                  dataSource={movieInfo.actors}
                  renderItem={(item) => (
                    <List.Item>
                      <span>
                        {item.name} ({item.character})
                      </span>
                    </List.Item>
                  )}
                />
              </Text>
            </div>
            <div className="release-time">
              <Text>release time: {movieInfo.release_time}</Text>
            </div>
            <div className="release-status">
              <Text>release status: {movieInfo.release_status}</Text>
            </div>
          </div>
          <div className="movie-rating">
            <span>
              <div className="rating-text">
                <Text>rating: </Text>
              </div>
              <Rate disabled defaultValue={3} />
              <div className="rating-number">
                <Text>{rating}</Text>
              </div>
            </span>
          </div>
        </div>
      </div>
      <div className="movie-recommendation">
        <RecommendationInMovie></RecommendationInMovie>
      </div>
      <div className="movie-review">
        <MovieReview id={id.replace("id=", "")} userInfo={userInfo} loginStatus={loginStatus} ></MovieReview>
      </div>


    </div>
  );
}

export default MovieDetail;
