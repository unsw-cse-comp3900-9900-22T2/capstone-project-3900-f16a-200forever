import { Box, Button, Paper } from "@mui/material";
import { useNavigate } from "react-router-dom"
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import { useState } from "react";
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';
import axios from "axios";

const Login = ({ setAuth }) => {
	const navigate = useNavigate();

	const [status, setStatus] = useState(0);
	const [errorMsg, setErrorMsg] = useState("");

	const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setStatus(0);
  };

	const submit = (event) => {
		event.preventDefault();
    const data = new FormData(event.currentTarget);
		if (!data.get("email").replace(/\s/g, '').length) {
			setStatus(1);
			return;
		}

		if (!data.get("password").replace(/\s/g, '').length) {
			setStatus(1);
			return;
		}
		axios
			.post("http://127.0.0.1:8080/login", {
				email: data.get("email"),
				password: data.get("password"),
				is_admin: false
			})
			.then(function (response) {
				console.log(response);
				setAuth(response.data.token, response.data.id, response.data.name, data.get("email"), true)
				navigate("/")
			})
			.catch(function (error) {
				console.log(error.response.data);
				setErrorMsg(error.response.data.message);
				setStatus(3);
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
					/>
					<TextField
						margin="normal"
						required
						fullWidth
						id="password"
						label="Password"
						name="password"
					/>
					<Button
						type="submit"
						fullWidth
						variant="contained"
						sx={{ mt: 3, mb: 2 }}
					>
						Login
					</Button>
					<Button
						fullWidth
						variant="contained"
						sx={{ mt: 1, mb: 3 }}
						onClick={() => { navigate("/register")}}
					>
						Register
					</Button>
				</Box>
			</Paper>
			<Snackbar open={status === 1 ? true : false} autoHideDuration={2000} onClose={handleClose}>
        <Alert onClose={handleClose} severity="success" sx={{ width: '100%' }}>
          Login Successfully!
        </Alert>
      </Snackbar>
      
      <Snackbar open={status === 2 ? true : false} autoHideDuration={2000} onClose={handleClose}>
        <Alert onClose={handleClose} severity="info" sx={{ width: '100%' }}>
          Please enter valid info!
        </Alert>
      </Snackbar>

			<Snackbar open={status === 3 ? true : false} autoHideDuration={2000} onClose={handleClose}>
        <Alert onClose={handleClose} severity="error" sx={{ width: '100%' }}>
          {errorMsg}
        </Alert>
      </Snackbar>
		</>
	)
}

export default Login;
