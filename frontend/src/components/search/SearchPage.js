import { useState } from "react";
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormHelperText from '@mui/material/FormHelperText';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import TextField from '@mui/material/TextField';
import {Button} from "@mui/material";
import axios from "axios";
import Pagination from '@mui/material/Pagination';
import Grid from '@mui/material/Grid';
import MovieCard from "../movie/MovieCard";

const pageSize = 12;

function getResult(searchTag, order, keywords, page, setResult, setTotal, setAlertInfo) {
  if (!keywords.replace(/\s/g, "").length) {
    setAlertInfo({
      status: 2,
      msg: "Please enter valid keywords",
    });
    return;
  }

  var param = {
    type: searchTag,
    keywords: keywords,
    order: order,
    num_per_page: pageSize,
    page: page
  }
  if (localStorage.getItem("id") !== null) {
    param.user_id = localStorage.getItem("id")
  }
  axios
    .get("http://127.0.0.1:8080/movie/search", {
      params: param
    })
    .then(function (response) {
      console.log(response.data);
      setTotal(response.data.total);
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

const SearchPage = ({ setAlertInfo }) => {
	
  const [searchTag, setSearchTag] = useState("movie name");
	const [order, setOrder] = useState("descending");
	const [keywords, setKeywords] = useState("");
	const [page, setPage] = useState(1);
	const [total, setTotal] = useState(0);
  const [result, setResult] = useState([]);

  return (
		<>
      <FormControl sx={{ m: 1, minWidth: 150 }}>
        <InputLabel id="search-tag">Search Tag</InputLabel>
        <Select
          labelId="demo-simple-select-helper-label"
          id="demo-simple-select-helper"
          value={searchTag}
          label="Search tag"
          onChange={(event) => { setSearchTag(event.target.value) }}
        >
          <MenuItem value={"movie name"}>movie name</MenuItem>
          <MenuItem value={"description"}>description</MenuItem>
          <MenuItem value={"director"}>director</MenuItem>
        </Select>
        <FormHelperText>Search option</FormHelperText>
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
        <FormHelperText>rating order</FormHelperText>
      </FormControl>

			<TextField 
				id="search-keywords" 
				label="Keywords" 
				variant="standard" 
				onChange={(event) => { setKeywords(event.target.value)}}
				sx={{ mt: 2, ml: 3, minWidth: 400 }} />

			<Button variant="contained"
        onClick={() => { getResult(searchTag, order, keywords, 1, setResult, setTotal, setAlertInfo)}}
        sx={{ mt: 4, ml: 2, mb: 5}}>
        Search
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
          onChange={(event, value) => { setPage(value); getResult(searchTag, order, keywords, value, setResult, setTotal, setAlertInfo); }}/>
      }
		</>
	)
};
export default SearchPage;