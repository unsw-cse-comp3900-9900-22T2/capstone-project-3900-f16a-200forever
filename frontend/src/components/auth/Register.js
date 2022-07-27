import { Box, Button, Paper } from "@mui/material";
import { useNavigate } from "react-router-dom";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import axios from "axios";
import { useState } from "react";

const Register = ({ setAlertInfo }) => {
  const navigate = useNavigate();
  const [isError, setIsError] = useState(false);

  const submit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    if (
      !data.get("email").replace(/\s/g, "").length ||
      !data.get("username").replace(/\s/g, "").length ||
      !data.get("password").replace(/\s/g, "").length ||
      !data.get("confirm_password").replace(/\s/g, "").length
    ) {
      setAlertInfo({
        status: 2,
        msg: "Please enter valid info",
      });
      return;
    }
    if (data.get("confirm_password") !== data.get("password")) {
      setIsError(true);
      setAlertInfo({
        status: 3,
        msg: "The two passwords that you entered do not match!",
      });
      return;
    }
    axios
      .post("http://127.0.0.1:8080/register", {
        name: data.get("username"),
        email: data.get("email"),
        password: data.get("password"),
      })
      .then(function (response) {
        setAlertInfo({
          status: 1,
          msg: "Register successfully!",
        });
        navigate("/login");
      })
      .catch(function (error) {
        setAlertInfo({
          status: 3,
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
          className="Register-Form"
          onSubmit={submit}
        >
          <Typography
            component="h1"
            variant="h4"
            fontWeight="bold"
            sx={{ textAlign: "center" }}
            fontFamily="inherit"
          >
            Register
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
            id="username"
            label="username"
            name="username"
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
          <TextField
            error={isError}
            margin="normal"
            required
            fullWidth
            id="confirm_password"
            label="Confirm Password"
            name="confirm_password"
            type="password"
            onChange={() => {
              setIsError(false);
            }}
          />
          <Button type="submit" fullWidth variant="contained" sx={{ mt: 3 }}>
            Submit
          </Button>
          <Button
            fullWidth
            variant="contained"
            sx={{ mt: 1, mb: 3 }}
            onClick={() => {
              navigate("/login");
            }}
          >
            To Login
          </Button>
        </Box>
      </Paper>
    </>
  );
};

export default Register;
