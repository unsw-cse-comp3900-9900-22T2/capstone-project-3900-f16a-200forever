import { Input, Select, Row, Col, Divider } from "antd";
import "../css/SearchComponent.css";
import { useNavigate } from "react-router-dom";
import openNotification from "./Notification";
import { useState } from "react";
import axios from "axios";

const { Search } = Input;
const { Option } = Select;

const SearchComponent = ({ type, keywords, order, changePage }) => {
  let navigate = useNavigate();
  const [searchType, setSearchType] = useState(type);
  const [searchOrder, setSearchOrder] = useState(order);
  const updateSearchType = (type) => {
    // console.log(type);
    setSearchType(type);
  }

  const updateSearchOrder = (order) => {
    setSearchOrder(order);
  }

  const onSearch = (value) => {
    console.log(value)
    if (value.length === 0 || value === "") {
      openNotification({
        "title": "Please enter some keywords"
      })
      return;
    }
    // 
    try {
      changePage(1)
    } catch (err) {
      console.log(err)
    }
    navigate(`/search/type=${searchType}/keywords=${value}/order=${searchOrder}`)   
  };

  return (
    <div className="search-input">
      <Divider orientation="left">Search</Divider>
      <Row>
        <Col offset={1} flex="100px">
          <Select className="search-type" defaultValue={`By ${type}`} onChange={updateSearchType}>
            <Option value="movie name">By movie name</Option>
            <Option value="description">By description</Option>
            <Option value="director">By director</Option>
          </Select>
        </Col>
        <Col span={8} flex="auto">
          <Search
            placeholder="input search text"
            enterButton="Search"
            size="mid"
            className="search-input-area"
            onSearch={onSearch}
            defaultValue={keywords}
          />
        </Col>
        <Col offset={1} flex="100px">
          <Select className="search-order" defaultValue={`By ${order}`} onChange={updateSearchOrder}>
            <Option value="descending">Sort: descending</Option>
            <Option value="ascending">Sort: ascending</Option>
          </Select>
        </Col>
      </Row>
      <Divider className="search-divider" orientation="left"></Divider>
    </div>
  );
};

export default SearchComponent;
