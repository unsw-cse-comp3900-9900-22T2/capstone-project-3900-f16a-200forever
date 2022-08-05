import { useNavigate, useParams } from "react-router-dom";
import MenuItem from "@mui/material/MenuItem";
import TextField from "@mui/material/TextField";
import { useEffect, useState } from "react";
import Typography from '@mui/material/Typography';
import axios from "axios";
import { Box, Button, Paper, Select, InputLabel,ImageListItem, ImageList } from "@mui/material";
import Stack from '@mui/material/Stack';
import { styled } from '@mui/material/styles';


const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'left',
  color: theme.palette.text.secondary,
}));

const AdminEventDetail = ({ setAlertInfo }) => {
	const { id } = useParams();
	const [info, setInfo] = useState({ movies: [], questions: [] })
	const [test, setTest] = useState("");
	const navigate = useNavigate();
	
	useEffect( () => {
		axios
			.get("http://127.0.0.1:8080/event/detail", {
				params: {
					id: id
				}
			})
			.then(function (response) {
				console.log(response.data);
				setInfo(response.data)
				setTest(response.data.topic)
			})
			.catch(function (error) {
				console.log(error.response);
				setAlertInfo({
					status: 3,
					msg: error.response.data.message
				});
			});
	}, []);

	const submit = (event) => {
		console.log(info.topic)	
		console.log(test)
	}

  return (
		<>
			<Typography variant="h4" component="div" sx={{ mb: 4 }}>
				Event details
			</Typography>
			<Paper
        elevation={1}>
				<Box
          noValidate
          autoComplete="off"
        >
					<Typography variant="h5" component="div" sx={{ mb: 4 }}>
						Topic: {info.topic}
					</Typography>
					<Typography variant="h7" component="div" sx={{ mb: 4 }}>
						Status: {info.event_status}
					</Typography>
					<Typography variant="h7" component="div" sx={{ mb: 4 }}>
						Duration: {info.duration} min(s)
					</Typography>
					<Typography variant="h6" component="div" sx={{ }}>
						Movies:
					</Typography>
					<Box sx={{ width: '70%' }}>
						<Stack spacing={2} sx={{ ml: 4 }}>
							{info.movies.map((movie) => {
							return (
								<Item>
									id: {movie.id}&nbsp;&nbsp;&nbsp;&nbsp;Title: {movie.name}
								</Item>
							)  
						})}
						</Stack>
					</Box>
					<Typography variant="h7" component="div" sx={{ mt: 4, mb: 4 }}>
						Deadline: {info.deadline}
					</Typography>
					<Typography variant="h6" component="div" sx={{ mt: 4, mb: 4 }}>
						Description: {info.description}
					</Typography>
					<Typography variant="h6" component="div" sx={{ mb: 4 }}>
						Badge:
						<ImageList sx={{ width: 200, height: 200 }} cols={1} rowHeight={200}>
							<ImageListItem>
								<img
									src={info.image}
									loading="lazy"
								/>
							</ImageListItem>
						</ImageList>
					</Typography>
					<Typography variant="h6" component="div" sx={{ mt: 4, mb: 4 }}>
						Questions
					</Typography>
					{info.questions.map((q) => {
						return (
							<>
							<Typography variant="h6" component="div" sx={{ ml: 4, mt: 4, mb: 4 }}>
								id: {q.id}
							</Typography>
							<Typography variant="h6" component="div" sx={{ ml: 4, mt: 4, mb: 4 }}>
								Question: {q.question}
							</Typography>
							{q.choices.map((c) => {
								return (
									<Typography variant="h7" component="div" sx={{ ml: 8, mt: 4 }}>
										choice {c.num}: {c.choice} 
									</Typography>
								)
							})}
							</>
						)
					})}
        </Box>
			</Paper>
		</>
  )
};

export default AdminEventDetail;


{/* <TextField
margin="normal"
required
fullWidth
id="topic"
label="Topic"
name="topic"
defaultValue={info.topic}
/>
<InputLabel id="demo-simple-select-label">Duration</InputLabel>
<Select
	value={parseInt(info.duration)}
	label="Duration"
	onChange={(event) => {
		var temp = info
		temp.duration = event.target.value
		setInfo(temp);
	}}
>
	<MenuItem value={10}>10</MenuItem>
	<MenuItem value={20}>20</MenuItem>
	<MenuItem value={30}>30</MenuItem>
	<MenuItem value={60}>60</MenuItem>
</Select>
<Button onClick={submit} fullWidth variant="contained" sx={{ mt: 3 }}>
Login
</Button> */}