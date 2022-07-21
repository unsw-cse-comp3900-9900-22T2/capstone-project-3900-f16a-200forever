import { Radio, Button } from "antd";
import React, { useState } from "react";
const BadgeQuestion = () => {
  const [value, setValue] = useState(1);

  const onChange = (e) => {
    console.log("radio checked", e.target.value);
    setValue(e.target.value);
  };

  return (
    <div className="badge-question-page">
      <div className="badge-question-wrapper">
        {" "}
        <header style={{"fontSize":"large"}}>Answer Question and Get Badge!</header>
        <div className="title-area">
          {" "}
          <text>I am question here hahahahaha</text>
        </div>
        <div className="ratio-area">
          {" "}
          <Radio.Group onChange={onChange} value={value}>
            <Radio value={1}>A</Radio>
            <Radio value={2}>B</Radio>
            <Radio value={3}>C</Radio>
            <Radio value={4}>D</Radio>
          </Radio.Group>
        </div>
        
        <div className="title-area">
          {" "}
          <text>I am question here hahahahaha</text>
        </div>
        <div className="ratio-area">
          {" "}
          <Radio.Group onChange={onChange} value={value}>
            <Radio value={1}>A</Radio>
            <Radio value={2}>B</Radio>
            <Radio value={3}>C</Radio>
            <Radio value={4}>D</Radio>
          </Radio.Group>
        </div>
        <Button>submit</Button>
      </div>
      
    </div>
  );
};

export default BadgeQuestion;
