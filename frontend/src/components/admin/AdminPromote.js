import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import { useNavigate } from "react-router-dom";
import TextField from "@mui/material/TextField";
import { Button } from '@mui/material';
import FormHelperText from '@mui/material/FormHelperText';
import { useState } from 'react';
import axios from 'axios';

const AdminPromote = ({ setAlertInfo }) => {
	const [email1, setEmail1] = useState("");
	const [email2, setEmail2] = useState("");

	const setReviewAdmin = () => {
		if (localStorage.getItem("token") === null) {
			setAlertInfo({
				status: 2,
				msg: "please login"
			})
		}
		setAlertInfo({
			status: 2,
			msg: "sending"
		});
		axios
			.put(`http://127.0.0.1:8080/review/admin`, {
				user_email: email1,
				admin_email: localStorage.getItem("email"),
				token: localStorage.getItem("token"),
				become_admin: true
			})
			.then(function (response) {
				setAlertInfo({
					status: 1,
					msg: "Successfully"
				});
			})
			.catch(function (error) {
				setAlertInfo({
					status: 3,
					msg: error.response.data.message
				});
			});
	}

	const setForumAdmin = () => {
		if (localStorage.getItem("token") === null) {
			setAlertInfo({
				status: 2,
				msg: "please login"
			})
		}
		setAlertInfo({
			status: 2,
			msg: "sending"
		});
		axios
			.put(`http://127.0.0.1:8080/thread/admin`, {
				user_email: email2,
				admin_email: localStorage.getItem("email"),
				token: localStorage.getItem("token"),
				become_admin: true
			})
			.then(function (response) {
				setAlertInfo({
					status: 1,
					msg: "Successfully"
				});
			})
			.catch(function (error) {
				setAlertInfo({
					status: 3,
					msg: error.response.data.message
				});
			});
		}

	return (
		<Grid container>
			<Grid item xs={2}/>
			<Grid item xs={4}>
				<TextField
					margin="normal"
					required
					fullWidth
					id="email"
					label="Email of review admin"
					name="email"
					onChange={(event) => { setEmail1(event.target.value) }}
				/>
			</Grid>
			<Grid item xs={1}>
				<Button sx={{ mt: 3 }} onClick={setReviewAdmin}>
					confirm
				</Button>
			</Grid>
			<Grid item xs={5}/>
			<Grid item xs={2}/>

			<Grid item xs={4}>
				<TextField
					margin="normal"
					required
					fullWidth
					id="email"
					label="Email of forum admin"
					name="email"
					onChange={(event) => { setEmail2(event.target.value) }}
				/>
			</Grid>
			<Grid item xs={1}>
				<Button sx={{ mt: 3 }} onClick={setForumAdmin}>
					confirm
				</Button>
			</Grid>
			<Grid item xs={5}/>
		</Grid>
		
	)
};

export default AdminPromote;