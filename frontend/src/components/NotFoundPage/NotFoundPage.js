import { Button } from "@mui/material";
import React from "react";
import { useNavigate } from "react-router-dom";
import classes from "./NotFoundPage.module.scss";
import image from "../../asset/NotFound.png";

const NotFoundPage = () => {
  const navigate = useNavigate();

  return (
    <div className={classes.container}>
      <img src={image} alt="404 not found" />
      <h3>OOPS! 404 NOT FOUND!</h3>
      <h3>PAGES ARE HACKED BY ALIENS</h3>
      <Button variant="contained" onClick={() => navigate('/')}>
        Back to Earth
      </Button>
    </div>
  );
};

export default NotFoundPage;
