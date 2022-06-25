import React from "react";
import { Button } from "antd";
import "./App.css";
import HomePage from "./pages/HomePage";
import Login from "./pages/Login";
import Register from "./pages/Register";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

function App() {
  return (
    <Router>
      <Routes>
        <Route path = "/" element = {<HomePage/>}/>
        <Route path = "/Login" element = {<Login/>}/>
        <Route path = "/Register" element = {<Register/>}/>
      </Routes>
    </Router>
  );
  // <div className="App">
  //   <HomePage />
  //   <Button type="primary">Button</Button>
  // </div>{}
}

export default App;
