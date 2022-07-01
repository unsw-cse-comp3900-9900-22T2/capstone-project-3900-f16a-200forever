import { Button, Row, Col, Card, Divider } from "antd";
import "../css/AdminPages.css";
import { useNavigate } from "react-router-dom";
const AdminControl = () => {
  let navigate = useNavigate();

  return (
    <div className="admin-control-page">
      {" "}
      <div className="admin-control-card-wrapper">
        <Row gutter={16}>
          <Col span={12} >
            <Card
              hoverable
              title="EVENT"
              onClick={() => navigate("/admin/event/control")}
              bordered={true}
            >
              Click to manage events
            </Card>
          </Col>
          <Col span={12}>
            <Card hoverable title="SET ADMIN" bordered={false}>
              Set normal user as admin
            </Card>
          </Col>
        </Row>
      </div>
    </div>
  );
};
export default AdminControl;
