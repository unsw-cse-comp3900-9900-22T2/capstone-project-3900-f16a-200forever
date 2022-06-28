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
function App() {
  const [loginStatus, setLoginStatus] = useState(false);

  const updateLoginStatus = (loginStatus) => {
    setLoginStatus(loginStatus);
  };

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <>
              <Header loginStatus={loginStatus} />
              <Outlet />
            </>
          }
        >
          <Route path="/" element={<HomePage />} />
          <Route
            path="/login"
            element={<Login updateLoginStatus={updateLoginStatus} />}
          />
          <Route
            path="/register"
            element={<Register updateLoginStatus={updateLoginStatus} />}
          />
          <Route
            path="/forgetpassword"
            element={<ForgetPassword updateLoginStatus={updateLoginStatus} />}
          />
          <Route
            path="/searchresult"
            element={<SearchResult updateLoginStatus={updateLoginStatus} />}
          />
          <Route
            path="/moviedetail"
            element={<MovieDetail updateLoginStatus={updateLoginStatus} />}
          />
        </Route>
      </Routes>
      <Routes>
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
