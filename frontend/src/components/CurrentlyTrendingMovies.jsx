import { Breadcrumb, Button, Layout, Menu, List } from "antd";
import SearchComponent from "./SearchComponent";
import { Link, useNavigate, useParams } from "react-router-dom";
import { Card, Row, Col, Pagination } from "antd";
import { useState } from "react";
import axios from "axios";
import "../css/HomePage.css"
import openNotification from "./Notification";
import { useEffect } from "react";
import HomePage from "../pages/HomePage";
const { Meta } = Card;
const CurrentlyTrendingMovies = () => {
  let navigate = useNavigate()
  return (
    <div className="genres-component-in-HomePage">
      <List>
        <List.Item offset={2}>
          <Card
            hoverable
            style={{ width: 100 }}
            cover={
              <img
                alt="example"
                src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png"
              />
            }
          >
            <Meta title="Europe Street beat" />
          </Card>
        </List.Item>
      </List>
      <Button onClick={() => navigate("/guesswhatyoulike")}>Guess what you like</Button>
    </div>
  );
};
export default CurrentlyTrendingMovies;
