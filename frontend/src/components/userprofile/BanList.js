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

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'center',
  color: theme.palette.text.secondary,
}));

const BanList = ({ setAlertInfo }) => {
	const { id }  = useParams();
	const [banlist, setBanlist] = useState([]);
	const navigate = useNavigate();

	useEffect(() => {
		setAlertInfo({
			status: 2,
			msg: "loading"
		});
		axios
			.get(`http://127.0.0.1:8080/user/bannedlist`, {
				params: {
					"user_id": id
				}
			})
			.then(function (response) {
				console.log(response.data);
				setBanlist(response.data.list)
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
		>
				{
					banlist.map((user) => {
						console.log(user)
						return (
							<Grid item xs={2}>
								<Paper elevation={4}>
									<Box>
										<Stack spacing={2} alignItems="center" textAlign="center">
											<Avatar src={user.image} sx={{ height:150, width: 150}}/>
											<Item>{user.name}</Item>
											<Item>{user.email}</Item>
											<Button size="small" onClick={()=> { navigate(`/userprofile/${user.id}`)}}>View profile</Button>
										</Stack>
									</Box>
								</Paper>
							</Grid>
						)
					})
				}
		</Grid>
	)
};

export default BanList;