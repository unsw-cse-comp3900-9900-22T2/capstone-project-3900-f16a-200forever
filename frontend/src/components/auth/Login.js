import { Box, Button, Paper } from "@mui/material";
import { useNavigate } from "react-router-dom";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import axios from "axios";

const Login = ({ setAuth, setAlertInfo }) => {
  const navigate = useNavigate();

  const submit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    if (
      !data.get("email").replace(/\s/g, "").length ||
      !data.get("password").replace(/\s/g, "").length
    ) {
      setAlertInfo({
        status: 2,
        msg: "Please enter valid info",
      });
      return;
    }

    axios
      .post("http://127.0.0.1:8080/login", {
        email: data.get("email"),
        password: data.get("password"),
        is_admin: false,
      })
      .then(function (response) {
        console.log(response);
        setAuth(
          response.data.token,
          response.data.id,
          response.data.name,
          data.get("email"),
          true
        );
        setAlertInfo({
          status: 1,
          msg: "Login successfully!",
        });
        navigate("/");
      })
      .catch(function (error) {
        console.log(error.response.data);
        setAlertInfo({
          status: 2,
          msg: error.response.data.message,
        });
      });
  };

  return (
    <>
      <Paper
        elevation={6}
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          padding: "36px",
          width: "600px",
          height: "500px",
          gap: "40px",
          mx: "auto",
          mt: "50px",
        }}
      >
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
            type="password"
          />
          <Button type="submit" fullWidth variant="contained" sx={{ mt: 3 }}>
            Login
          </Button>
          <Button
            fullWidth
            variant="contained"
            sx={{ mt: 1 }}
            onClick={() => {
              navigate("/register");
            }}
          >
            Register
          </Button>
          <Button
            fullWidth
            variant="text"
            sx={{ mt: 1, mb: 2 }}
            onClick={() => {
              navigate("/forgetpassword");
            }}
          >
            FORGET PASSWORD
          </Button>
        </Box>
      </Paper>
    </>
  );
};

export default Login;
