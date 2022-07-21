import { Radio, Button, Form } from "antd";
import axios from "axios";
import React, { useState } from "react";
import { useEffect } from "react";
import { useParams } from "react-router-dom";
const BadgeQuestion = () => {
  const { id } = useParams();
  const [value1, setValue1] = useState(1);
  const [value2, setValue2] = useState(1);
  const [question, setquestion] = useState([]);
  const onChange1 = (e) => {
    console.log("radio checked", e.target.value);
    setValue1(e.target.value);
  };
  const onChange2 = (e) => {
    console.log("radio checked", e.target.value);
    setValue2(e.target.value);
  };
  
  const submitQuestion = () => {
    axios.get()
  };

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8080/event/detail", {
        params: { id: id.replace("id=", "") },
      })
      .then(function (response) {
        console.log(response.data);
        setquestion(response.data.questions);
        console.log(Object.keys(question));
      })
      .catch(function (error) {
        console.log(error.response.data);
      });
  });
  return (
    <div className="badge-question-page">
      <div className="badge-question-wrapper">
        {" "}
        <Form>
          {" "}
          <Form.Item>
            {" "}
            <header style={{ fontSize: "large" }}>
              Answer Question and Get Badge!
            </header>
          </Form.Item>
          <Form.Item>
            {" "}
            <div className="title-area">
              {" "}
              <text>{Object.keys(question)[0]}</text>
            </div>
          </Form.Item>
          <Form.Item>
            {" "}
            <div className="ratio-area">
              {" "}
              <Radio.Group onChange={onChange1} value={value1}>
                {/* todo 
                here is a bug, don't know how to get the value in a list*/}
                <Radio value={1}>{Object.keys(question)[0][0]}</Radio>
                <Radio value={2}>{Object.keys(question)[0][1]}</Radio>
                <Radio value={3}>{Object.keys(question)[0][2]}</Radio>
              </Radio.Group>
            </div>
          </Form.Item>
          <Form.Item>
            {" "}
            <div className="title-area">
              {" "}
              <text>jjjj{Object.keys(question)[1]}</text>
            </div>
          </Form.Item>
          <Form.Item>
            {" "}
            <div className="ratio-area">
              {" "}
              <Radio.Group onChange={onChange2} value={value2}>
                {/* todo 
                here is a bug, don't know how to get the value in a list*/}
                <Radio value={1}>{Object.values(Object.keys(question)[0])}</Radio>
                <Radio value={2}>{Object.keys(question)[1][1]}</Radio>
                <Radio value={3}>{Object.keys(question)[1][2]}</Radio>
              </Radio.Group>
            </div>
          </Form.Item>
          <Button onClick={submitQuestion}>submit</Button>
        </Form>
      </div>
    </div>
  );
};

export default BadgeQuestion;
