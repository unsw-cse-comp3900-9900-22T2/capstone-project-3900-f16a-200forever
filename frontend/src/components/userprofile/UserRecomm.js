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
import Checkbox from '@mui/material/Checkbox';
import FormGroup from '@mui/material/FormGroup';

const UserRecomm = ({ setAlertInfo }) => {
	const { id } = useParams();
	const [type, setType] = useState("genre");
	const [result, setResult] = useState([]);
	const [genreChecked, setGenreChecked] = useState(false);
	const [directorChecked, setDirectorChecked] = useState(false);

	const getList = () => {
		var param = {
			"user_id":id
		}
		if (genreChecked === true && directorChecked === false) {
			param['by'] = "genre"
		} else if (genreChecked === false && directorChecked === true) {
			param["by"] = "director"
		}
		
		axios.get("http://127.0.0.1:8080/recommendation/user",{
      params: param
    })
    .then(function(response){
      console.log(response.data)
			setResult(response.data.movies)
    })
    .catch(function(error){
      console.log(error.response)
    })
	}

	useEffect(() => {
		setAlertInfo({
			status: 1,
			msg: "Movies are coming",
		});
		getList();
	}, [genreChecked, directorChecked]);

	return (
		<>
			<Typography variant="h4" component="div" sx={{ mb: 5 }}>
				Guses what you like
			</Typography>
			{/* <FormControl>
				<FormLabel sx={{ mb: 1 }}>Recommend by</FormLabel>
				<RadioGroup
					row
					aria-labelledby="demo-row-radio-buttons-group-label"
					name="row-radio-buttons-group"
					onChange={(event) => { setType(event.target.value) }}
				>
					<FormControlLabel value="genre" control={<Radio />} label="Genre" />
					<FormControlLabel value="director" control={<Radio />} label="Director" />
				</RadioGroup>
			</FormControl> */}
			<FormLabel sx={{ mb: 1 }}>Recommend by</FormLabel>
			<FormGroup>
				<FormControlLabel control={<Checkbox onChange={(event) => {setGenreChecked(event.target.checked); getList() }}/> } label="genre" />
				<FormControlLabel control={<Checkbox onChange={(event) => {setDirectorChecked(event.target.checked); getList() }} />} label="director" />
			</FormGroup>

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