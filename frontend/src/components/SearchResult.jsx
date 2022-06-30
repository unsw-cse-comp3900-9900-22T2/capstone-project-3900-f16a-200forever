import { Breadcrumb, Button, Layout, Menu, List } from "antd";
import SearchComponent from "./SearchComponent";
import { Link, useNavigate, useParams } from "react-router-dom";
import { Card, Row, Col, Pagination } from "antd";
import { useState } from "react";
import axios from "axios";
import openNotification from "./Notification";
import { useEffect } from "react";

const { Header, Content, Footer } = Layout;
const { Meta } = Card;

const SearchResult = () => {
  const { type, keywords, order } = useParams();
  const type_val = type.replace("type=", "")
  const keywords_val = keywords.replace("keywords=", "")
  const order_val = order.replace("order=", "")
  // console.log(type);
  // console.log(keywords);
  // console.log(order);
  const [fullList, setFullList] = useState([]);
  const [showList, setShowList] = useState([]);
  const [numItem, setNumItem] = useState(0);

  const changePage = (page, pageSize) => {
    // console.log(page);
    // console.log(pageSize);
    setShowList(fullList.slice(page*pageSize - 12, page*pageSize))
  }

  useEffect( () => {
    axios
    // todo change url here
    .get("http://127.0.0.1:5000/test", {
      params: {
        "type": type_val,
        "keywords": keywords_val,
        "order": order_val
      }
    })
    .then(function (response) {
      console.log(response.data.result);
      setFullList(response.data.result);
      setNumItem(response.data.result.length);
      setShowList(response.data.result.slice(0, 12));
    })
    // todo handle error
    .catch(function (error) {
      console.log(error.response);
      // openNotification({
      //   "title": "Search error",
      //   "content": error
      // })
    });
  }, [])

  return (
    <>
    <Content
      style={{
        paddingTop: 70,
        background: "white",
      }}
    >
      <SearchComponent type={type_val} keywords={keywords_val} order={order_val}></SearchComponent>

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
        dataSource={showList}
        renderItem={(item) => (
          <List.Item>
            {
              type_val === "director" ?
              <Link to={`/director/id=${item.id}`}>
                <Card
                  hoverable
                  bordered={false}
                  style={{}}
                  cover={
                    <img
                      alt="example"
                      src={item.url}
                    />
                  }
                >
                  <Meta title={item.title}/>
                </Card>   
              </Link>
                :
              <Link to={`/movie/detail/id=${item.id}`}>
                <Card
                  hoverable
                  bordered={false}
                  style={{}}
                  cover={
                    <img
                      alt="example"
                      src={item.url}
                    />
                  }
                >
                  <Meta title={item.title} description={`rating: ${item.rating}`} />
                </Card>
              </Link>
            }
          </List.Item>
        )}
      />
      <Pagination defaultCurrent={1} total={numItem} defaultPageSize={12} hideOnSinglePage onChange={changePage}/>
      </div>
      
    </Content>
    </>
  );
};

export default SearchResult;