import { Breadcrumb, Button, Layout, Menu, List } from "antd";
import { Link, useNavigate, useParams } from "react-router-dom";
import { Card, Row, Col, Pagination, Space } from "antd";
import { useState } from "react";
import axios from "axios";
import { useEffect } from "react";
import HomePage from "./HomePage";
import openNotification from "../components/Notification";

const { Meta } = Card;

const GenresPage = () => {
  const [movies, setMovies] = useState([]);
  const [numItem, setNumItem] = useState(0);
  const { id } = useParams();
  const id_val = id.replace("id=", "");

  const changePage = (page, pageSize) => {
    console.log(page);
    console.log(pageSize);
    // getList(page);
  }

  useEffect( () => {
    axios
    // todo change url here
    .get("http://127.0.0.1:8080/genre/genremovies", {
      params: {
        "genre_id": id_val
      }
    })
    .then(function (response) {
      console.log(response.data.movies);
      console.log(id_val);
    })
    // todo handle error
    .catch(function (error) {
      console.log(error.response);
      openNotification({
        "title": "Error",
      })
    });
  }, [])

  return (
    <div className="genres-page">
      <div className="genres-name">Action</div>
      <div className="genres-movies-wrapper">
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
            <Link to={`/movie/detail/id=${item.id}`}>
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
                <Meta title={item.title} description={`rating: 0`} />
              </Card>
            </Link>
          </List.Item>
        )}
      />
      <Pagination defaultCurrent={1} total={numItem} defaultPageSize={12} hideOnSinglePage onChange={changePage}/>
      </div>
    </div>
  );
};
export default GenresPage;
