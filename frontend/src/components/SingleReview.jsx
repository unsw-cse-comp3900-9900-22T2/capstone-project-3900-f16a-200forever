import { DislikeFilled, DislikeOutlined, LikeFilled, LikeOutlined } from '@ant-design/icons';
import { Avatar, Comment, Rate, Tooltip } from 'antd';
import axios from 'axios';
import React, { createElement, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import openNotification from './Notification';

const SingleReview = ({ item, userInfo, loginStatus }) => {
	const [likes, setLikes] = useState(item.likes_count);
  const [dislikes, setDislikes] = useState(item.unlikes_count);
  const [action, setAction] = useState(null);
	const navigate = useNavigate();

  const like = () => {
    setLikes(likes + 1);
    setAction('liked');
    axios
      .post(`http://127.0.0.1:8080/review/react?review_id=${item.id}&reaction=like`, {
        email: userInfo["email"],
        token: userInfo.token
      })
      .then(function (response) {
        console.log(response.data);
      })
      .catch(function (error) {
        console.log(error.response.data);
        openNotification({
          "title": "An error occur",
        })
      });
  };

  const dislike = () => {
    setDislikes(dislikes + 1);
    setAction('disliked');
  };

  const actions = [
    <Tooltip key="comment-basic-like" title="Like">
      <span onClick={like}>
        {createElement(action === 'liked' ? LikeFilled : LikeOutlined)}
        <span className="comment-action">{likes}</span>
      </span>
    </Tooltip>,
    <Tooltip key="comment-basic-dislike" title="Dislike">
      <span onClick={dislike}>
        {React.createElement(action === 'disliked' ? DislikeFilled : DislikeOutlined)}
        <span className="comment-action">{dislikes}</span>
      </span>
    </Tooltip>,
    <span key="comment-basic-reply-to">DELETE</span>,
  ];
	return (
		<Comment
      actions={actions}
      author={<a onClick={() => {navigate("/")}}>{item.user_name}</a>}
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
          <Rate defaultValue={item.rating}></Rate>
          <span>{item.created_time}</span>
          </>
				</Tooltip>
			}
    />
	)
}

export default SingleReview;
