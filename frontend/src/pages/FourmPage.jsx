import { Layout } from "antd";
import React from "react";
import "../css/FourmPage.css";
const { Header, Footer, Sider, Content } = Layout;

const ForumPage = () => {
  return (
    // <div className="forum-page">
    //   hello
    //   <div className="category">hello</div>
    //   <div className="post"></div>
    //   <div className="detail"> hello</div>
    // </div>
    <div className="forum-page">
      <Layout>
        <Header>Header</Header>
        <Layout>
          <Sider>Sider</Sider>
          <Content>Content</Content>
        </Layout>
        <Footer>Footer</Footer>
      </Layout>
    </div>
  );
};

export default ForumPage;
