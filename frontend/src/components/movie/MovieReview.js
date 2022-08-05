import { useNavigate } from 'react-router-dom';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Avatar from '@mui/material/Avatar';
import FavoriteIcon from '@mui/icons-material/Favorite';
import Fab from '@mui/material/Fab';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import ThumbDownIcon from '@mui/icons-material/ThumbDown';
import { useState } from 'react';
import Rating from '@mui/material/Rating';

import IconButton from '@mui/material/IconButton';

import DeleteIcon from '@mui/icons-material/Delete';
import axios from 'axios';

const MovieReview = ({ review, setAlertInfo }) => {
	const navigate = useNavigate();
	const imgLink = "";
	const [up, setUp] = useState(review.likes_count);
	const [down, setDown] = useState(review.unlikes_count);

	const react = (option) => {
		var type = "";
		if (option === 0) {
			type = "like"
		} else {
			type = "unlike"
		}
		if (localStorage.getItem('token') === null) {
			setAlertInfo({
        status: 2,
        msg: "Please login",
      });
			return;
		}

		axios
      .post(`http://127.0.0.1:8080/review/react?review_id=${review.id}&reaction=${type}`, {
        email: localStorage.getItem("email"),
        token: localStorage.getItem("token")
      })
      .then(function (response) {
        console.log(response.data);
				if (response.data.is_remove === 1) {
					if (option === 0) {
						setUp(up + 1);
						setAlertInfo({
							status: 1,
							msg: "Like",
						});
					} else {
						setDown(down + 1);
						setAlertInfo({
							status: 1,
							msg: "Dislike",
						});
					}
				} else {
					if (option === 0) {
						setUp(up - 1);
						setAlertInfo({
							status: 1,
							msg: "Redo Like",
						});
					} else {
						setDown(down - 1);
						setAlertInfo({
							status: 1,
							msg: "Redo Dislike",
						});
					}
				}
      })
      .catch(function (error) {
        console.log(error.response.data);
				setAlertInfo({
					status: 3,
					msg: error.response.data.message
				});
      });
	}

	const doDelete = () => {
		if (localStorage.getItem('token') === null) {
			setAlertInfo({
        status: 2,
        msg: "Please login",
      });
			return;
		}
		axios
			.delete("http://127.0.0.1:8080/review", {
				data:{
					review_id: review.id,
					email: localStorage.getItem("email"),
        	token: localStorage.getItem("token")
			}})
			.then(function (response) {
				console.log(response.data);
				setAlertInfo({
					status: 1,
					msg: response.data.message
				});
				navigate(0);
			})
			.catch(function (error) {
				console.log(error.response);
				setAlertInfo({
					status: 3,
					msg: error.response.data.message
				});
			});
	}

  return (
		<Paper style={{ padding: "40px 20px"}}>
			<Grid container wrap="nowrap" spacing={2}>
				<Grid item onClick={() => { navigate(`/userprofile/${review.user_id}`)}}>
					<Avatar src={review.user_image}/>
				</Grid>
				<Grid justifyContent="left" item xs zeroMinWidth>
					<h4 style={{ margin: 0, textAlign: "left" }} onClick={() => { navigate(`/userprofile/${review.user_id}`)}}>
						{review.user_name}&nbsp;&nbsp;&nbsp;&nbsp;{review.user_email}
						<Rating disabled value={review.rating}></Rating>
					</h4>
					<p style={{ textAlign: "left" }}>
						{review.review_content}.{" "}
					</p>
					<p style={{ textAlign: "left", color: "gray" }}>
						{review.created_time.replace(/\..*/g, "")}	
						<IconButton aria-label="delete" size="large" onClick={doDelete}>
							<DeleteIcon />
						</IconButton>					
					</p>
				</Grid>
				<Fab aria-label="like" size='small' sx={{ ml: 3, mt: 1 }} >
					<ThumbUpIcon onClick={() => { react(0) }} />
					{up}
				</Fab>
				<Fab aria-label="like" size='small' sx={{ ml: 3, mt: 1 }} >
					<ThumbDownIcon onClick={() => { react(1) }} />
					{down}
				</Fab>
			</Grid>
		</Paper>
  )
};

export default MovieReview;
