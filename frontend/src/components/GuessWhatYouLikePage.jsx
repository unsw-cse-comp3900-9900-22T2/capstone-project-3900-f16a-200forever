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
  List,
  Card,
  Pagination,
} from "antd";
import { useNavigate } from "react-router-dom";
import React, { useState } from "react";
import "../css/UserProfile.css";
import ImgCrop from "antd-img-crop";
import { useInsertionEffect } from "react";
import axios from "axios";
import "../css/UserProfile.css";
import Title from "antd/lib/skeleton/Title";
const { Header, Content, Footer } = Layout;
const { Meta } = Card;
const GuessWhatYouLikePage = () => {
  return (
    <div className="guess-what-you-like-page">
      <Content
        style={{
          paddingTop: 100,
          background: "white",
        }}
      >
        <div className="guess-what-you-like-title">Guess what you like</div>
        <div className="guess-you-like-card-wrap">
          {" "}
         
        </div>
      </Content>
    </div>
  );
};

export default GuessWhatYouLikePage;
