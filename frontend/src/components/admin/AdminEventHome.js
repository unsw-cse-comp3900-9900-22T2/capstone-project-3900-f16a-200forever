import { useEffect, useState } from "react";
import {Button} from "@mui/material";
import axios from "axios";
import Card from '@mui/material/Card';
import Grid from '@mui/material/Grid';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Fab from '@mui/material/Fab';
import AddIcon from '@mui/icons-material/Add';
import { useNavigate } from "react-router-dom";

const AdminEventHome = () => {
	const [events, setEvents] = useState([]);
	const navigate = useNavigate();

	useEffect(() => {
    axios
      .get("http://127.0.0.1:8080/event")
      .then(function (response) {
        console.log(response.data);
        setEvents(response.data.events)
      })
			// todo
      .catch(function (error) {
        console.log(error.response);
      });
  }, []);

	return (
		<>
			<Typography variant="h2" component="div" sx={{ mb: 4 }}>
				All Events
				{/* todo */}
				<Fab color="primary" aria-label="add" sx={{ ml: 5 }}>
					<AddIcon />
				</Fab>
			</Typography>
			<Grid container spacing={{ xs: 2, md: 3 }} columns={{ xs: 4, sm: 8, md: 12 }}>
				{events.map((event) => {
					return (
						<Grid item xs={12}>
							<Card >
								<CardContent>
									<Typography variant="h5" component="div">
										Topic: {event.topic}
									</Typography>
									<Typography variant="h6" component="div">
										Status: {event.event_status}
									</Typography>
									<Typography variant="caption" component="div">
										deadline: {event.deadline}
									</Typography>
									<Typography variant="body2" component="div">
										{event.description}
									</Typography>
								</CardContent>
								<CardActions>
									<Button 
										size="small"
										onClick={() => { navigate(`/admin/event/${event.id}`)}}>
										View More
									</Button>
								</CardActions>
							</Card>
						</Grid>	
					)
				})}
			</Grid>
		</>
	)
};

export default AdminEventHome;