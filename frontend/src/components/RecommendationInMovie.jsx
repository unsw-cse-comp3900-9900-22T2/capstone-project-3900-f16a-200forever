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
import React, { useState ,useEffect} from "react";
import "../css/MovieDetail.css";
import ImgCrop from "antd-img-crop";
import { useInsertionEffect } from "react";
import axios from "axios";
import openNotification from "../components/Notification";
import Title from "antd/lib/skeleton/Title";
const { Header, Content, Footer } = Layout;
const { Meta } = Card;

const RecommendationInMovie = () => {
  const { id } = useParams();
  const [recommendInfo, setrecommend] = useState([]);
  const getList = (pageNum)=>{
    axios.get("http://127.0.0.1:8080/recommendation/genre",{
      params:{
        "movie_id": id.replace("id=", ""),
      }
    }).then(function (response) {
      console.log(response.data.movies);
      var list = response.data.movies.splice(0,5)
      console.log(list)
      setrecommend(list);
    })
    // todo handle error
    .catch(function (error) {
      console.log(error.response);
      openNotification({
        "title": "Viewing page error",
      })
    });
  }

  useEffect(() => {
    getList()
  }, []);
  return (
    <div className="recommendation-component">
      <div className="recommendation-component-title">Related Movie</div>

       <div className="search-card-wrapper">
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
        dataSource={recommendInfo} 
        renderItem={(item) => (
          <List.Item>
            {
              <Link to={`/movie/detail/id=${item.movie_id}`}>
                <Card
                  hoverable
                  bordered={false}
                  style={{}}
                  cover={
                    <img
                      alt="example"
                      src={item.backdrop}
                    />
                  }
                >
                  <Meta title={item.movie_title} description={`rating: 0`} />
                </Card>
              </Link>
            }
          </List.Item>
        )}
      /> 
      {/* <Pagination defaultCurrent={1} total={numItem} defaultPageSize={12} hideOnSinglePage onChange={changePage}/> */}
       </div> 
    </div>
  );
};

export default RecommendationInMovie;
