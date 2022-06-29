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
import { Space } from "antd";
import "../css/AdminPages.css";
import { useState } from "react";
import { Upload } from "antd";
import ImgCrop from "antd-img-crop";
const { RangePicker } = DatePicker;

const { TextArea } = Input;
const onChange = (time, timeString) => {
  console.log(time, timeString);
};

const AdminEvent = () => {
  const [fileList, setFileList] = useState([
    {
      uid: "-1",
      name: "image.png",
      status: "done",
      url: "https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png",
    },
  ]);
  const onChange = ({ fileList: newFileList }) => {
    setFileList(newFileList);
  };

  const onPreview = async (file) => {
    let src = file.url;

    if (!src) {
      src = await new Promise((resolve) => {
        const reader = new FileReader();
        reader.readAsDataURL(file.originFileObj);

        reader.onload = () => resolve(reader.result);
      });
    }

    const image = new Image();
    image.src = src;
    const imgWindow = window.open(src);
    imgWindow?.document.write(image.outerHTML);
  };
  return (
    <div className="admin-event-control-form">
      <Form
        labelCol={{ span: 7 }}
        wrapperCol={{ span: 10 }}
        layout="horizontal"
      >
        <Form.Item label="Topic">
          <Input></Input>
        </Form.Item>
        {/* duration */}
        <Form.Item label="Duration">
          <TimePicker onChange={onChange} />
        </Form.Item>
        <Form.Item label="Deadline">
          {" "}
          <RangePicker />
        </Form.Item>
        {/* ddl */}
        {/* badge upload */}
        <Form.Item label="Badge">
          <ImgCrop rotate>
            <Upload
              action="https://www.mocky.io/v2/5cc8019d300000980a055e76"
              listType="picture-card"
              fileList={fileList}
              onChange={onChange}
              onPreview={onPreview}
            >
              {fileList.length < 5 && "+ Upload"}
            </Upload>
          </ImgCrop>
        </Form.Item>
        {/* description */}
        <Form.Item label="Description">
          <TextArea rows={4} />
        </Form.Item>

        {/* question and correct answer */}
        <Form.Item wrapperCol={{span: 10, offset:10}} labelCol={{span: 10, offset:8}}>
          <Button type="primary" ghost>create a new event</Button>
        </Form.Item>
      </Form>
    </div>
  );
};
export default AdminEvent;
