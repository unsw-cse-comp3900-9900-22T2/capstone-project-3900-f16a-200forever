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
import {
  DislikeFilled,
  DislikeOutlined,
  LikeFilled,
  LikeOutlined,
} from "@ant-design/icons";
import { useEffect } from "react";
import openNotification from "./Notification";
import axios from "axios";
import { UserOutlined } from '@ant-design/icons';

const { TextArea } = Input;

const CommentList = ({ comments }) => (
  <List
    dataSource={comments}
    header={`${comments.length} ${comments.length > 1 ? "replies" : "reply"}`}
    itemLayout="horizontal"
    renderItem={(props) => <Comment {...props} />}
  />
);

const data = [
  {
    actions: [<span key="comment-list-reply-to-0">Reply to</span>],
    author: "Han Solo",
    avatar: "https://joeschmoe.io/api/v1/random",
    content: (
      <p>
        We supply a series of design principles, practical patterns and high
        quality design resources (Sketch and Axure), to help people create their
        product prototypes beautifully and efficiently.
      </p>
    ),
    datetime: (
      <Tooltip
        title={moment().subtract(1, "days").format("YYYY-MM-DD HH:mm:ss")}
      >
        <span>{moment().subtract(1, "days").fromNow()}</span>
      </Tooltip>
    ),
  },
  {
    actions: [<span key="comment-list-reply-to-0">Reply to</span>],
    author: "Han Solo",
    avatar: "https://joeschmoe.io/api/v1/random",
    content: (
      <p>
        We supply a series of design principles, practical patterns and high
        quality design resources (Sketch and Axure), to help people create their
        product prototypes beautifully and efficiently.
      </p>
    ),
    datetime: (
      <Tooltip
        title={moment().subtract(2, "days").format("YYYY-MM-DD HH:mm:ss")}
      >
        <span>{moment().subtract(2, "days").fromNow()}</span>
      </Tooltip>
    ),
  },
];


const MovieReview = ({ id, userInfo, loginStatus }) => {
  const [likes, setLikes] = useState(0);
  const [dislikes, setDislikes] = useState(0);
  const [action, setAction] = useState(null);
  const [reviews, setReviews] = useState([]);
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
      .get("http://127.0.0.1:8080/movie/movie_detail", {
        params: {
          movie_id: id.replace("id=", ""),
          page: pageNum,
          review_num_per_page: 20
        },
      })
      .then(function (response) {
        console.log(response.data);
        // setMovieInfo(response.data);
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
    
  }, []);

  const like = () => {
    setLikes(1);
    setDislikes(0);
    setAction("liked");
  };

  const dislike = () => {
    setLikes(0);
    setDislikes(1);
    setAction("disliked");
  };

  const [comments, setComments] = useState([]);
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
      .post("http://127.0.0.1:8080/review/review", {
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

  const actions = [
    <Tooltip key="comment-basic-like" title="Like">
      <span onClick={like}>
        {createElement(action === "liked" ? LikeFilled : LikeOutlined)}
        <span className="comment-action">{likes}</span>
      </span>
    </Tooltip>,
    <Tooltip key="comment-basic-dislike" title="Dislike">
      <span onClick={dislike}>
        {React.createElement(
          action === "disliked" ? DislikeFilled : DislikeOutlined
        )}
        <span className="comment-action">{dislikes}</span>
      </span>
    </Tooltip>,
  ];

  return (
    <>
      {comments.length > 0 && <CommentList comments={comments} />}
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
        header={`${data.length} replies`}
        itemLayout="horizontal"
        dataSource={data}
        renderItem={(item) => (
          <li>
            <Comment
              actions={actions}
              author={<a>Han Solo</a>}
              avatar={
                <Avatar
                  src="https://joeschmoe.io/api/v1/random"
                  alt="Han Solo"
                />
              }
              content={
                <p>
                  We supply a series of design principles, practical patterns
                  and high quality design resources (Sketch and Axure), to help
                  people create their product prototypes beautifully and
                  efficiently.
                </p>
              }
              datetime={
                <Tooltip title={moment().format("YYYY-MM-DD HH:mm:ss")}>
                  <span>{moment().fromNow()}</span>
                </Tooltip>
              }
            />
          </li>
        )}
      />
    </>
  );
};

export default MovieReview;
