import { Input, Select, Row, Col, Space, Tooltip, Divider } from "antd";
import { AudioOutlined } from "@ant-design/icons";
import "../css/SearchComponent.css";
import { useNavigate } from "react-router-dom";

const { Search } = Input;
const { Option } = Select;

const SearchComponent = ({ updateLoginStatus }) => {
  let navigate = useNavigate();
  const onSearch = (value) => navigate("/searchresult");
  return (
    <div className="search-input">
      <Divider orientation="left">Search</Divider>
      <Row>
        <Col offset = {1}flex="100px">
          <Select defaultValue="By movie name">
            <Option value="By movie name">By movie name</Option>
            <Option value="By genre">By genre</Option>
            <Option value="By directors">By directors</Option>
          </Select>
        </Col>
        <Col span={8} flex="auto">
          <Search
            placeholder="input search text"
            enterButton="Search"
            size="large"
            maxLength={9}
            // suffix={suffix}
            onSearch={onSearch}
          />
        </Col>
      </Row>
      <Divider orientation="left">Results</Divider>
      {/* <Row gutter={[16, { xs: 8, sm: 16, md: 24, lg: 32 }]}>
        <Col span={3} offset={6}>
          <Select defaultValue="By movie name">
            <Option value="By movie name">By movie name</Option>
            <Option value="By genre">By genre</Option>
            <Option value="By directors">By directors</Option>
          </Select>
        </Col>
        <Col  offset={1}>
          <Search
            placeholder="input search text"
            enterButton="Search"
            size="large"
            // suffix={suffix}
            onSearch={onSearch}
          />
        </Col>
      </Row> */}
    </div>
  );
};

export default SearchComponent;
