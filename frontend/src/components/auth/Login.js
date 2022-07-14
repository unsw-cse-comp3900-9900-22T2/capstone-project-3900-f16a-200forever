import { Box, Button, Paper } from "@mui/material";
import { useNavigate } from "react-router-dom"

const Login = ({ updateLoginStatus }) => {
	// const navigate = useNavigate();
	return (
		<Paper>
		<Box
			component="form"
			noValidate
			autoComplete="off"
			className="Login-Form"
		>
		</Box>
		</Paper>
	)
}

export default Login;
