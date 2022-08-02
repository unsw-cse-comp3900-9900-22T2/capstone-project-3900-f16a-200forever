import { useEffect, useState } from "react";
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormHelperText from '@mui/material/FormHelperText';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Typography from '@mui/material/Typography';
import {Button} from "@mui/material";
import axios from "axios";
import Pagination from '@mui/material/Pagination';
import Grid from '@mui/material/Grid';
import MovieCard from "../movie/MovieCard";
import { useParams } from "react-router-dom";

const pageSize = 12;

function getResult(id, order, page, setResult, setTotal, setAlertInfo) {
  axios
    .get("http://127.0.0.1:8080/genre/genremovies", {
      params: {
        "genre_id": id,
        "num_per_page": pageSize,
        "order": order,
        "page": page
      }
    })
    .then(function (response) {
      console.log(response.data);
      setTotal(response.data.total_num);
      setResult(response.data.movies);
    })
    .catch(function (error) {
      console.log(error.response);
      setAlertInfo({
        status: 3,
        msg: "An error occur",
      });
    });
}

const GenreMovie = ({ setAlertInfo }) => {
  const { genre, id } = useParams();
	const [order, setOrder] = useState("descending");
	const [page, setPage] = useState(1);
	const [total, setTotal] = useState(0);
  const [result, setResult] = useState([]);

  useEffect(() => {
    getResult(id, order, 1, setResult, setTotal, setAlertInfo);
  }, [])

  return (
    <>
      <Typography variant="h4" component="div" sx={{ mb: 3 }}>
				Movies with genre: {genre}
			</Typography>
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
        <FormHelperText>rating order</FormHelperText>
      </FormControl>

			<Button variant="contained"
        onClick={() => { getResult(id, order, 1, setResult, setTotal, setAlertInfo) }}
        sx={{ mt: 2, ml: 2, mb: 5}}>
        Sort
      </Button>

      <Grid container spacing={{ xs: 2, md: 3 }} columns={{ xs: 4, sm: 8, md: 12 }}>
        {result.map((movie) => {
          return (<Grid item xs={2} sm={3} md={3}>
            <MovieCard data={movie}/>
          </Grid>)
        })}
      </Grid>
 
      {parseInt((total - 1) / pageSize) === 0 ?
        null:
        <Pagination 
          sx={{ mt: 3 }}
          count={parseInt((total - 1) / pageSize) + 1} page={page} 
          onChange={(event, value) => { setPage(value); getResult(id, order, page, setResult, setTotal, setAlertInfo); }}
          />
      }
		</>
  )
};

export default GenreMovie;