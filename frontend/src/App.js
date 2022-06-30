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
import AdminHeader from "./components/AdminHeader";
import EventControl from "./components/EventControl";
import CreateEvent from "./pages/CreateEvent";
import EditEvent from "./pages/EditEvent";

function App() {
  const [loginStatus, setLoginStatus] = useState(false);
  const [userInfo, setUserInfo] = useState({})
  const [sid, setSid] = useState("")

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
            <Header loginStatus={ loginStatus } 
                    updateLoginStatus={ updateLoginStatus } 
                    userInfo={userInfo}
                    updateUserInfo={ updateUserInfo }
                    sid={sid}/>
            <Outlet />
          </>
        }>
          <Route path="/" element = {<HomePage/>}/>
          <Route path="/login" element = {<Login updateLoginStatus={updateLoginStatus} updateUserInfo={updateUserInfo} sid={sid} setSid={setSid}/>}/>
          <Route path="/register" element = {<Register updateLoginStatus={updateLoginStatus} updateUserInfo={updateUserInfo}/>}/> 
          <Route path="/forgetpassword" element = {<ForgetPassword updateLoginStatus={updateLoginStatus}/>}/>             
          <Route path="/search/:type/:keywords/:order" element={<SearchResult/>}/>   
          <Route path="/movie/detail/:id" element={<MovieDetail/>}/>   
        </Route>
      </Routes>
      <Routes>
        <Route path="/test/:type/:keywords/:order" element ={<SearchResult/>} />
        <Route
          path="/admin"
          element={
            <>
              <AdminHeader loginStatus={loginStatus} />
              <Outlet />
            </>
          }
        >
          <Route
            path="/admin/login"
            element={<AdminLogin updateLoginStatus={updateLoginStatus} />}
          ></Route>
          <Route
            path="/admin/control"
            element={<AdminControl updateLoginStatus={updateLoginStatus} />}
          ></Route>
          <Route
            path="/admin/event/control"
            element={<EventControl updateLoginStatus={updateLoginStatus} />}
          ></Route>
          <Route
            path="/admin/event/create"
            element={<CreateEvent></CreateEvent>}
          ></Route>
          <Route
            path="/admin/event/edit"
            element={<EditEvent></EditEvent>}
          ></Route>
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
