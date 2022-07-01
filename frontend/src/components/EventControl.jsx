import { Button, Space, Table, Tag, List } from "antd";
import "../css/AdminPages.css";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { useEffect } from "react";
import axios from "axios";
import AdminHeader from "./AdminHeader";

const data = [
  "Racing car sprays burning fuel into crowd.",
  "Japanese princess to wed commoner.",
  "Australian walks 100km after outback crash.",
  "Man charged over missing wedding girl.",
  "Los Angeles battles huge wildfires.",
];
const EventControl = () => {
  let navigate = useNavigate();
  const [eventList, setEventList] = useState([]);
  useEffect(() => {
    axios
      .get("http://127.0.0.1:8080/event")
      .then(function (response) {
        console.log(response.data);
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
          size="large"
          header={<div>All Events</div>}
          bordered
          dataSource={data}
          renderItem={(item) => <List.Item>{item}</List.Item>}
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
