import {
  Avatar,
  Rate,
  Button,
  Tooltip,
  Comment,
  Form,
  Input,
  List,
} from "antd";
import moment from "moment";
import React, { createElement, useState } from "react";
import { useEffect } from "react";
import openNotification from "./Notification";
import axios from "axios";
import { UserOutlined } from '@ant-design/icons';
import SingleReview from "./SingleReview";

const { TextArea } = Input;

const MovieReview = ({ id, userInfo, loginStatus }) => {
  const [reviews, setReviews] = useState([]);
  const [reviewsNum, setReviewNum] = useState(0);
  const [pageNum, setPageNum] = useState(1);
  const [rating, setRating] = useState(1);

  const Editor = ({ onChange, onSubmit, submitting, value }) => (
    <>
      <Form.Item>
        <TextArea rows={4} onChange={onChange} value={value} />
      </Form.Item>
      <Form.Item>
        <Rate 
          onChange={(value) => { setRating(value) }}
          defaultValue={1}
        />
      </Form.Item>
      <Form.Item>
        <Button
          htmlType="submit"
          loading={submitting}
          onClick={onSubmit}
          type="primary"
        >
          Add Comment
        </Button>
      </Form.Item>
    </>
  );

  const getReviews = () => {
    axios
      // todo change url here
      .get("http://127.0.0.1:8080/review/sort", {
        params: {
          movie_id: id.replace("id=", ""),
          type: "time",
          order: "descending",
          num_per_page: 20,
          page: 1,
        },
      })
      .then(function (response) {
        console.log(response.data);
        setReviews(response.data.reviews);
        setReviewNum(response.data.total);
      })
      // todo handle error
      .catch(function (error) {
        console.log(error.response);
        openNotification({
          "title": "Viewing page error",
        })
      });
  }

  useEffect(() => {
    getReviews()
  }, []);

  const [value, setValue] = useState("");

  const handleSubmit = () => {
    if (loginStatus === false) {
      openNotification({
        "title": "Please login first"
      })
      return
    }
    if (!value) {
      openNotification({
        "title": "Please enter some contents"
      })
      return
    }
    // console.log(value);
    // console.log(rating);
    // console.log(id);
    // console.log(userInfo);
    axios
      .post("http://127.0.0.1:8080/review", {
        movie_id: parseInt(id),
        email: userInfo.email,
        token: userInfo.token,
        rating: parseInt(rating),
        review_content: value
      })
      .then(function (response) {
        console.log(response);
        openNotification({
          "title": "Posting successfully!",
        })
      })
      .catch(function (error) {
        console.log(error.response.data);
        openNotification({
          "title": "An error occur when posting",
          "content": error.response.data.message
        })
      });
  };

  const handleChange = (e) => {
    setValue(e.target.value);
  };

  return (
    <>
      <Comment
        avatar={
          <Avatar size="large" icon={<UserOutlined/>} ></Avatar>
        }
        content={
          <Editor
            onChange={handleChange}
            onSubmit={handleSubmit}
            submitting={false}
            value={value}
          />
        }
      />
      <List
        className="comment-list"
        header={`${reviewsNum} replie(s)`}
        itemLayout="horizontal"
        dataSource={reviews}
        renderItem={(item) => (
          <li>
            <SingleReview item={item}></SingleReview>
          </li>
        )}
      />
    </>
  );
};

export default MovieReview;
