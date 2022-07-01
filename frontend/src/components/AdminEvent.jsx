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
import { MinusCircleOutlined, PlusOutlined } from "@ant-design/icons";
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
  const onFinish = (values) => {
    console.log("Received values of form:", values);
  };
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

  const [value, setValue] = useState(1);

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
    <div className="admin-event-component-page">
      <div className="admin-event-control-form">
        <Form
          labelCol={{ span: 5 }}
          wrapperCol={{ span: 15 }}
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
          <Form.Item label="Movie">
            <Select
              mode="multiple"
              allowClear
              style={{
                width: "100%",
              }}
              placeholder="Please select"
              defaultValue={["Harry potter", "lalaland"]}
            >
              {}
            </Select>
            <br />
          </Form.Item>
          {/* description */}
          <Form.Item label="Description">
            <TextArea rows={4} />
          </Form.Item>
          <Form.Item label="Add question">
            <Form.List name="question">
              {(fields, { add, remove }) => (
                <>
                  {fields.map(({ key, name, ...restField }) => (
                    <Space
                      key={key}
                      style={{
                        display: "flex",
                        marginBottom: 8,
                      }}
                      align="baseline"
                    >
                      <Form.Item {...restField} label="Question Descriotion">
                        <TextArea rows={4} />
                      </Form.Item>
                      <Form.Item>
                        <Radio.Group>
                          <Space direction="vertical">
                            <Radio value={1}>
                              <Input
                                style={{
                                  width: 300,
                                  marginLeft: 10,
                                }}
                              />
                            </Radio>
                            <Radio value={2}>
                              <Input
                                style={{
                                  width: 300,
                                  marginLeft: 10,
                                }}
                              />
                            </Radio>
                            <Radio value={3}>
                              <Input
                                style={{
                                  width: 300,
                                  marginLeft: 10,
                                }}
                              />
                            </Radio>
                            <Radio value={4}>
                              <Input
                                style={{
                                  width: 300,
                                  marginLeft: 10,
                                }}
                              />
                            </Radio>
                          </Space>
                        </Radio.Group>
                      </Form.Item>
                      <MinusCircleOutlined onClick={() => remove(name)} />
                    </Space>
                  ))}
                  <Form.Item>
                    <Button
                      type="dashed"
                      onClick={() => add()}
                      block
                      icon={<PlusOutlined />}
                    >
                      Add field
                    </Button>
                  </Form.Item>
                </>
              )}
            </Form.List>
          </Form.Item>
        </Form>{" "}
        <Form
          name="dynamic_form_nest_item"
          onFinish={onFinish}
          autoComplete="off"
        ></Form>
      </div>
    </div>
  );
};
export default AdminEvent;
