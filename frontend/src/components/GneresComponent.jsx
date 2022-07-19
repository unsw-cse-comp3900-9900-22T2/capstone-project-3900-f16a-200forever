import { Breadcrumb, Button, Layout, Menu, List } from "antd";
import SearchComponent from "./SearchComponent";
import { Link, useNavigate, useParams } from "react-router-dom";
import { Card, Space } from "antd";
import { useState } from "react";
import axios from "axios";
import openNotification from "./Notification";
import { useEffect } from "react";

const {Meta} = Card;

const GenresInHomepage = () => {
  let navigate = useNavigate()
  const [genres, setGenres] = useState([])

  useEffect( () => {
    axios
    // todo change url here
    .get("http://127.0.0.1:8080/genre/all", {
    })
    .then(function (response) {
      console.log(response.data);
      setGenres(response.data.genres);
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
    <div className="genres-component-in-HomePage">
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
        
        dataSource={genres}
        renderItem={(item) => (
          <List.Item>
            <Link to={`/genre/id=${item.id}`}>
              <Card
                hoverable
                bordered={true}
                // loading={true}
              >
                <Meta title={item.name} />
              </Card>
            </Link>
          </List.Item>
        )}
      />
      <Space>
        {" "}
        <Button   onClick={() => navigate("/forum")}>Go to forum to disscuss more</Button>
        <Button onClick={()=> navigate('/getbadge')}>Go to get a badge</Button>
      </Space>
    </div>
  );
};
export default GenresInHomepage;
