import { Button, Space, Table, Tag, List } from "antd";
import "../css/Badge.css";
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import { useEffect } from "react";
import axios from "axios";
import openNotification from "./Notification";

const GetBadge = ({ loginStatus, userInfo}) => {
  const [eventList, setEventList] = useState([]);
  const navigate = useNavigate();

  const attend = (event_id) => {
    // console.log(event_id)
    navigate(`/badgequestion/id=${event_id}`)
    // if (!loginStatus) {
    //   openNotification({
    //     "title": "please login first"
    //   })
    //   return;
    // }
    // console.log(userInfo);
    // console.log(event_id);
    // axios
    //   .post("http://127.0.0.1:8080/event/attemp", {
    //     email: userInfo.email,
    //     token: userInfo.token,
    //     event_id: event_id
    //   })
    //   .then(function (response) {
    //     console.log(response.data);
    //     navigate(`/badgequestion/id=${event_id}`)
    //   })
    //   .catch(function (error) {
    //     console.log(error.response.data);
    //     openNotification({
    //       "title": "An error occur",
    //       "content": error.response.data.message
    //     })
    //   });
  }
  useEffect(()=>{
    axios
      .get("http://127.0.0.1:8080/event")
      .then(function (response) {
          console.log(response.data.events);
          setEventList(response.data.events)
      })
      .catch(function (error) {
          console.log(error.response);
          openNotification({
            "title": "An error",
          })
      }); 
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
              {/* todo 
              can not goto link
               */}
              {/* <Link to={`/badgequestion/id=${item.id}`}> */}
                {/* {item} */}
                <h4>Title: {item.topic}</h4>
                <h4>Status: {item.event_status}</h4>
                <h4>Description:{item.description}</h4>
                <Button onClick={()=> {attend(item.id)}}>ATTEND</Button>
              {/* </Link> */}
            </List.Item>
          )}
        />
      </div>
    </div>
  );
};
export default GetBadge;
