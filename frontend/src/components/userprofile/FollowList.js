import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Grid from '@mui/material/Grid';
import axios from "axios";
import UserCard from "./UserCard";
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import Avatar from '@mui/material/Avatar';
import { useNavigate } from 'react-router-dom';
import { styled } from '@mui/material/styles';
import { Button } from "@mui/material";
import Typography from '@mui/material/Typography';
import MovieCard from "../movie/MovieCard";

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'center',
  color: theme.palette.text.secondary,
}));

const FollowList = ({ setAlertInfo }) => {
	const { id }  = useParams();
	const [followers, setFollowers] = useState([]);
	const [reviews, setReviews] = useState([]);
	const [target, setTarget] = useState("");
	const navigate = useNavigate();

	const getReviews = (target) => {
		// console.log(localStorage.getItem("email"));
		// console.log(localStorage.getItem("token"))
		setAlertInfo({
			status: 2,
			msg: "loading"
		});
		axios
      .post("http://127.0.0.1:8080/user/followlist/reviews", {
        email: localStorage.getItem("email"),
				token: localStorage.getItem("token"),
				page_num: 1,
				num_per_page: 100,
				follow_id: target
      })
      .then(function (response) {
        console.log(response.data.reviews);
				setReviews(response.data.reviews)
      })
      .catch(function (error) {
        console.log(error.response.data);
        setAlertInfo({
          status: 3,
          msg: error.response.data.message,
        });
      });
	}

	useEffect(() => {
		setAlertInfo({
			status: 2,
			msg: "loading"
		});
		axios
			.get(`http://127.0.0.1:8080/user/followlist`, {
				params: {
					"user_id": localStorage.getItem("id")
				}
			})
			.then(function (response) {
				console.log(response.data);
				setFollowers(response.data.list)
			})
			.catch(function (error) {
				console.log(error.response);
				setAlertInfo({
					status: 3,
					msg: error.response.data.message
				});
			});
	}, [])

	return (
		<Grid
			container
			direction="row"
			justifyContent="center"
			alignItems="flex-start"
		>
			<Grid container item xs={2}>
				{
					followers.map((user) => {
						console.log(user)
						return (
							<Grid item xs={12}>
								<Paper elevation={4}>
									<Box>
										<Stack spacing={2} alignItems="center" textAlign="center">
											<Avatar onClick={() => setTarget(user.id)} src={user.image} sx={{ height:150, width: 150}}/>
											<Item>{user.name}</Item>
											<Item>{user.email}</Item>
											<Button size="small" onClick={()=> { navigate(`/userprofile/${user.id}`)}}>View profile</Button>
											<Button size="small" onClick={() => {getReviews(user.id)}}>View reviews</Button>
										</Stack>
									</Box>
								</Paper>
							</Grid>
						)
					})
				}
			</Grid>
			<Grid container item xs={1}/>
			<Grid 
				container 
				item 
				xs={9}
				direction="column"
				justifyContent="center"
				alignItems="stretch"
			>
				<Grid item xs={12}>
					<Typography variant="h5" component="div">
						Reviews:
					</Typography>
				</Grid>
				{
					reviews.map((review) => {
						return (
							<Paper elevation={4}>
								<Grid item container direction="row"
									justifyContent="flex-start"
									alignItems="stretch"xs={12} sx={{ mb: 4 }}>
									<Grid item xs={4}>
										<Avatar onClick={() => setTarget(review.user_id)} src={review.user_image} sx={{ height:150, width: 150}}/>
									</Grid>
									<Grid item
										container 
										xs={8}
										direction="column"
										justifyContent="flex-start"
										alignItems="stretch">

									<Stack spacing={2} alignItems="left" textAlign="left">
											<Grid item xs={12}>
												<Item>{review.user_email}</Item>
												<Typography variant="h5" component="div">
													Content: {review.review_content}
												</Typography>
												<p style={{ textAlign: "left" }}>
													{review.created_time.replace(/\..*/g, "")}	
												</p>
												<Typography variant="h6" component="div">
													Movie: {review.title}
													<Button onClick={() => { navigate(`/movie/details/${review.movie_id}`); navigate(0) }}>View movie</Button>
												</Typography>
											</Grid>
											</Stack>
									</Grid>
								</Grid>		
							</Paper>
						)
					})
				}
			</Grid>
		</Grid>
	)
};

export default FollowList;