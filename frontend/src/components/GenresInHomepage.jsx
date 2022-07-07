import { Breadcrumb, Button, Layout, Menu, List } from "antd";
import SearchComponent from "./SearchComponent";
import { Link, useNavigate, useParams } from "react-router-dom";
import { Card, Row, Col, Pagination, Space } from "antd";
import { useState } from "react";
import axios from "axios";
import openNotification from "./Notification";
import { useEffect } from "react";
import HomePage from "../pages/HomePage";
const { Meta } = Card;
const GenresInHomepage = () => {
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
      <Space>
        {" "}
        <Button>Go to forum to disscuss more</Button>
        <Button>Go to get a badge</Button>
      </Space>
    </div>
  );
};
export default GenresInHomepage;
