import { Image, Layout, Rate } from "antd";
import React, { useState } from "react";
import { Typography } from "antd";
import "../css/MovieDetail.css";
import { useParams } from "react-router-dom";
import { useEffect } from "react";
import axios from "axios";

const { Header, Content, Footer } = Layout;
const desc = ["terrible", "bad", "normal", "good", "wonderful"];
const { Title, Text } = Typography;

function MovieDetail() {
  const { id } = useParams();
  const [movieInfo, setMovieInfo] = useState({})
  useEffect (() => {
    axios
    // todo change url here
    .get("http://127.0.0.1:5000/test2", {
      params: {
        "id": id.replace("id=", "")
      }
    })
    .then(function (response) {
      console.log(response.data);
      setMovieInfo(response.data);
    })
    // todo handle error
    .catch(function (error) {
      console.log(error.response);
      // openNotification({
      //   "title": "Search error",
      //   "content": error
      // })
    });
  }, [])

  return (
    <div className="movie-detail-page">
      <div className="movie-detail">
        <div className="movie-image">
          <Image
            className="image"
            src={movieInfo.img}
            alt="movie-image"
          ></Image>
        </div>
        <div className="movie-box">
          <div className="movie-title">
            <Title level={3}>Movie Name:{movieInfo.title}</Title>
            <span>
              <Text strong>Director: {movieInfo.director}</Text>
            </span>
          </div>
          <div className="runtime">
            <Text>Runtime:{movieInfo.runtime}</Text>
          </div>

          <div className="genres">
            <Text>Genres: {movieInfo.genres}</Text>
          </div>
          <div className="actors">
            <Text>Actors: {movieInfo.actor}</Text>
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
              <Text>rating</Text>
            </div>

            <Rate disabled defaultValue={movieInfo.rating} />
            <div className="rating-number">
              <Text>{movieInfo.rating}</Text>
            </div>
          </span>
        </div>
      </div>
    </div>
  );
}

export default MovieDetail;
