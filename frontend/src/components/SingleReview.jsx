import { DislikeFilled, DislikeOutlined, LikeFilled, LikeOutlined } from '@ant-design/icons';
import { Avatar, Comment, Rate, Tooltip } from 'antd';
import axios from 'axios';
import React, { createElement, useState } from 'react';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import openNotification from './Notification';

const SingleReview = ({ item, userInfo, loginStatus }) => {
	const [likes, setLikes] = useState(0);
  const [dislikes, setDislikes] = useState(0);
  const [rating, setRating] = useState(0);
  const [action, setAction] = useState(null);
  const [display, setDisplay] = useState(true);
	const navigate = useNavigate();

  useEffect(() => {
    setLikes(item.likes_count);
    setDislikes(item.unlikes_count);
    setRating(item.rating);
  }, []);

  const loginAlarm = () => {
    openNotification({
      "title": "An error occur",
      "content": "please login first"
    })
  }

  const like = () => {
    if (loginStatus === false) {
      loginAlarm();
      return;
    }
    axios
      .post(`http://127.0.0.1:8080/review/react?review_id=${item.id}&reaction=like`, {
        email: userInfo.email,
        token: userInfo.token
      })
      .then(function (response) {
        console.log(response.data);
        if (response.data.is_remove === 1) {
          setLikes(item.likes_count + 1);
          setAction('liked');
        } else {
          setLikes(item.likes_count - 1);
          setAction("none");
          openNotification({
            "title": "you removed your like"
          })
        }
      })
      .catch(function (error) {
        console.log(error.response.data);
        openNotification({
          "title": "An error occur",
          "content": error.response.data.message
        })
      });
  };

  const dislike = () => {
    if (loginStatus === false) {
      loginAlarm();
      return;
    }
    console.log(likes)
    console.log(item.id)
    console.log(item.likes_count)
    axios
      .post(`http://127.0.0.1:8080/review/react?review_id=${item.id}&reaction=unlike`, {
        email: userInfo.email,
        token: userInfo.token
      })
      .then(function (response) {
        console.log(response.data);
        if (response.data.is_remove === 1) {
          setDislikes(item.unlikes_count + 1);
          setAction('disliked');
        } else {
          setDislikes(item.unlikes_count - 1);
          setAction("none");
          openNotification({
            "title": "you removed your dislike"
          })
        }
      })
      .catch(function (error) {
        console.log(error.response.data);
        openNotification({
          "title": "An error occur",
          "content": error.response.data.message
        })
      });
  };

  const delete_review = () => {
    if (loginStatus === false) {
      loginAlarm();
      return;
    }
    console.log(item.id);
    console.log(userInfo.token)
    axios
      .delete("http://127.0.0.1:8080/review", {
        data: {
          email: userInfo.email,
          token: userInfo.token,
          review_id: item.id
        }
      })
      .then(function (response) {
        console.log(response.data);
        setDisplay(false)
      })
      .catch(function (error) {
        console.log(error.response.data);
        openNotification({
          "title": "An error occur when deleting a review",
          "content": error.response.data.message
        })
      });
  }

  const actions = [
    <Tooltip key="comment-basic-like" title="Like">
      <span onClick={like}>
        {createElement(action === 'liked' ? LikeFilled : LikeOutlined)}
      </span>
    </Tooltip>,
    <span className="comment-action">{likes}</span>,
    <Tooltip key="comment-basic-dislike" title="Dislike">
      <span onClick={dislike}>
        {React.createElement(action === 'disliked' ? DislikeFilled : DislikeOutlined)}
      </span>
    </Tooltip>,
    <span className="comment-action">{dislikes}</span>,
    <span onClick={delete_review}>DELETE</span>,
  ];
	return (
    <>
    {
      display === true ? 
        <Comment
        actions={actions}
        author={<a onClick={() => {navigate(`/userprofile/${item.user_id}`)}}>{item.user_name}</a>}
        avatar={
          <Avatar
            src={ item.user_image !== null ? item.user_image : "https://joeschmoe.io/api/v1/random" }
            alt={item.user_name}
          />
        }
        content={
          <>
          <p>{item.review_content}</p>
          </>
        }
        datetime={
          <Tooltip>
            <>
            <Rate disabled defaultValue={item.rating}></Rate>
            {/* <space></space> */}
            <span>{item.created_time}</span>
            </>
          </Tooltip>
        }
      />
      :
      null
    }
    </>
	)
}

export default SingleReview;
