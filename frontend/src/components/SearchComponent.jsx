import { Input, Select, Row, Col, Space, Tooltip, Divider } from "antd";
import { AudioOutlined } from "@ant-design/icons";
import "../css/SearchComponent.css";
import { useNavigate } from "react-router-dom";
import openNotification from "./Notification";
import { useState } from "react";
import axios from "axios";

const { Search } = Input;
const { Option } = Select;

const SearchComponent = ({ updateLoginStatus }) => {
  let navigate = useNavigate();
  const [searchTag, setSearchTag] = useState("name");

  const updateSearchTag = (tag) => {
    // console.log(tag);
    setSearchTag(tag);
  }

  const onSearch = (value) => {
    console.log(value);
    if (value === "") {
      openNotification({
        "title": "Search Error",
        "content": "Please enter some keywords"
      })
      return;
    }
    // todo change url
    axios
      .get("/url", {
        token: "token"
      })
      .then(function (response) {
        console.log(response);
        // todo change url here
        // navigate("/");
      })
      .catch(function (error) {
        console.log(error);
        openNotification({
          "title": "Search error",
          "content": error
        })
      });
  };

  return (
    <div className="search-input">
      <Divider orientation="left">Search</Divider>
      <Row>
        <Col offset = {1}flex="100px">
          <Select defaultValue="By movie name" onChange={updateSearchTag}>
            <Option value="name">By movie name</Option>
            <Option value="genre">By genre</Option>
            <Option value="director">By director</Option>
          </Select>
        </Col>
        <Col span={8} flex="auto">
          <Search
            placeholder="input search text"
            enterButton="Search"
            size="mid"
            onSearch={onSearch}
          />
        </Col>
      </Row>
     
    </div>
  );
};

export default SearchComponent;
