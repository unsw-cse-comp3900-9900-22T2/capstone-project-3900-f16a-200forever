import { useEffect, useState } from "react";
import { Button, Box } from "@mui/material";
import axios from "axios";
import Card from "@mui/material/Card";
import Grid from "@mui/material/Grid";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import { useNavigate } from "react-router-dom";
import * as React from "react";
import Avatar from "@mui/material/Avatar";
import CardMedia from "@mui/material/CardMedia";

const UserProfile = () => {
  return (
    <div>
      <Box>
        {" "}
        <UserCard></UserCard>
      </Box>
    </div>
  );
};
export default UserProfile;

const UserCard = () => {
  return (
    <Card sx={{ maxWidth: 500, maxHeight: 400 }}>
      <CardMedia
        component="img"
        alt="green iguana"
        height="300"
        width="300"
        // sx={{ paddingTop: "81.25%", borderRadius: "50%", margin: "28px" }}
        image="https://image.tmdb.org/t/p/w600_and_h900_bestv2/kpuTCMw3v2AuKjqGS7383uWbc8V.jpg"
      />
    </Card>
  );
};
