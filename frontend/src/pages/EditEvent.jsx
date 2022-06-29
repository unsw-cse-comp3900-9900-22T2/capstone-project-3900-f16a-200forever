import AdminEvent from "../components/AdminEvent";
import "../css/AdminPages.css";
import { Button, Space } from "antd";
const EditEvent = () => {
  return (
    <div className="admin-edit-event">
      <AdminEvent></AdminEvent>
      <center>
        <Space size={"large"}>
          {" "}
          <Button type="primary" ghost>
            save
          </Button>
          <Button type="primary" ghost>
            publish
          </Button>
          <Button type="primary" ghost>
            end event
          </Button>
        </Space>
      </center>
    </div>
  );
};
export default EditEvent;
