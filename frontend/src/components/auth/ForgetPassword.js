import { Box, Button, Paper } from "@mui/material";
import { useNavigate } from "react-router-dom"
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import axios from "axios";
import { useState } from "react";

const ForgetPassword = ({ setAlertInfo }) => {
	const navigate = useNavigate();
	const [email, setEmail] = useState("");
	const [isError, setIsError] = useState(false);

	const sendCode = () => {
		if (!email.replace(/\s/g, '').length) {
			setAlertInfo({
				"status": 2,
				"msg": "Please enter valid email"
			});
			return;
		}
		axios
      .post("http://127.0.0.1:8080/sendemail", {
        email: email
      })
      .then(function (response) {
        // console.log(response);
        setAlertInfo({
					"status": 1,
					"msg": "Code is on the way!"
				});
      })
      .catch(function (error) {
        // console.log(error);
				setAlertInfo({
					"status": 3,
					"msg": error.response.data.message
				});
      });
	}

	const submit = (event) => {
		event.preventDefault();
    const data = new FormData(event.currentTarget);
		if (!data.get("email").replace(/\s/g, '').length ||
			!data.get("code").replace(/\s/g, '').length ||
			!data.get("password").replace(/\s/g, '').length ||
			!data.get("confirm_password").replace(/\s/g, '').length) {
			setAlertInfo({
				"status": 2,
				"msg": "Please enter valid info"
			});
			return;
		}
		axios
      .post("http://127.0.0.1:8080/reset_password", {
        email: data.get("email"),
        new_password: data.get("password"),
        validation_code: data.get("code")
      })
      .then(function (response) {
        // console.log(response);
				setAlertInfo({
					"status": 1,
					"msg": "Reset successfully!"
				});
        navigate("/login");
      })
      .catch(function (error) {
        // console.log(error);
				setAlertInfo({
					"status": 3,
					"msg": error.response.data.message
				});
      });
	}

	return (
		<>
			<Paper>
				<Box
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
						Login
					</Typography>
					<TextField
						margin="normal"
						required
						fullWidth
						id="email"
						label="Email"
						name="email"
						onChange={(event) => { setEmail(event.target.value) }}
					/>
					<TextField
						margin="normal"
						required
						id="code"
						label="Code"
						name="code"
					/>
					<Button
						variant="contained"
						size="large"
						sx={{ ml: 3, mt: 3}}
						onClick={sendCode}
					>
						SEND CODE
					</Button>
					<TextField
						margin="normal"
						required
						fullWidth
						id="password"
						label="Password"
						name="password"
						type="password"
					/>
					<TextField
						error={isError}
						margin="normal"
						required
						fullWidth
						id="confirm_password"
						label="Confirm Password"
						name="confirm_password"
						type="password"
						onChange={() => { setIsError(false) }}
					/>
					<Button
						type="submit"
						fullWidth
						variant="contained"
						sx={{ mt: 3, mb: 3}}
					>
						SUBMIT
					</Button>
				</Box>
			</Paper>
		</>
	)
}

export default ForgetPassword;
