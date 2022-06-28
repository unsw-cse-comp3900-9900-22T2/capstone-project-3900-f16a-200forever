import { Input, Select, Row, Col, Space, Tooltip, Divider } from "antd";
import { Image, Layout } from "antd";
const { Header, Content, Footer } = Layout;
const MovieDetail = ({ updateLoginStatus }) => {
  return (
    <Content
      style={{
        paddingTop: 70,
        background: "white",
      }}
    >
      <Row justify="left" gutter={[16, 16]}>
        <Divider orientation="left">Movie Detail</Divider>
        <Col offset={2}>
          <div>
            <Image
              width={200}
              src=" https://image.tmdb.org/t/p/w600_and_h900_bestv2/fZ0rzH83nprexRjNn9IQBVDq5rf.jpg"
            ></Image>
          </div>
        </Col>

        <Row  offset={4}>
          <Col span ={8} push={9}>aaa</Col>
          <Col>aaa</Col>
          <Col>aaa</Col>
          hello
        </Row>
      </Row>
    </Content>
  );
};
export default MovieDetail;
