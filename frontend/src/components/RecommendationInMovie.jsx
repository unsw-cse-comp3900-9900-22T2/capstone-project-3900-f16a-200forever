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
import "../css/MovieDetail.css";
import ImgCrop from "antd-img-crop";
import { useInsertionEffect } from "react";
import axios from "axios";

import Title from "antd/lib/skeleton/Title";
const { Header, Content, Footer } = Layout;
const { Meta } = Card;

const RecommendationInMovie = () => {
  return (
    <div className="recommendation-component">
      <div className="recommendation-component-title">Related Movie</div>

      <Card
        hoverable
        style={{ width: 240 }}
        cover={
          <img
            alt="example"
            src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png"
          />
        }
      >
        <Meta title="Europe Street beat" description="www.instagram.com" />
      </Card>
    </div>
  );
};

export default RecommendationInMovie;
