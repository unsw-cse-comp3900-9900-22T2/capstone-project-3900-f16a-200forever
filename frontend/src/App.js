import classes from "./App.module.scss";
import { useState } from "react";
import { Fragment } from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Container } from '@mui/system';
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';
import NavBar from "./components/NavBar/NavBar";
import Home from './components/Home/Home';
import NotFoundPage from './components/NotFoundPage/NotFoundPage';
import Login from "./components/auth/Login";
import Register from "./components/auth/Register";
import ForgetPassword from "./components/auth/ForgetPassword";

function App() {
  const [userInfo, setUserInfo] = useState({});
  const [alertInfo, setAlertInfo] = useState({
    "status": 0,
    "msg": ""
  })

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setAlertInfo({
      "status": 0,
      "msg": ""
    });
  };

  const updateUserInfo = (userInfo) => {
    setUserInfo(userInfo);
  };

  localStorage.setItem('status', false);
  function setAuth(token, id, username, email, status) {
    localStorage.setItem('token', token);
    localStorage.setItem('id', id);
    localStorage.setItem('username', username);
    localStorage.setItem('email', email);
    localStorage.setItem('status', status);
  }

  return (
    <Fragment>
      <Router>
        <NavBar setAuth={setAuth}/>
        <Container maxWidth={false} className={classes.rootContainer}>
        <Routes>  
          <Route path='' element={<Home />}/>
          <Route path='/login' element={<Login setAuth={setAuth} setAlertInfo={setAlertInfo}/>}/>
          <Route path='/register' element={<Register setAlertInfo={setAlertInfo}/>}/>
          <Route path='/forgetpassword' element={<ForgetPassword setAlertInfo={setAlertInfo}/>}/>
          <Route path='*' element={<NotFoundPage />}></Route>
        </Routes>
        </Container>
      </Router>
      <Snackbar open={alertInfo['status'] === 1 ? true : false} autoHideDuration={2000} onClose={handleClose}>
        <Alert onClose={handleClose} severity="success" sx={{ width: '100%' }}>
          {alertInfo['msg']}
        </Alert>
      </Snackbar>
      
      <Snackbar open={alertInfo['status'] === 2 ? true : false} autoHideDuration={2000} onClose={handleClose}>
        <Alert onClose={handleClose} severity="info" sx={{ width: '100%' }}>
          {alertInfo['msg']}
        </Alert>
      </Snackbar>

			<Snackbar open={alertInfo['status'] === 3 ? true : false} autoHideDuration={2000} onClose={handleClose}>
        <Alert onClose={handleClose} severity="error" sx={{ width: '100%' }}>
          {alertInfo['msg']}
        </Alert>
      </Snackbar>
    </Fragment>
  );
}

export default App;
