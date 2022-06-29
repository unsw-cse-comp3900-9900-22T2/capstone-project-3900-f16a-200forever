import React from "react";
import "../css/HomePage.css";
import SearchComponent from "../components/SearchComponent";
import { Breadcrumb, Layout, Menu } from "antd";
const { Header, Content, Footer } = Layout;
function HomePage() {
  return (
    <Layout className="layout">
      <div className="homepage">
        {/* <Header/> */}
        <Content
          style={{
            paddingTop:70,
            background:"white"
          }}
        >
          <SearchComponent>hello world</SearchComponent>
        </Content>
      </div>
    </Layout>
  );
}
export default HomePage;
