//https://github.com/codermother/Movie-Rating-App/blob/master/src/components/MovieCard/MovieCard.js


import React from "react";
import { Link } from "react-router-dom";
import "./MovieCard.scss";

function MovieCard(props) {
  const { data } = props;
  return (
    <div className="card-item">
      <Link to={`/movie/${data.imdbID}`}>
        <div className="card-inner">
          <div className="card-top">
            <img src={data.Poster} alt={data.Title} />
          </div>
        </div>
        <div className="card-bottom">
          <div className="card-info">
            <h4>{data.Title}</h4>
            <p>{data.Year}</p>
          </div>
        </div>
      </Link>
    </div>
  );
}

export default MovieCard;