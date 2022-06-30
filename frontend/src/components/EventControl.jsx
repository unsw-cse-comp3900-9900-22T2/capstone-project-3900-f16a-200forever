import { Button, Space, Table, Tag } from "antd";
import "../css/AdminPages.css";
import { useNavigate } from "react-router-dom";
const columns = [
  {
    title: "event",
    dataIndex: "event",
    key: "event",
    render: (text) => <a>{text}</a>,
  },
  {
    title: "status",
    dataIndex: "status",
    key: "status",
  },
];
const data = [
  {
    key: "1",
    event: "Harry Potter",
    status: "Open",
  },
  { key: "2", event: "La La Land", status: "Closed" },
  { key: "3", event: "La La Land", status: "Closed" },
  { key: "4", event: "La La Land", status: "Closed" },
  { key: "5", event: "La La Land", status: "Closed" },
  { key: "6", event: "La La Land", status: "Closed" },
  { key: "7", event: "La La Land", status: "Closed" },
  { key: "8", event: "La La Land", status: "Closed" },
];
const EventControl = () => {
  let navigate = useNavigate();
  return (
    <span>
      {" "}
      <div className="event-control-table">
        <Table
          columns={columns}
          dataSource={data}
          scroll={{
            x: 1500,
            y: 300,
          }}
        />
      </div>
      <div className="event-control-create-button">
        <center>
          <Button onClick={() => navigate("/forgetpassword")}>
            create new event
          </Button>
        </center>
      </div>
    </span>
  );
};
export default EventControl;
