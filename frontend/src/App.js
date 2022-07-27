import classes from "./App.module.scss";
import { useState } from "react";
import { Fragment } from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Container } from '@mui/system';
import NavBar from "./components/NavBar/NavBar";
import Home from './components/Home/Home';
import NotFoundPage from './components/NotFoundPage/NotFoundPage';
import Login from "./components/auth/Login";

function App() {
  const [loginStatus, setLoginStatus] = useState(false);
  const [userInfo, setUserInfo] = useState({});

  const updateLoginStatus = (loginStatus) => {
    setLoginStatus(loginStatus);
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
        <NavBar loginStatus={loginStatus} updateLoginStatus={updateLoginStatus}/>
        <Container maxWidth={false} className={classes.rootContainer}>
        <Routes>  
          <Route path='' element={<Home />}/>
          <Route path='/login' element={<Login setAuth={setAuth}/>}></Route>
          <Route path='*' element={<NotFoundPage />}></Route>
        </Routes>
        </Container>
      </Router>
    </Fragment>
  );
}

export default App;
