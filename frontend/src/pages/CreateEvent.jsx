import "../css/AdminPages.css";
import { useState } from "react";
import {
  Form,
  Input,
  Button,
  Radio,
  Select,
  Spin,
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
import { Upload } from "antd";
import ImgCrop from "antd-img-crop";
import { useEffect } from "react";
import axios from "axios";
import openNotification from "../components/Notification";
import debounce from 'lodash/debounce';
import React, { useMemo, useRef } from 'react';

const { RangePicker } = DatePicker;
const { TextArea } = Input;
const onChange = (time, timeString) => {
  console.log(time, timeString);
};

function fileToDataUrl(file) {
  const validFileTypes = [ 'image/jpeg', 'image/png', 'image/jpg' ]
  const valid = validFileTypes.find(type => type === file.type);
  // Bad data, let's walk away.
  if (!valid) {
      throw Error('provided file is not a png, jpg or jpeg image.');
  }
  
  const reader = new FileReader();
  const dataUrlPromise = new Promise((resolve,reject) => {
      reader.onerror = reject;
      reader.onload = () => resolve(reader.result);
  });
  reader.readAsDataURL(file);
  return dataUrlPromise;
}

function DebounceSelect({ debounceTimeout = 800, ...props }) {
  const [fetching, setFetching] = useState(false);
  const [options, setOptions] = useState([]);
  const fetchRef = useRef(0);
  const debounceFetcher = useMemo(() => {
    const loadOptions = (value) => {
      fetchRef.current += 1;
      const fetchId = fetchRef.current;
      setOptions([]);
      setFetching(true);
      axios
        .get("http://127.0.0.1:8080/event/search", {
          params: {
            keyword: value
          }
        })
        .then(function (response) {
          console.log(response.data);
          setOptions(["jfslkd", "fdjsk"])
          setFetching(false);
        })
        .catch(function (error) {
          console.log(error.response);
          setFetching(false);
          openNotification({
            "title": "An error",
          })
        });
    };
    return debounce(loadOptions, debounceTimeout);
  }, [debounceTimeout]);
  return (
    <Select
      labelInValue
      filterOption={false}
      onSearch={debounceFetcher}
      notFoundContent={fetching ? <Spin size="small" /> : null}
      {...props}
      options={options}
    />
  );
} 



const CreateEvent = () => {
  const [detail, setDetail] = useState({});
  const [base64, setBase64] = useState("");
  const [movies, setMovies] = useState([]);

  const getMovies = (keywords) => {
    axios
      .get("http://127.0.0.1:8080/event/search", {
        params: {
          keyword: keywords
        }
      })
      .then(function (response) {
        console.log(response.data);
      })
      .catch(function (error) {
        console.log(error.response);
        openNotification({
          "title": "An error",
        })
      });
  }

  const onFinish = (values) => {
    console.log("Received values of form:", values);
    setDetail(values);
  };
  const CreateForonFinish = (values) => {
    // setDetail(values)
    console.log("form console log:", values);
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
    <div className="admin-create-event">
      <div className="admin-event-component-page">
      <div className="admin-event-control-form">
        <Form
          labelCol={{ span: 5 }}
          wrapperCol={{ span: 15 }}
          layout="horizontal"
          onFinish={CreateForonFinish}
        >
          <Form.Item>
      
          </Form.Item>
          <Form.Item label="Topic">
            <Input></Input>
          </Form.Item>
          {/* duration */}
          <Form.Item label="Duration">
            <Input></Input>
            <span>min(s)</span>
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
                accept=".png,.jpeg,.jpg"
                beforeUpload={ (file) => {
                  fileToDataUrl(file).
                  then((data) => {
                    setBase64(data);
                  })
                  return false;
                }}
              >
                {fileList.length < 1 && "+ Upload"}
              </Upload>
            </ImgCrop>
          </Form.Item>
          <Form.Item label="Movie">
            <DebounceSelect
              mode="multiple"
              value={movies}
              placeholder="Select users"
              // fetchOptions={fetchUserList}
              onChange={(newValue) => {
                setMovies(newValue);
              }}
              style={{
                width: '100%',
              }}
            />
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

      <center>
        <Button type="primary" ghost onClick={() => {console.log(detail)}}>
          create a new event
        </Button>
      </center>
    </div>
  );
};
export default CreateEvent;
