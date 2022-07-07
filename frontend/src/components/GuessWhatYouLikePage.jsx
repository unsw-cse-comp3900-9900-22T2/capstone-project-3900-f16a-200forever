import { Link, useParams } from "react-router-dom";
import {
  Button,
  Radio,
  Row,
  Col,
  Space,
  Typography,
  Upload,
  Image,
  Form,
  Input,
  Layout,
} from "antd";
import { useNavigate } from "react-router-dom";
import React, { useState } from "react";
import "../css/UserProfile.css";
import ImgCrop from "antd-img-crop";
import { useInsertionEffect } from "react";
import axios from "axios";
import "../css/UserProfile.css";
const { Header, Content, Footer } = Layout;
const GuessWhatYouLikePage = () => {
  return (
    <div className="guess-what-you-like-page">
      <Content
        style={{
          paddingTop: 70,
          background: "white",
        }}
      ></Content>
    </div>
  );
};

export default GuessWhatYouLikePage;
