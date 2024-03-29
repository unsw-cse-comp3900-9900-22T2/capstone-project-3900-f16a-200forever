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
import SearchPage from "./components/search/SearchPage";
import MovieDetails from "./components/movie/MovieDetails";
import GenrePage from "./components/genre/GenrePage";
import GenreMovie from "./components/genre/GenreMovie";
import ForumHome from "./components/forum/ForumHome";
import ForumPage from "./components/forum/ForumPage";
import PostPage from "./components/forum/PostPage";
import Userprofile from "./components/userprofile/Userprofile";
import UserRecomm from "./components/userprofile/UserRecomm";
import AdminLogin from "./components/admin/AdminLogin";
import AdminHome from "./components/admin/AdminHome";
import AdminEventHome from "./components/admin/AdminEventHome";
import AdminEventDetail from "./components/admin/AdminEventDetail";
import EventHome from "./components/event/EventHome";
import EventDetail from "./components/event/EventDetail";
import AdminEventCreate from "./components/admin/AdminEventCreate";
import FollowList from "./components/userprofile/FollowList";
import BanList from "./components/userprofile/BanList";
import AdminPromote from "./components/admin/AdminPromote";
import AdminDemote from "./components/admin/AdminDemote";

function App() {
  // const [userInfo, setUserInfo] = useState({});
  // const [loginStatus, setLoginStatus] = useState(localStorage.getItem("status"));
  // const [loginStatus, setLoginStatus] = useState(false);
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

  function setAuth(token, id, username, email, status) {
    localStorage.setItem('token', token);
    localStorage.setItem('id', id);
    localStorage.setItem('username', username);
    localStorage.setItem('email', email);
    localStorage.setItem('status', status);
    if (status === false) {
      localStorage.removeItem("token");
      localStorage.removeItem("id");
      localStorage.removeItem("username");
      localStorage.removeItem("email");
    }
  }

  return (
    <Fragment>
      <Router>
        <NavBar setAuth={setAuth} setAlertInfo={setAlertInfo}/>
        <Container maxWidth={false} className={classes.rootContainer}>
        <Routes>  
          <Route path='' element={<Home />}/>
          <Route path='/login' element={<Login setAuth={setAuth} setAlertInfo={setAlertInfo}/>}/>
          <Route path='/register' element={<Register setAlertInfo={setAlertInfo}/>}/>
          <Route path='/forgetpassword' element={<ForgetPassword setAlertInfo={setAlertInfo}/>}/>
          <Route path='/search' element={<SearchPage setAlertInfo={setAlertInfo}/>}/>
          <Route path='/movie/details/:id' element={<MovieDetails setAlertInfo={setAlertInfo}/>}/>
          <Route path='/genres' element={<GenrePage setAlertInfo={setAlertInfo}/>}/>
          <Route path='/genre/:genre/:id' element={<GenreMovie setAlertInfo={setAlertInfo}/>}/>
          <Route path='/events' element={<EventHome setAlertInfo={setAlertInfo}/>}/>
          <Route path='/event/:id' element={<EventDetail setAlertInfo={setAlertInfo}/>}/>
          <Route path='/forums' element={<ForumHome setAlertInfo={setAlertInfo}/>}/>
          <Route path='/forum/:genre/:id' element={<ForumPage setAlertInfo={setAlertInfo}/>}/>
          <Route path='/post/:id' element={<PostPage setAlertInfo={setAlertInfo}/>}/>
          <Route path='/userprofile/:id' element={<Userprofile setAlertInfo={setAlertInfo}/>}/>
          <Route path='/user/recommend/:id' element={<UserRecomm setAlertInfo={setAlertInfo}/>}/>
          <Route path='/user/follow/:id' element={<FollowList setAlertInfo={setAlertInfo}/>}/>
          <Route path='/user/ban/:id' element={<BanList setAlertInfo={setAlertInfo}/>}/>
          <Route path='/admin/login' element={<AdminLogin setAuth={setAuth} setAlertInfo={setAlertInfo}/>}/>
          <Route path='/admin/home' element={<AdminHome setAlertInfo={setAlertInfo}/>}/>
          <Route path='/admin/events' element={<AdminEventHome setAlertInfo={setAlertInfo}/>}/>
          <Route path='/admin/promote' element={<AdminPromote setAlertInfo={setAlertInfo}/>}/>
          <Route path='/admin/demote' element={<AdminDemote setAlertInfo={setAlertInfo}/>}/>
          <Route path='/admin/event/:id' element={<AdminEventDetail setAlertInfo={setAlertInfo}/>}/>
          <Route path='/admin/event/create' element={<AdminEventCreate setAlertInfo={setAlertInfo}/>}/>
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
