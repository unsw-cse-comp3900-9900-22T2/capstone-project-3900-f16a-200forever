import { useEffect, useState } from "react";
import {Button} from "@mui/material";
import axios from "axios";
import Card from '@mui/material/Card';
import Grid from '@mui/material/Grid';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import { useNavigate } from "react-router-dom";

const ForumHome = ({ setAlertInfo }) => {
	const navigate = useNavigate();
	const [genres, setGenres] = useState([]);

	useEffect( () => {
    axios
			.get("http://127.0.0.1:8080/genre/all", {
			})
			.then(function (response) {
				console.log(response.data);
				setGenres(response.data.genres);
			})
			.catch(function (error) {
				console.log(error.response);
				setAlertInfo({
					status: 3,
					msg: error.response.message,
				});
			});
  }, [])

	return (
		<>
			<Typography variant="h2" component="div" sx={{ mb: 4 }}>
				All Forums
			</Typography>
			<Grid container spacing={{ xs: 2, md: 3 }} columns={{ xs: 4, sm: 8, md: 12 }}>
				{genres.map((genre) => {
					return (
					<Grid item xs={2} sm={3} md={3}>
						<Card >
							<CardContent>
								<Typography variant="h5" component="div">
									{genre.name}
								</Typography>
							</CardContent>
							<CardActions>
								<Button 
									size="small"
									onClick={() => { navigate(`/forum/${genre.name.toLowerCase()}/${genre.id}`)}}>
									View Forum
								</Button>
							</CardActions>
						</Card>
					</Grid>)
				})}
			</Grid>
		</>
	)
};
  
export default ForumHome;