import { Input, Select, Row, Col, Space, Tooltip, Divider } from "antd";
import { Image, Layout, Rate } from "antd";
import React, { Component, useState } from "react";
import { Typography } from "antd";
import "../css/MovieDetail.css";
import { useParams } from "react-router-dom";
import { useEffect } from "react";
import axios from "axios";

const { Header, Content, Footer } = Layout;
const desc = ["terrible", "bad", "normal", "good", "wonderful"];
const { Title, Text } = Typography;

function MovieDetail() {
  const [value, setValue] = useState(3);
  const state = {
    movies: [
      {
        id: "2",
        name: "Ariel",
        back_drop:
          "https://image.tmdb.org/t/p/w600_and_h900_bestv2/hQ4pYsIbP22TMXOUdSfC2mjWrO0.jpg",
        description:
          "Taisto Kasurinen is a Finnish coal miner whose father has just committed suicide and who is framed for a crime he did not commit. In jail, he starts to dream about leaving the country and starting a new life. He escapes from prison but things don't go as ",
        runtime: "73",
        release_time: "2001-01-10 00:00:00",
        release_status: "Released",
        total_rating: "4",
        rating_count: "0",
        director: "Pentti Auer",
        actor: "Matti Pellonpää",
        genres: "Western",
        reviews: "I like this",
      },
    ],
  };

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
      console.log(response.data.result);
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


  const { movies } = state;
  return (
    <div className="movie-detail-page">
      {movies.map((item) => (
        <div className="movie-detail">
          <div className="movie-image">
            <Image
              className="image"
              src={item.back_drop}
              alt="movie-image"
            ></Image>
          </div>
          <div className="movie-box">
            <div className="movie-title">
              <Title level={3}>Movie Name:{item.name}</Title>
              <span>
                <Text strong>Director: {item.director}</Text>
              </span>
            </div>
            <div className="runtime">
              <Text>Runtime:{item.runtime}</Text>
            </div>

            <div className="genres">
              <Text>Genres: {item.genres}</Text>
            </div>
            <div className="actors">
              <Text>Actors: {item.actor}</Text>
            </div>
            <div className="release-time">
              <Text>release time: {item.release_time}</Text>
            </div>
            <div className="release-status">
              <Text>release status: {item.release_status}</Text>
            </div>
          </div>
          <div className="movie-rating">
            <span>
              <div className="rating-text">
                <Text>rating</Text>
              </div>

              <Rate disabled defaultValue={item.total_rating} />
              <div className="rating-number">
                <Text>{item.total_rating}</Text>
              </div>
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}

export default MovieDetail;
