import { Breadcrumb, Button, Layout, Menu, List } from "antd";

import { Link, useNavigate, useParams } from "react-router-dom";
import { Card, Row, Col, Pagination, Space } from "antd";
import { useState } from "react";
import axios from "axios";

import { useEffect } from "react";
import HomePage from "./HomePage";
const { Meta } = Card;
const GenresPage = () => {
  return (
    <div className="genres-page">
      <div className="genres-name">Action</div>
      <div className="genres-movies-wrapper">
        {" "}
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
    </div>
  );
};
export default GenresPage;
