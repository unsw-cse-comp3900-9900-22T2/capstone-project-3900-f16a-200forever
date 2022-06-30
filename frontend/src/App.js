import React, { useState } from "react";
import "./App.css";
import HomePage from "./pages/HomePage";
import Login from "./components/Login";
import Register from "./components/Register";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Outlet,
} from "react-router-dom";
import Header from "./components/Header";
import ForgetPassword from "./components/ForgetPassword";
import SearchResult from "./components/SearchResult";
import MovieDetail from "./pages/MovieDetail";
import AdminLogin from "./components/AdminLogin";
import AdminControl from "./components/AdminControl";
import searchResult from "./components/SearchResult";
function App() {
  const [loginStatus, setLoginStatus] = useState(false);
  const [userInfo, setUserInfo] = useState({})

  const updateLoginStatus = (loginStatus) => {
    setLoginStatus(loginStatus);
  };

  const updateUserInfo = (userInfo) => {
    setUserInfo(userInfo);
  }

  return (
    <Router>
      <Routes>
        <Route path='/' element={
          <>
            <Header loginStatus={ loginStatus } userInfo={userInfo}/>
            <Outlet />
          </>
        }>
          <Route path="/" element = {<HomePage/>}/>
          <Route path="/login" element = {<Login updateLoginStatus={updateLoginStatus} updateUserInfo={updateUserInfo}/>}/>
          <Route path="/register" element = {<Register updateLoginStatus={updateLoginStatus} updateUserInfo={updateUserInfo}/>}/> 
          <Route path="/forgetpassword" element = {<ForgetPassword updateLoginStatus={updateLoginStatus}/>}/>             
          <Route path="/search/:type/:keywords/:order" element={<SearchResult/>}/>   
          <Route path="/movie/detail/:id" element={<MovieDetail/>}/>   
        </Route>
      </Routes>
      <Routes>
        <Route path="/test/:type/:keywords/:order" element ={<SearchResult/>} />
        <Route
          path="/admin/login"
          element={<AdminLogin updateLoginStatus={updateLoginStatus} />}
        ></Route>
        <Route
          path="/admin/control"
          element={<AdminControl updateLoginStatus={updateLoginStatus} />}
        ></Route>
      </Routes>
    </Router>
  );
}

export default App;
