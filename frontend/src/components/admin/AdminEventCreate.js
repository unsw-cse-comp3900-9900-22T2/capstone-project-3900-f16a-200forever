import { Box, Button, Paper } from "@mui/material";
import { useNavigate } from "react-router-dom";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import axios from "axios";
import { useState } from "react";

import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormHelperText from '@mui/material/FormHelperText';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

import Grid from '@mui/material/Grid';

function fileToDataUrl(file) {
  const validFileTypes = [ 'image/jpeg', 'image/png', 'image/jpg' ]
  const valid = validFileTypes.find(type => type === file.type);
  // Bad data, let's walk away.
  if (!valid) {
      throw Error('provided file is not a png, jpg or jpeg image.');
  }
  
  const reader = new FileReader();
  const dataUrlPromise = new Promise((resolve,reject) => {
      reader.onerror = reject;
      reader.onload = () => resolve(reader.result);
  });
  reader.readAsDataURL(file);
  return dataUrlPromise;
}

const AdminEventCreate = ({ setAlertInfo }) => {
	const navigate = useNavigate();
	const [base64, setBase64] = useState("");
	const submit = (event) => {
		event.preventDefault();
    const data = new FormData(event.currentTarget);
		const body = {
			email: localStorage.getItem("email"),
			token: localStorage.getItem("token"),
			topic: data.get("topic"),
			duration: parseInt(data.get("duration")),
			deadline: data.get("deadline"),
			image: base64,
			image_description: "",
			description: data.get("description"),
			require_correctness_amt: 4,
			status: "open",
			movies: [parseInt(data.get("movie"))],
			questions: [
				{
					content: data.get("q1"),
					choice_1: data.get("q1c1"),
					choice_2: data.get("q1c2"),
					choice_3: data.get("q1c3"),
					correct_answer: parseInt(data.get("q1a")),
				},
				{
					content: data.get("q2"),
					choice_1: data.get("q2c1"),
					choice_2: data.get("q2c2"),
					choice_3: data.get("q2c3"),
					correct_answer: parseInt(data.get("q2a")),
				},
				{
					content: data.get("q3"),
					choice_1: data.get("q3c1"),
					choice_2: data.get("q3c2"),
					choice_3: data.get("q3c3"),
					correct_answer: parseInt(data.get("q3a")),
				},
				{
					content: data.get("q4"),
					choice_1: data.get("q4c1"),
					choice_2: data.get("q4c2"),
					choice_3: data.get("q4c3"),
					correct_answer: parseInt(data.get("q4a")),
				},
				{
					content: data.get("q5"),
					choice_1: data.get("q5c1"),
					choice_2: data.get("q5c2"),
					choice_3: data.get("q5c3"),
					correct_answer: parseInt(data.get("q5a")),
				}
			]
		}
		axios
			.post("http://127.0.0.1:8080/event/create", body)
			.then(function (response) {
				console.log(response);
				setAlertInfo({
					status: 1,
					msg: "Create successfully"
				});
				navigate("/admin/events")
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
						Create an event
					</Typography>
				</Grid>
				<Grid item xs={2}/>
        <Grid item xs={6}>
					<TextField
						margin="normal"
						required
						fullWidth
						id="topic"
						label="Topic"
						name="topic"
					/>
        </Grid>
				<Grid item xs={2}>
					<Button variant="contained" component="label" fullWidth size="large" sx={{ mt: 3 }}>
						Upload
						<input hidden accept=".png,.jpeg,.jpg" type="file" onChange={
							(event) => {
								fileToDataUrl(event.target.files[0]).
									then((data) => {
										setBase64(data);
										setAlertInfo({
											status: 1,
											msg: "Upload successfully"	
										})
									})
									.catch(() => {
										setAlertInfo({
											status: 3,
											msg: "Upload fails"	
										})
									});
								return false;
							}}/>
					</Button>
				</Grid>
				<Grid item xs={2}/>

				<Grid item xs={2}/>
				<Grid item xs={2}>
					<TextField
						margin="normal"
						required
						fullWidth
						id="duration"
						label="Duration in mins"
						name="duration"
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
					/>
				</Grid>
				<Grid item xs={2}/>

				<Grid item xs={2}/>
				<Grid item xs={8}>
					<TextField
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
						create
					</Button>
				</Grid>
				<Grid item xs={5}/>
				<Grid item xs={12}/>
      </Grid>
    </Box>
	)
};

export default AdminEventCreate;



{/* <Box
			component="form"
			noValidate
			autoComplete="off"
			className="Login-Form"
			onSubmit={submit}
		>
			<Typography
				component="h1"
				variant="h4"
				fontWeight="bold"
				sx={{ textAlign: "center" }}
				fontFamily="inherit"
			>
				Create an event
			</Typography>
			<TextField
				margin="normal"
				required
				fullWidth
				id="topic"
				label="Topic"
				name="topic"
			/>
			<TextField
				margin="normal"
				required
				fullWidth
				id="duration"
				label="Duration in mins"
				name="duration"
			/>
			<TextField
				margin="normal"
				required
				fullWidth
				id="deadline"
				label="Deadline yyyy-mm-dd"
				name="deadline"
			/>
			<TextField
				margin="normal"
				required
				fullWidth
				id="description"
				label="Description"
				name="description"
				multiline
				rows={2}
			/>

			<Typography variant="h4" component="div" sx={{ mt: 4, mb: 4 }}>
				Questions
			</Typography>
			<TextField
				margin="normal"
				required
				fullWidth
				id="q1"
				label="Question1"
				name="q1"
				multiline
				rows={2}
			/>
			<TextField
				margin="normal"
				required
				id="q1c1"
				label="Choice 1"
				name="q1c1"
			/>

			<Button variant="contained" sx={{ ml: 10 }}>
				Login
			</Button>
		</Box> */}