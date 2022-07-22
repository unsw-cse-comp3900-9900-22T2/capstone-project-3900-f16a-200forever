import {
  Form,
  Input,
  Button
} from "antd";
import "../css/FourmPage.css"
import openNotification from "./Notification";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const { TextArea } = Input;

const NewPost = ({ loginStatus, userInfo, genre_id }) => {
  const navigate = useNavigate();
  const onFinish = (values) => {
    console.log(values)
    console.log(userInfo);
    console.log(genre_id)
    if (loginStatus === false) {
      openNotification({
        "title": "please login first"
      })
      return;
    }
    axios
      .post("http://127.0.0.1:8080/thread", {
        email: userInfo.email,
        token: userInfo.token,
        genre_id: parseInt(genre_id),
        is_anonymous: 0,
        title: values.topic,
        content: values.content
      })
      .then(function (response) {
        console.log(response.data);
        openNotification({
          "title": "post successfully",
          "content": "please reload"
        })
        navigate(`/forum/id=${genre_id}`)
      })
      .catch(function (error) {
        console.log(error.response.data);
        openNotification({
          "title": "An error occur",
          "content": error.response.data.message
        })
      });
  }

  const onFinishFailed = () => {
    openNotification({
      "title": "please finish all"
    })
  }

  return (
    <div className="new-post-page">
      <div className="post-wrapper">
        {" "}
        
        <Form
          labelCol={{ span: 5}}
          wrapperCol={{ span: 20 }}
          layout="horizontal"
          onFinish={onFinish}
          onFinishFailed={onFinishFailed}
        >
          <Form.Item>New Post</Form.Item>
          <Form.Item 
            label="Topic"
            name="topic">
            <Input></Input>
          </Form.Item>
          <Form.Item 
            label="Content"
            name="content">
            <TextArea rows={4} />
          </Form.Item>
          <Form.Item>
            <Button 
              type="primary"
              htmlType="submit"
            >
              submit
            </Button>
          </Form.Item>
        </Form>
      </div>
    </div>
  );
};
export default NewPost;
