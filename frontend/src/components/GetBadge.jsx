import { Button, Space, Table, Tag, List } from "antd";
import "../css/Badge.css";
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import { useEffect } from "react";
import axios from "axios";
import openNotification from "./Notification";
const eventList = [
  {
    title: "aaa",
    status: "bbb",
    description: "aosidjfo",
  },
  {
    title: "aaa",
    status: "bbb",
    description: "harry potter",
  },
];

const GetBadge = () => {
    const [eventList, setEventList] = useState([]);
    const getList = ()=>{
        axios
        .get("http://127.0.0.1:8080/event",{})
        .then(function (response) {
            console.log(response.data.events);
            setEventList(response.data.events)
        })
        .catch(function (error) {
            console.log(error.response);
            openNotification({
              "title": "Search error",
            })
        });    
    }
    useEffect(()=>{
      getList()
    },[]);
  return (
    <div className="get-badge-page">
      {" "}
      <div className="event-control-table">
        <List
          grid={{
            gutter: 16,
            xs: 1,
            sm: 2,
            md: 4,
            lg: 4,
            xl: 6,
            xxl: 10,
          }}
          size="large"
          header={<div>All Events</div>}
          bordered
          dataSource={eventList}
          renderItem={(item) => (
            <List.Item>
              <Link to={`/badgequestion/id=${item.id}`}>
                {/* {item} */}
                <h4>Title: {item.topic}</h4>
                <h4>Status: {item.event_status}</h4>
                <h4>Description:{item.description}</h4>
              </Link>
            </List.Item>
          )}
        />
      </div>
    </div>
  );
};
export default GetBadge;
