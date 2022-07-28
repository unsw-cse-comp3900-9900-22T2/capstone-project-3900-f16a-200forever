import { Segmented } from "antd";
import "../css/FriendList.css";
import { LikeOutlined, MessageOutlined, StarOutlined } from "@ant-design/icons";
import { Avatar, List, Space } from "antd";
import React from "react";
const data = Array.from({
  length: 23,
}).map((_, i) => ({
  href: "https://ant.design",
  title: `ant design part ${i}`,
  avatar: "https://joeschmoe.io/api/v1/random",
  description:
    "Ant Design, a design language for background applications, is refined by Ant UED Team.",
  content:
    "We supply a series of design principles, practical patterns and high quality design resources (Sketch and Axure), to help people create their product prototypes beautifully and efficiently.",
}));

const IconText = ({ icon, text }) => (
  <Space>
    {React.createElement(icon)}
    {text}
  </Space>
);

const FriendList = () => {
  return (
    <div className="friend-list-page">
      <div className="wrapper">
        {" "}
        <Segmented options={["Following", "Friends"]} />
        <List
          itemLayout="vertical"
          size="large"
          pagination={{
            onChange: (page) => {
              console.log(page);
            },
            pageSize: 3,
          }}
          dataSource={data}
          footer={
            <div>
              <b>ant design</b> footer part
            </div>
          }
          renderItem={(item) => (
            <List.Item key={item.title}>
              <List.Item.Meta
                avatar={<Avatar src={item.avatar} />}
                description={item.description}
              />
              {item.content}
            </List.Item>
          )}
        />
      </div>
    </div>
  );
};
export default FriendList;
