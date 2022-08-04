import { useParams } from "react-router-dom";
import Typography from "@mui/material/Typography";
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import { useEffect, useState } from "react";
import axios from "axios";
import Grid from '@mui/material/Grid';
import MovieCard from "../movie/MovieCard";

const UserRecomm = ({ setAlertInfo }) => {
	const { id } = useParams();
	const [type, setType] = useState("genre");
	const [result, setResult] = useState([]);
	
	useEffect(() => {
		setAlertInfo({
			status: 1,
			msg: "Movies are coming",
		});
		axios.get("http://127.0.0.1:8080/recommendation/user",{
      params:{
        "user_id":id,
        "by": type
      }
    })
    .then(function(response){
      console.log(response.data)
			setResult(response.data.movies)
    })
    .catch(function(error){
      console.log(error.response)
    })
	}, [type]);

	return (
		<>
			<Typography variant="h4" component="div" sx={{ mb: 5 }}>
				Guses what you like
			</Typography>
			<FormControl>
				<FormLabel id="demo-row-radio-buttons-group-label" sx={{ mb: 1 }}>Recommend by</FormLabel>
				<RadioGroup
					row
					aria-labelledby="demo-row-radio-buttons-group-label"
					name="row-radio-buttons-group"
					onChange={(event) => { setType(event.target.value) }}
				>
					<FormControlLabel value="genre" control={<Radio />} label="Genre" />
					<FormControlLabel value="director" control={<Radio />} label="Director" />
				</RadioGroup>
			</FormControl>
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

export default UserRecomm;