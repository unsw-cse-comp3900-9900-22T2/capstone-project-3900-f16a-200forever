import { useNavigate, useParams } from "react-router-dom";
import TextField from "@mui/material/TextField";
import { useEffect, useState } from "react";
import Typography from '@mui/material/Typography';
import axios from "axios";
import { Box, Button, Paper,ImageListItem, ImageList } from "@mui/material";
import Stack from '@mui/material/Stack';
import { styled } from '@mui/material/styles';
import Grid from '@mui/material/Grid';
import FormHelperText from '@mui/material/FormHelperText';

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'left',
  color: theme.palette.text.secondary,
}));

const EventDetail = ({ setAlertInfo }) => {
	const { id } = useParams();
	const [info, setInfo] = useState({ movies: [], questions: [] })
	const [begin, setBegin] = useState(false);
	// const [test, setTest] = useState("");
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
				// setTest(response.data.topic)
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
		event.preventDefault();
    const data = new FormData(event.currentTarget);
		const body = {
			email: localStorage.getItem("email"),
			token: localStorage.getItem("token"),
			event_id: id,
			answers: {}
		}
		body.answers[info.questions[0].id] = data.get("q1a");
		body.answers[info.questions[1].id] = data.get("q2a");
		body.answers[info.questions[2].id] = data.get("q3a");
		body.answers[info.questions[3].id] = data.get("q4a");
		body.answers[info.questions[4].id] = data.get("q5a");
		axios
			.post("http://127.0.0.1:8080/event/finish", body)
			.then(function (response) {
				console.log(response);
				setAlertInfo({
					status: 1,
					msg: "Congrats! You passed!"
				});
				navigate("/events");
			})
			.catch(function (error) {
				console.log(error.response.data);
				setAlertInfo({
					status: 3,
					msg: error.response.data.message,
				});
				navigate("/events")
			});
	}

	const attemp = () => {
		setAlertInfo({
			status: 2,
			msg: "operating"
		});
		axios
			.post("http://127.0.0.1:8080/event/attemp", {
				email: localStorage.getItem("email"),
				token: localStorage.getItem("token"),
				event_id: id
			})
			.then(function (response) {
				console.log(response);
				setBegin(true);
			})
			.catch(function (error) {
				console.log(error.response.data);
				setAlertInfo({
					status: 3,
					msg: error.response.data.message,
				});
			});
	}

  return (
		<>
			{
				begin === false ?
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
							<ImageList sx={{ width: 200, height: 200, ml: 8 }} cols={1} rowHeight={200}>
								<ImageListItem>
									<img
										src={info.image}
										loading="lazy"
									/>
								</ImageListItem>
							</ImageList>
						</Typography>
						<Button sx={{ ml:20, mb: 5 }} variant="contained" onClick={attemp}>attemp</Button>
					</Box>
				</Paper>
				</>
				:
				<Box
				component="form"
				noValidate
				autoComplete="off"
				onSubmit={submit}
				sx={{ flexGrow: 1 }}
			>
				<Grid container spacing={2}>
					<Grid item xs={12}>
						<Typography
							component="h1"
							variant="h4"
							fontWeight="bold"
							sx={{ textAlign: "center" }}
							fontFamily="inherit"
						>
							Attending
						</Typography>
					</Grid>
					<Grid item xs={2}/>
					<Grid item xs={6}>
						<TextField
							disabled
							margin="normal"
							required
							fullWidth
							id="topic"
							label="Topic"
							name="topic"
							defaultValue={info.topic}
						/>
					</Grid>
					<Grid item xs={2}>
					</Grid>
					<Grid item xs={2}/>
	
					<Grid item xs={2}/>
					<Grid item xs={2}>
						<TextField
							disabled
							margin="normal"
							required
							fullWidth
							id="duration"
							label="Duration in mins"
							name="duration"
							defaultValue={info.duration}
						/>
					</Grid>
					<Grid item xs={3}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="deadline"
							label="Deadline yyyy-mm-dd"
							name="deadline"
							disabled
							defaultValue={info.deadline}
						/>
					</Grid>
					<Grid item xs={3}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="movie"
							label="Movie id"
							name="movie"
							disabled
							defaultValue={info.movies[0].id}
						/>
					</Grid>
					<Grid item xs={2}/>
	
					<Grid item xs={2}/>
					<Grid item xs={8}>
						<TextField
							disabled
							defaultValue={info.description}
							margin="normal"
							required
							fullWidth
							id="description"
							label="Description"
							name="description"
							multiline
							rows={2}
						/>
					</Grid>
					<Grid item xs={2}/>
	
					<Grid item xs={2}/>
					<Grid item xs={8}>
						<Typography variant="h4" component="div">
							Questions
						</Typography>
					</Grid>
					<Grid item xs={2}/>
	
					<Grid item xs={2}/>
					<Grid item xs={8}>
						<Typography variant="h5" component="div">
							Question1
						</Typography>
					</Grid>
					<Grid item xs={2}/>
	
					<Grid item xs={2}/>
					<Grid item xs={8}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q1"
							label="Question1"
							name="q1"
							multiline
							rows={2}
							disabled
							defaultValue={info.questions[0].question}
						/>
					</Grid>
					<Grid item xs={2}/>
	
					<Grid item xs={2}/>
					<Grid item xs={4}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q1c1"
							label="Choice 1"
							name="q1c1"
							disabled
							defaultValue={info.questions[0].choices[0].choice}
						/>
					</Grid>
					<Grid item xs={4}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q1c2"
							label="Choice 2"
							name="q1c2"
							disabled
							defaultValue={info.questions[0].choices[1].choice}
						/>
					</Grid>
					<Grid item xs={2}/>
	
					<Grid item xs={2}/>
					<Grid item xs={4}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q1c3"
							label="Choice 3"
							name="q1c3"
							disabled
							defaultValue={info.questions[0].choices[2].choice}
						/>
					</Grid>
					<Grid item xs={4}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q1a"
							label="Seq of correct"
							name="q1a"
						/>
						<FormHelperText>Enter 1 if choice 1 is correct</FormHelperText>
					</Grid>
					<Grid item xs={2}/>
	
					<Grid item xs={2}/>
					<Grid item xs={8}>
						<Typography variant="h5" component="div">
							Question2
						</Typography>
					</Grid>
					<Grid item xs={2}/>
	
					<Grid item xs={2}/>
					<Grid item xs={8}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q2"
							label="Question2"
							name="q2"
							multiline
							rows={2}
							disabled
							defaultValue={info.questions[1].question}
						/>
					</Grid>
					<Grid item xs={2}/>
	
					<Grid item xs={2}/>
					<Grid item xs={4}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q2c1"
							label="Choice 1"
							name="q2c1"
							disabled
							defaultValue={info.questions[1].choices[0].choice}
						/>
					</Grid>
					<Grid item xs={4}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q2c2"
							label="Choice 2"
							name="q2c2"
							disabled
							defaultValue={info.questions[1].choices[1].choice}
						/>
					</Grid>
					<Grid item xs={2}/>
	
					<Grid item xs={2}/>
					<Grid item xs={4}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q2c3"
							label="Choice 3"
							name="q2c3"
							disabled
							defaultValue={info.questions[1].choices[2].choice}
						/>
					</Grid>
					<Grid item xs={4}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q2a"
							label="Seq of correct"
							name="q2a"
						/>
						<FormHelperText>Enter 1 if choice 1 is correct</FormHelperText>
					</Grid>
					<Grid item xs={2}/>
	
					<Grid item xs={2}/>
					<Grid item xs={8}>
						<Typography variant="h5" component="div">
							Question3
						</Typography>
					</Grid>
					<Grid item xs={2}/>
	
					<Grid item xs={2}/>
					<Grid item xs={8}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q3"
							label="Question3"
							name="q3"
							multiline
							rows={2}
							disabled
							defaultValue={info.questions[2].question}
						/>
					</Grid>
					<Grid item xs={2}/>
	
					<Grid item xs={2}/>
					<Grid item xs={4}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q3c1"
							label="Choice 1"
							name="q3c1"
							disabled
							defaultValue={info.questions[2].choices[0].choice}
						/>
					</Grid>
					<Grid item xs={4}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q3c2"
							label="Choice 2"
							name="q3c2"
							disabled
							defaultValue={info.questions[2].choices[1].choice}
						/>
					</Grid>
					<Grid item xs={2}/>
	
					<Grid item xs={2}/>
					<Grid item xs={4}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q3c3"
							label="Choice 3"
							name="q3c3"
							disabled
							defaultValue={info.questions[2].choices[2].choice}
						/>
					</Grid>
					<Grid item xs={4}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q3a"
							label="Seq of correct"
							name="q3a"
						/>
						<FormHelperText>Enter 1 if choice 1 is correct</FormHelperText>
					</Grid>
					<Grid item xs={2}/>
	
					<Grid item xs={2}/>
					<Grid item xs={8}>
						<Typography variant="h5" component="div">
							Question4
						</Typography>
					</Grid>
					<Grid item xs={2}/>
	
					<Grid item xs={2}/>
					<Grid item xs={8}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q4"
							label="Question4"
							name="q4"
							multiline
							rows={2}
							disabled
							defaultValue={info.questions[3].question}
						/>
					</Grid>
					<Grid item xs={2}/>
	
					<Grid item xs={2}/>
					<Grid item xs={4}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q4c1"
							label="Choice 1"
							name="q4c1"
							disabled
							defaultValue={info.questions[3].choices[0].choice}
						/>
					</Grid>
					<Grid item xs={4}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q4c2"
							label="Choice 2"
							name="q4c2"
							disabled
							defaultValue={info.questions[3].choices[1].choice}
						/>
					</Grid>
					<Grid item xs={2}/>
	
					<Grid item xs={2}/>
					<Grid item xs={4}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q4c3"
							label="Choice 3"
							name="q4c3"
							disabled
							defaultValue={info.questions[3].choices[2].choice}
						/>
					</Grid>
					<Grid item xs={4}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q4a"
							label="Seq of correct"
							name="q4a"
						/>
						<FormHelperText>Enter 1 if choice 1 is correct</FormHelperText>
					</Grid>
					<Grid item xs={2}/>
	
					<Grid item xs={2}/>
					<Grid item xs={8}>
						<Typography variant="h5" component="div">
							Question5
						</Typography>
					</Grid>
					<Grid item xs={2}/>
	
					<Grid item xs={2}/>
					<Grid item xs={8}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q5"
							label="Question5"
							name="q5"
							multiline
							rows={2}
							disabled
							defaultValue={info.questions[4].question}
						/>
					</Grid>
					<Grid item xs={2}/>
	
					<Grid item xs={2}/>
					<Grid item xs={4}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q5c1"
							label="Choice 1"
							name="q5c1"
							disabled
							defaultValue={info.questions[4].choices[0].choice}
						/>
					</Grid>
					<Grid item xs={4}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q5c2"
							label="Choice 2"
							name="q5c2"
							disabled
							defaultValue={info.questions[4].choices[1].choice}
						/>
					</Grid>
					<Grid item xs={2}/>
	
					<Grid item xs={2}/>
					<Grid item xs={4}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q5c3"
							label="Choice 3"
							name="q5c3"
							disabled
							defaultValue={info.questions[4].choices[2].choice}
						/>
					</Grid>
					<Grid item xs={4}>
						<TextField
							margin="normal"
							required
							fullWidth
							id="q5a"
							label="Seq of correct"
							name="q5a"
						/>
						<FormHelperText>Enter 1 if choice 1 is correct</FormHelperText>
					</Grid>
					<Grid item xs={2}/>
	
					
					<Grid item xs={5}/>
					<Grid item xs={2}>
						<Button type="primary" variant="contained" fullWidth>
							submit
						</Button>
					</Grid>
					<Grid item xs={5}/>
					<Grid item xs={12}/>
				</Grid>
			</Box>
			}
		</>
  )
};

export default EventDetail;

