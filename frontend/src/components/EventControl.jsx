import { Button, Space, Table, Tag, List } from "antd";
import "../css/AdminPages.css";
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import { useEffect } from "react";
import axios from "axios";
import AdminHeader from "./AdminHeader";

const EventControl = () => {
  let navigate = useNavigate();
  const [eventList, setEventList] = useState([]);
  useEffect(() => {
    axios
      .get("http://127.0.0.1:8080/event")
      .then(function (response) {
        console.log(response.data);
        setEventList(response.data.events)
        // console.log(response.data.movies[1].backdrop)
      })
      // todo handle error
      .catch(function (error) {
        console.log(error.response);
      });
  }, []);

  return (
    <div className="event-hold-page">
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
          renderItem={(item) =>
          <List.Item>
            <Link to={`/admin/event/edit/id=${item.id}`}>
            {/* {item} */}
            <h4>Title: {item.topic}</h4>
            <h4>Status: {item.event_status}</h4>
            </Link>
          </List.Item>}
        />
      </div>
      <div className="event-control-create-button">
        <center>
          <Button onClick={() => navigate("/admin/event/create")}>
            create new event
          </Button>
        </center>
      </div>
    </div>
  );
};
export default EventControl;
