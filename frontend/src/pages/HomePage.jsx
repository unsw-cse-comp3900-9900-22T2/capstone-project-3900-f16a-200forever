import React from "react";
import "../css/HomePage.css";
import SearchComponent from "../components/SearchComponent";
import { Breadcrumb, Layout, Divider,Menu , Button} from "antd";
import CurrentlyTrendingMovies from "../components/CurrentlyTrendingMovies";
import GenresInHomepage from "../components/GneresComponent";
import GenresPage from "./GenresPage"
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
          <SearchComponent type={"movie name"} order={"descending"}></SearchComponent>
          {/* <Divider orientation="left">CURENTLY TRENDING MOVIES</Divider> */}
          {/* <CurrentlyTrendingMovies></CurrentlyTrendingMovies> */}
          <Divider orientation="left">GENRES</Divider>
          <GenresInHomepage></GenresInHomepage>
          
        </Content>
      </div>
    </Layout>
  );
}
export default HomePage;
