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
import UserProfile from "./components/UserProfile";
import UserProfileEditPage from "./components/UserProfileEditPage";
import GuessWhatYouLikePage from "./components/GuessWhatYouLikePage";
import GenresPage from "./pages/GenresPage";
import SetAdmin from "./components/SetAdmin";
function App() {
  const [loginStatus, setLoginStatus] = useState(false);
  const [userInfo, setUserInfo] = useState({});

  const updateLoginStatus = (loginStatus) => {
    setLoginStatus(loginStatus);
  };

  const updateUserInfo = (userInfo) => {
    setUserInfo(userInfo);
  };

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <>
              <Header loginStatus={loginStatus} updateLoginStatus={updateLoginStatus} userInfo={userInfo} updateUserInfo={updateUserInfo}/>
              <Outlet />
            </>
          }
        >
          <Route path="/" element={<HomePage />} />
          <Route
            path="/login"
            element={<Login updateLoginStatus={updateLoginStatus} updateUserInfo={updateUserInfo} />}
          />
          <Route
            path="/register"
            element={<Register updateLoginStatus={updateLoginStatus} updateUserInfo={updateUserInfo}/>}
          />
          <Route
            path="/forgetpassword"
            element={<ForgetPassword updateLoginStatus={updateLoginStatus} />}
          />
          <Route
            path="/search/:type/:keywords/:order"
            element={<SearchResult />}
          />
          <Route path="/movie/detail/:id" element={<MovieDetail />} />
          <Route path="/userprofile/:id" element={<UserProfile />} />
          <Route path="/userprofile/guesswhatyoulike/:id" element={<GuessWhatYouLikePage/>}/>
          <Route path="/genre/:id" element={<GenresPage/>}/>
          <Route path="/userprofile/edit/:id" element={<UserProfileEditPage />} />
        </Route>
        <Route
          path="/admin"
          element={
            <>
              <AdminHeader loginStatus={loginStatus} updateLoginStatus={updateLoginStatus}
              />
              <Outlet />
            </>
          }
        >
          <Route
            path="/admin/login"
            element={
              <AdminLogin
                loginStatus={loginStatus}
                updateLoginStatus={updateLoginStatus}
              />
            }
          ></Route>
          <Route
            path="/admin/control"
            element={
              <AdminControl
                loginStatus={loginStatus}
                updateLoginStatus={updateLoginStatus}
              />
            }
          ></Route>
          <Route
            path="/admin/event/control"
            element={
              <EventControl
                loginStatus={loginStatus}
                updateLoginStatus={updateLoginStatus}
              />
            }
          ></Route>
          <Route
            path="/admin/event/create"
            element={<CreateEvent></CreateEvent>}
          ></Route>
          <Route
            path="/admin/event/edit/:id"
            element={<EditEvent></EditEvent>}
          ></Route>
          <Route path="/admin/setadmin" element={<SetAdmin></SetAdmin>}></Route>
        </Route>
      </Routes>

      {/* <Route path="/test/:type/:keywords/:order" element ={<SearchResult/>} /> */}
    </Router>
  );
}

export default App;
