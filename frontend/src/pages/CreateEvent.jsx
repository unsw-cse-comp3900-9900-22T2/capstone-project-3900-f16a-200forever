import AdminEvent from "../components/AdminEvent";
import "../css/AdminPages.css";
import { Button } from "antd";
import { useState } from "react";

const CreateEvent = () => {
  const [detail, setDetail] = useState({});
  return (
    <div className="admin-create-event">
      <AdminEvent detail={detail} setDetail={setDetail}></AdminEvent>

      <center>
        <Button type="primary" ghost onClick={console.log(detail)}>
          create a new event
        </Button>
      </center>
    </div>
  );
};
export default CreateEvent;
