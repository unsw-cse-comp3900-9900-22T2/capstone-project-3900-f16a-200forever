import axios from "axios";
import { useEffect, useState } from "react";
import MovieCard from "../movie/MovieCard";
import Grid from '@mui/material/Grid';
import Typography from "@mui/material/Typography";

const Home = () => {
  const [result, setResult] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8080/recommendation/genre",{
      params:{
        "movie_id": 2,
      }
    })
      .then(function (response) {
        const temp = response.data.movies.splice(0, 20)
        setResult(temp)
      })
      .catch(function (error) {
        console.log(error.response);
      });
  }, [])

  return (
    <>
      <Typography variant="h4" component="div" sx={{ mb: 3 }}>
          Welcome!!!
        </Typography>

        <Grid container spacing={{ xs: 2, md: 3 }} columns={{ xs: 4, sm: 8, md: 12 }}>
          {result.map((movie) => {
            return (<Grid item xs={2} sm={3} md={3}>
              <MovieCard data={movie}/>
            </Grid>)
          })}
        </Grid>
    </>
  )
};

export default Home;