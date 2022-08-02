import axios from "axios";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Box from '@mui/material/Box';
import image from "../../asset/NoMovieImg.png";
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';

const MovieDetails = ({ setAlertInfo }) => {
  const { id } = useParams();
  const [movieInfo, setMovieInfo] = useState({});

  useEffect (() => {
    axios
    .get("http://127.0.0.1:8080/movie/moviedetails", {
      params: {
        "movie_id": id,
      }
    })
    .then(function (response) {
      console.log(response.data);
      setMovieInfo(response.data);
    })
    .catch(function (error) {
      console.log(error.response);
      setAlertInfo({
        status: 3,
        msg: "An error when getting movie details.",
      });
    });
  }, [])

  return (
    <>
    <Box sx={{ flexGrow: 3 }}>
      <Box component="div">
        <Typography component="legend">Rating: </Typography>
      </Box>
      <Box
        component="img"
        sx={{
          height: 600,
          width: 400
        }}
        src={movieInfo.backdrop === null ? image : movieInfo.backdrop}
      />
    </Box>
    
    </>
  )
};
  
  export default MovieDetails;