import {
  SortAscendingOutlined,
  SortDescendingOutlined,
  CaretUpOutlined,
} from "@ant-design/icons";
import { Breadcrumb, Layout, Menu } from "antd";
import SearchComponent from "./SearchComponent";
import { useNavigate } from "react-router-dom";
import { Card, Row, Col } from "antd";
const { Header, Content, Footer } = Layout;
const { Meta } = Card;
const searchResult = ({ updateLoginStatus }) => {
  // eslint-disable-next-line react-hooks/rules-of-hooks
  let navigate = useNavigate();

  return (
    <Content
      style={{
        paddingTop: 70,
        background: "white",
      }}
    >
      <SearchComponent classname="searchresult-searchinput"></SearchComponent>
      <SortAscendingOutlined stype={{ fontSize: 100, colour: "red" }} />
      <SortDescendingOutlined></SortDescendingOutlined>
      <CaretUpOutlined />

      <div className="site-card-wrapper">
        <Row gutter={16}>
          <Col offset={1} span={4} flex="none">
            <Card
              hoverable
              bordered={false}
              style={{}}
              cover={
                <img
                  alt="example"
                  src="https://image.tmdb.org/t/p/w600_and_h900_bestv2/hQ4pYsIbP22TMXOUdSfC2mjWrO0.jpg"
                />
              }
            >
              <Meta title="Ariel" description="www.instagram.com" />
            </Card>
          </Col>
          <Col span={4}>
            <Card
              hoverable
              bordered={false}
              style={{}}
              cover={
                <img
                  alt="example"
                  src="https://image.tmdb.org/t/p/w600_and_h900_bestv2/hQ4pYsIbP22TMXOUdSfC2mjWrO0.jpg"
                />
              }
            >
              <Meta title="Ariel" description="www.instagram.com" />
            </Card>
          </Col>
          <Col span={4}>
            <Card
              hoverable
              bordered={false}
              style={{}}
              cover={
                <img
                  alt="example"
                  src="https://image.tmdb.org/t/p/w600_and_h900_bestv2/hQ4pYsIbP22TMXOUdSfC2mjWrO0.jpg"
                />
              }
            >
              <Meta title="Ariel" description="www.instagram.com" />
            </Card>
          </Col>

          <Col span={4}>
            <Card
              hoverable
              bordered={false}
              style={{}}
              cover={
                <img
                  alt="example"
                  src="https://image.tmdb.org/t/p/w600_and_h900_bestv2/hQ4pYsIbP22TMXOUdSfC2mjWrO0.jpg"
                />
              }
            >
              <Meta title="Ariel" description="www.instagram.com" />
            </Card>
          </Col>
          <Col span={4}>
            <Card
              hoverable
              bordered={false}
              style={{}}
              cover={
                <img
                  alt="example"
                  src="https://image.tmdb.org/t/p/w600_and_h900_bestv2/hQ4pYsIbP22TMXOUdSfC2mjWrO0.jpg"
                />
              }
            >
              <Meta title="Ariel" description="www.instagram.com" />
            </Card>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={4} offset = {1}>
            <Card
              hoverable
              bordered={false}
              style={{}}
              cover={
                <img
                  alt="example"
                  src="https://image.tmdb.org/t/p/w600_and_h900_bestv2/hQ4pYsIbP22TMXOUdSfC2mjWrO0.jpg"
                />
              }
            >
              <Meta title="Ariel" description="www.instagram.com" />
            </Card>
          </Col>
          <Col span={4}>
            <Card
              hoverable
              bordered={false}
              style={{}}
              cover={
                <img
                  alt="example"
                  src="https://image.tmdb.org/t/p/w600_and_h900_bestv2/hQ4pYsIbP22TMXOUdSfC2mjWrO0.jpg"
                />
              }
            >
              <Meta title="Ariel" description="www.instagram.com" />
            </Card>
          </Col>
          <Col span={4}>
            <Card
              hoverable
              bordered={false}
              style={{}}
              cover={
                <img
                  alt="example"
                  src="https://image.tmdb.org/t/p/w600_and_h900_bestv2/hQ4pYsIbP22TMXOUdSfC2mjWrO0.jpg"
                />
              }
            >
              <Meta title="Ariel" description="www.instagram.com" />
            </Card>
          </Col>

          <Col span={4}>
            <Card
              hoverable
              bordered={false}
              style={{}}
              cover={
                <img
                  alt="example"
                  src="https://image.tmdb.org/t/p/w600_and_h900_bestv2/hQ4pYsIbP22TMXOUdSfC2mjWrO0.jpg"
                />
              }
            >
              <Meta title="Ariel" description="www.instagram.com" />
            </Card>
          </Col>
          <Col span={4}>
            <Card
              hoverable
              bordered={false}
              style={{}}
              cover={
                <img
                  alt="example"
                  src="https://image.tmdb.org/t/p/w600_and_h900_bestv2/hQ4pYsIbP22TMXOUdSfC2mjWrO0.jpg"
                />
              }
            >
              <Meta title="Ariel" description="www.instagram.com" />
            </Card>
          </Col>
        </Row>
      </div>
    </Content>
  );
};
export default searchResult;
