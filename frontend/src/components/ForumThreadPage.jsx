import { Avatar, List } from "antd";
import React from "react";
import "../css/ThreadPage.css";
import NewPost from "./NewPost";
import { useParams } from "react-router-dom";
import { useEffect } from "react";

const data = [
  {
    title: "Ant Design Title 1",
  },
  {
    title: "Ant Design Title 2",
  },
  {
    title: "Ant Design Title 3",
  },
  {
    title: "Ant Design Title 4",
  },
];

const ForumThreadPage = ({ loginStatus, userInfo }) => {
  const { id } = useParams();
  const id_val = id.replace("id=", "")

  // useEffect({
    
  // }, []);

  return (
    <div className="thread-page">
      {" "}
      <NewPost loginStatus={loginStatus} userInfo={userInfo} genre_id={id_val}></NewPost>
      <div className="thread-wrapper">
        
        <List
          itemLayout="horizontal"
          dataSource={data}
          renderItem={(item) => (
            <List.Item>
              <List.Item.Meta
                avatar={<Avatar src="https://joeschmoe.io/api/v1/random" />}
                title={<a href="https://ant.design">{item.title}</a>}
                description="Ant Design, a design language for background applications, is refined by Ant UED Team"
              />
            </List.Item>
          )}
        />
      </div>
    </div>)
};

export default ForumThreadPage;
