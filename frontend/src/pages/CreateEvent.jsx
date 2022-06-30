import AdminEvent from "../components/AdminEvent";
import "../css/AdminPages.css";
import { Button } from "antd";
const CreateEvent = () => {
  return (
    <div className="admin-create-event">
      <AdminEvent></AdminEvent>
      <center>
        <Button type="primary" ghost>
          create a new event
        </Button>
      </center>
    </div>
  );
};
export default CreateEvent;
