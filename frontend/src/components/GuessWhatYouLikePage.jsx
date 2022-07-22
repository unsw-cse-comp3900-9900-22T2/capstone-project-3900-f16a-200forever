import { Link, useParams } from "react-router-dom";
import {
  Button,
  Radio,
  Select,
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
import { useEffect } from "react";

const { Header, Content, Footer } = Layout;
const { Meta } = Card;
const { Option } = Select;

const GuessWhatYouLikePage = () => {
  const handleChange = (value) => {
    console.log(`selected ${value}`);
    getList(value);
  };
  const [movies, setMovies] = useState([]);
  const { id } = useParams();

  useEffect(()=>{
    getList("genre");
  }, [])

  const getList = (type) => {
    axios.get("http://127.0.0.1:8080/recommendation/user",{
      params:{
        "user_id":id.replace("id=",""),
        "by": type
      }
    })
    .then(function(response){
      console.log(response.data)
      setMovies(response.data.movies)
    })
    .catch(function(error){
      console.log(error.response)
    })
  }

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
          <Select
            defaultValue="genre"
            style={{
              width: 120,
            }}
            onChange={handleChange}
          >
            <Option value="genre">By genre</Option>
            <Option value="director">By director</Option>
          </Select>
          <List
            grid={{
              gutter: 16,
              xs: 1,
              sm: 2,
              md: 4,
              lg: 4,
              xl: 6,
              xxl: 10,
            }}
            dataSource={movies}
            renderItem={(item) => (
              <List.Item>
                {
                  <Link to={`/movie/detail/id=${item.id}`}>
                    <Card
                      hoverable
                      bordered={false}
                      style={{}}
                      cover={<img alt="example" src={item.backdrop} />}
                    >
                      <Meta title={item.title} description={`rating: 0`} />
                    </Card>
                  </Link>
                }
              </List.Item>
            )}
          />
        </div>
      </Content>
    </div>
  );
};

export default GuessWhatYouLikePage;