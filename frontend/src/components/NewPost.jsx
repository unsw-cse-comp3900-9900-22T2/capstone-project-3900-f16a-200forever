import {
  Form,
  Input,
  Button,
  Radio,
  Select,
  Cascader,
  DatePicker,
  InputNumber,
  TreeSelect,
  Switch,
  Checkbox,
  TimePicker,
} from "antd";
import "../css/FourmPage.css"
const { TextArea } = Input;

const NewPost = () => {
  return (
    <div className="new-post-page">
      <div className="post-wrapper">
        {" "}
        
        <Form
          labelCol={{ span: 5}}
          wrapperCol={{ span: 20 }}
          layout="horizontal"
        >
          <Form.Item>New forum</Form.Item>
          <Form.Item label="Topic">
            <Input></Input>
          </Form.Item>
          <Form.Item label="Content">
            <TextArea rows={4} />
          </Form.Item>
          <Form.Item>
            <Button>submit</Button>
          </Form.Item>
        </Form>
      </div>
    </div>
  );
};
export default NewPost;
