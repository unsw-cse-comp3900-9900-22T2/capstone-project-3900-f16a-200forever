import axios from "axios";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Box from '@mui/material/Box';
import image from "../../asset/NoMovieImg.png";
import Container from '@mui/material/Container';
import Rating from '@mui/material/Rating';
import { useNavigate } from "react-router-dom";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import SendIcon from '@mui/icons-material/Send';
import Button from "@mui/material/Button";
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormHelperText from '@mui/material/FormHelperText';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { Paper } from "@mui/material";
import Pagination from '@mui/material/Pagination';

import Grid from '@mui/material/Grid';
import MovieCard from "./MovieCard";
import MovieReview from "./MovieReview";
  
const pageSize = 20;

const MovieDetails = ({ setAlertInfo }) => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [movieInfo, setMovieInfo] = useState({ directors: [], actors: [], genres: [] });
  const [recomm, setRecomm] = useState([]);
  const [review, setReview] = useState("");
  const [rating, setRating] = useState(0);
  const [page, setPage] = useState(1);
  const [order, setOrder] = useState("descending");
  const [result, setResult] = useState([]);
  const [type, setType] = useState("time");
  const [total, setTotal] = useState(0);

  function getReviews(type, order, page, setResult, setTotal, setAlertInfo) {
    axios
      .get("http://127.0.0.1:8080/review/sort", {
        params: {
          movie_id: id,
          type: type,
          order: order,
          num_per_page: pageSize,
          page: page,
        },
      })
      .then(function (response) {
        console.log(response.data);
        setTotal(response.data.total);
        setResult(response.data.reviews);
      })
      .catch(function (error) {
        console.log(error.response);
        setAlertInfo({
          status: 3,
          msg: "An error occur",
        });
      });
  }

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

    axios.get("http://127.0.0.1:8080/recommendation/genre",{
      params:{
        "movie_id": id,
      }
    })
      .then(function (response) {
        const temp = response.data.movies.splice(0, 8)
        setRecomm(temp)
      })
      .catch(function (error) {
        console.log(error.response);
      });
    getReviews(type, order, page, setResult, setTotal, setAlertInfo)
  }, [])

  const addToList = (option) => {
    if (localStorage.getItem("token") === null) {
      setAlertInfo({
        status: 2,
        msg: "Please login",
      });
      return;
    }
    var type = "";
    if (option === 0) {
      type = "wishlist"
    } else if (option === 1) {
      type = "watchedlist"
    } else {
      type = "droppedlist"
    }
    axios
      .post(`http://127.0.0.1:8080/user/${type}`, {
        email: localStorage.getItem("email"),
        token: localStorage.getItem("token"),
        movie_id: parseInt(id)
      })
      .then(function (response) {
        console.log(response);
        setAlertInfo({
          status: 1,
          msg: response.data.message
        })
      })
      .catch(function (error) {
        console.log(error.response.data);
        setAlertInfo({
          status: 3,
          msg: error.response.data.message,
        });
      });
  }

  const sendReview = () => {
    if (!review.replace(/\s/g, "").length || rating === null) {
      setAlertInfo({
        status: 2,
        msg: "Please enter valid review",
      });
      return;
    }
    setAlertInfo({
      status: 2,
      msg: "Sending"
    });
    axios
      .post("http://127.0.0.1:8080/review", {
        movie_id: parseInt(id),
        email: localStorage.getItem("email"),
        token: localStorage.getItem("token"),
        rating: parseInt(rating),
        review_content: review
      })
      .then(function (response) {
        console.log(response);
        setAlertInfo({
          status: 1,
          msg: "Successfully"
        });
        navigate(0);
      })
      .catch(function (error) {
        console.log(error.response.data);
        setAlertInfo({
          status: 3,
          msg: error.response.data.message
        });
      });
  }

  return (
    <>
    <Box sx={{ flexGrow: 1}} >
      <Grid spacing={2}>
        <Paper elevation={6}>
          <Grid container item xs={12} direction="row" justifyContent="space-between" alignItems="flex-start">
            <Grid container item xs={8}>
              <Grid item xs={12}>
                <Typography gutterBottom variant="h4" component="div" sx={{ ml: 4, mt: 4}}>
                  {movieInfo.title}
                </Typography>
              </Grid>
              <Grid item xs={3}>
                <Rating 
                  value={parseInt(movieInfo.total_rating / movieInfo.rating_count)} 
                  disabled
                  size="large"
                  sx={{ ml: 4 }}
                />
              </Grid>
              <Grid item xs={9}>
                <Typography gutterBottom variant="body2" component="div" sx={{ mt: 1 }}>
                  ({movieInfo.rating_count})
                </Typography>
              </Grid>

              <Grid item xs={12} sx={{ ml: 4, mt: 2}}>
                <Typography gutterBottom variant="h6" component="div">
                  Runtime: {movieInfo.runtime} min(s)
                </Typography>
              </Grid>

              <Grid item xs={12} sx={{ ml: 4, mt: 2}}>
                <Typography gutterBottom variant="h6" component="div">
                  Release_status: {movieInfo.release_status}
                </Typography>
              </Grid>

              <Grid item xs={12} sx={{ ml: 4, mt: 2, mr: 2}}>
                <Typography gutterBottom variant="h6" component="div">
                  Description: {movieInfo.description}
                </Typography>
              </Grid>

              <Grid item xs={12} sx={{ ml: 4, mt: 2, mr: 2}}>
                <Typography gutterBottom variant="h6" component="div">
                  Tagline: {movieInfo.tagline}
                </Typography>
              </Grid>

              <Grid item xs={12} sx={{ ml: 4, mt: 2, mb: 2}}>
                <Typography gutterBottom variant="h6" component="div">
                  Genre(s):
                </Typography>
              </Grid>
              {
                movieInfo.genres.map((genre) => {
                  return (
                    <Grid item xs={12}>
                      <Typography gutterBottom variant="body1" component="div" sx={{ ml: 8}}>
                        {genre}
                      </Typography>
                    </Grid>
                  )
                })
              }

              <Grid item xs={12} sx={{ ml: 4, mt: 2, mb: 2}}>
                <Typography gutterBottom variant="h6" component="div">
                  Director(s):
                </Typography>
              </Grid>
              {
                movieInfo.directors.map((director) => {
                  return (
                    <Grid item xs={12}>
                      <Typography gutterBottom variant="body1" component="div" sx={{ ml: 8}}>
                        {director.name}
                      </Typography>
                    </Grid>
                  )
                })
              }

              <Grid item xs={12} sx={{ ml: 4, mt: 2, mb: 2}}>
                <Typography gutterBottom variant="h6" component="div">
                  Actor(s)
                </Typography>
              </Grid>
              <Grid item xs={5} sx={{ ml: 8, mb: 2}}>
                name
              </Grid>
              <Grid item xs={5} sx={{ mb: 2}}>
                character
              </Grid>
              {
                movieInfo.actors.map((actor) => {
                  return (
                    <>
                      <Grid item xs={5}>
                        <Typography gutterBottom variant="body1" component="div" sx={{ ml: 8}}>
                          {actor.name}
                        </Typography>
                      </Grid>
                      <Grid item xs={5}>
                        <Typography gutterBottom variant="body1" component="div" sx={{ ml: 8}}>
                          {actor.character}
                        </Typography>
                      </Grid>
                    </>
                  )
                })
              }
              <Grid item xs={12}/>
            </Grid>
  
            <Grid container item xs={4}direction="column" justifyContent="flex-start" alignItems="center">
              <Grid item xs={12}>
                <Box
                  component="img"
                  sx={{
                    height: 600,
                    width: 400
                  }}
                  src={movieInfo.backdrop === null ? image : movieInfo.backdrop}
                />
              </Grid>

              <Grid xs={12}>
                <Button variant="contained" onClick={() => { addToList(0)}} sx={{ minWidth: 230, mt: 5 }}>
                  add to wishlist
                </Button>
              </Grid>
              <Grid xs={12}>
                <Button variant="contained" onClick={() => { addToList(1)}} sx={{ minWidth: 230, mt: 3 }}>
                  add to watched list
                </Button>
              </Grid>
              <Grid xs={12}>
                <Button variant="contained" onClick={() => { addToList(2)}} sx={{ minWidth: 230, mt: 3 }}>
                  add to drop list
                </Button>
              </Grid>
            </Grid>         
          </Grid>
        </Paper>
        <Paper elevation={6} sx={{ mt: 4 }}>
          <Grid container item xs={12} direction="row" justifyContent="space-between" alignItems="flex-start">
            <Grid item xs={12}>
              <Typography gutterBottom variant="h4" component="div" sx={{ ml: 4, mt: 4}}>
                Related movies
              </Typography>
            </Grid>
            {
              recomm.map((movie) => {
                return (
                  <Grid item xs={3} sx={{ mb: 2}}>
                    <MovieCard data={movie}></MovieCard>
                  </Grid>
                )
              })
            }
          </Grid>
        </Paper>
        
        <Paper elevation={6} sx={{ mt: 4 }}>
          <Grid container item xs={12} direction="row" justifyContent="space-between" alignItems="flex-start">
            
            <Grid item xs={8}>
              <TextField
                margin="normal"
                required
                fullWidth
                id="review"
                label="Review"
                name="review"
                multiline
                rows={2}
                sx={{ ml: 4 }}
                onChange={(event) => { setReview(event.target.value) }}
              />
            </Grid>
            <Grid item xs={4}/>
            <Grid item xs={2}>
              <Rating
                value={rating}
                size="large"
                sx={{ ml: 5}}
                onChange={(event, newValue) => {
                  if (newValue === null) {
                    setRating(0);
                    return;
                  }
                  setRating(newValue);
                }}
              />
            </Grid>
            <Grid item xs={10}>
              <Button
                variant="text"
                type="submit"
                size="large"
                endIcon={<SendIcon />}
                onClick={sendReview}
              >
                POST
              </Button>
            </Grid>
            <Grid item xs={12}>
              <Typography gutterBottom variant="h4" component="div" sx={{ ml: 4, mt: 4}}>
                Reviews
              </Typography>
            </Grid>
            <Grid item xs={12}>
            <FormControl sx={{ m: 1, minWidth: 150 }}>
              <InputLabel id="search-tag">Sort by</InputLabel>
              <Select
                value={type}
                label="Sort by"
                onChange={(event) => { setType(event.target.value) }}
              >
                <MenuItem value={"time"}>time</MenuItem>
                <MenuItem value={"likes"}>likes</MenuItem>
              </Select>
            </FormControl>

            <FormControl sx={{ m: 1, minWidth: 150 }}>
              <InputLabel id="search-order">By</InputLabel>
              <Select
                value={order}
                onChange={(event) => { setOrder(event.target.value) }}
                label="By"
                displayEmpty
              >
                <MenuItem value={"descending"}>descending</MenuItem>
                <MenuItem value={"ascending"}>ascending</MenuItem>
              </Select>
              <FormHelperText>order</FormHelperText>
            </FormControl>
            <Button variant="contained"
              onClick={() => { getReviews(type, order, 1, setResult, setTotal, setAlertInfo)}}
              sx={{ ml: 2, mt: 3}}>
              Sort
            </Button>

            </Grid>

            {
              result.map((r) => {
                return (
                  <Grid item xs={12}>
                  <MovieReview review={r} setAlertInfo={setAlertInfo}></MovieReview>
                  </Grid>
                )
              })
            }
            {parseInt((total - 1) / pageSize) === 0 ?
              null:
              <Pagination 
                sx={{ mt: 3 }}
                count={parseInt((total - 1) / pageSize) + 1} page={page} 
                onChange={(event, value) => { setPage(value); getReviews(type, order, value, setResult, setTotal, setAlertInfo); }}/>
            }
          </Grid>
        </Paper>

      </Grid>
    </Box>
    </>
  )
};
  
  export default MovieDetails;