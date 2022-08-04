import axios from "axios";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Grid from '@mui/material/Grid';
import Avatar from '@mui/material/Avatar';
import ReactCrop from 'react-image-crop'
import {Button} from "@mui/material";
import Typography from '@mui/material/Typography';
import Box from "@mui/material/Box";
import ButtonGroup from '@mui/material/ButtonGroup';
import TextField from "@mui/material/TextField";

function fileToDataUrl(file) {
  const validFileTypes = [ 'image/jpeg', 'image/png', 'image/jpg' ]
  const valid = validFileTypes.find(type => type === file.type);
  // Bad data, let's walk away.
  if (!valid) {
      throw Error('provided file is not a png, jpg or jpeg image.');
  }
  
  const reader = new FileReader();
  const dataUrlPromise = new Promise((resolve,reject) => {
      reader.onerror = reject;
      reader.onload = () => resolve(reader.result);
  });
  reader.readAsDataURL(file);
  return dataUrlPromise;
}

const Userprofile = ({ setAlertInfo }) => {
	const { id } = useParams();
	const [profile, setProfile] = useState({});
	const [newInfo, setNewInfo] = useState({});
	const [isEdit, setIsEdit] = useState(false);
	const [base64, setBase64] = useState("");
	const [list, setList] = useState([]);
	const [reviews, setReviews] = useState([]);
	const [isError, setIsError] = useState(false);
	const navigate = useNavigate();

	useEffect(() => {
    axios
			.get("http://127.0.0.1:8080/user/userprofile", {
				params: {
					"user_id": id
				}
			})
			.then(function (response) {
				console.log(response.data);
				setProfile(response.data);
				setNewInfo({
					username: response.data.username,
					signature: response.data.signature,
					image: response.data.profile_picture,
					current_password: "",
					new_password: "",
					double_check: "",
					email: localStorage.getItem("email"),
					token: localStorage.getItem("token")
				});
			})
			.catch(function (error) {
				console.log(error.response);
				setAlertInfo({
          status: 3,
          msg: error.response.data.message
        });
			});
	}, [])

	const changeProfile = () => {
		console.log(newInfo)
		if (isError === true) {
			setAlertInfo({
				status: 3,
				msg: "Please enter valid password"
			});
			return;
		}
		var body = {
			email: newInfo["email"],
			token: newInfo.token,
			username: newInfo.username,
			signature: newInfo.signature,
			image: newInfo.image
		};
		if (newInfo.current_password.replace(/\s/g, "").length &&
				newInfo.new_password.replace(/\s/g, "").length &&
				newInfo.double_check.replace(/\s/g, "").length)
		{
			body.current_password = newInfo.current_password
			body.new_password = newInfo.new_password
			body.double_check = newInfo.double_check
		} else {
			setAlertInfo({
				status: 2,
				msg: "Enter valid password if you want to change"
			});
		}

		axios
			.put(`http://127.0.0.1:8080/user/userprofile?user_id=${id}`, body)
			.then(function (response) {
				setAlertInfo({
					status: 1,
					msg: "Saved"
				});
				navigate(0);
			})
			.catch(function (error) {
				setAlertInfo({
					status: 3,
					msg: error.response.data.message
				});
			});
	}

	const getList = (is_follow) => {
		console.log(is_follow)
		var type = ''
		if (is_follow === 1) {
			type = "follow"
		} else {
			type = "ban"
		}
		axios
			.get(`http://127.0.0.1:8080/user/${type}list`, {
				params: {
					"user_id": localStorage.getItem("id")
				}
			})
			.then(function (response) {
				console.log(response.data);
				// todo
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
		<>
		{
			isEdit === false ?
				<Grid container spacing={2}>
				<Grid item xs={4}>
					<Avatar 
						src={profile.profile_picture}
						sx={{ width: 300, height: 300}}
					/>
				</Grid>
				<Grid container item xs={6} zeroMinWidth sx={{ mt: 3 }}>
					<Grid item xs={12} justifyContent="left">
						<Typography variant="h5" component="div">
							User name: {profile.username}
						</Typography>
					</Grid>
					<Grid item xs={12} justifyContent="left">
						<Typography variant="body" component="div">
							user_id: {profile.id}
						</Typography>
					</Grid>
					<Grid item xs={12} justifyContent="left">
						<Typography variant="h6" component="div" sx={{ mb: 2 }}>
							signature: {profile.signature}
						</Typography>
					</Grid>
					<Grid item xs={12}>
						<ButtonGroup variant="outlined" aria-label="outlined button group">
							<Button>WishList</Button>
							<Button>Watchedlist</Button>
							<Button>dropedlist</Button>
						</ButtonGroup>
					</Grid>
					<Grid item justifyContent="left">
						<Typography variant="h6" component="div" sx={{ mb: 2 }}>
							Badges:
						</Typography>
						{/* todo */}
					</Grid>
				</Grid>

				<Grid container item xs={2} zeroMinWidth sx={{ mt: 3 }}>
					<Grid item xs={12} justifyContent="left">
						<Box
							sx={{
								display: 'flex',
								'& > *': {
									m: 1,
								},
							}}
						>
							{
								localStorage.getItem("id") === id ?
									<ButtonGroup
										orientation="vertical"
										aria-label="vertical outlined button group"
									>
										{/* todo */}
										<Button onClick={()=> { getList(1) }}>
											Follow list
										</Button>
										<Button onClick={()=> { getList(0) }}>
											Banlist
										</Button>
										<Button onClick={()=> { navigate(`/user/recommend/${id}`)}}>
											Guess what you like
										</Button>
										<Button onClick={() => { setIsEdit(true) }}>
											Edit
										</Button>
									</ButtonGroup>
									:
									<ButtonGroup
										orientation="vertical"
										aria-label="vertical outlined button group"
									>
										{/* todo */}
										<Button onClick={()=> { getList(1) }}>
											Follow
										</Button>
										<Button onClick={()=> { getList(0) }}>
											ban
										</Button>
									</ButtonGroup> 
							}
						</Box>
					</Grid>
				</Grid>
			</Grid> 


			: 
				<Grid container spacing={2}>
					<Grid item container xs={4} spacing={2}>
						<Grid item xs={12}>
							<Avatar 
								src={newInfo.image}
								sx={{ width: 200, height: 200}}
							/>
						</Grid>
						<Grid item xs={12}>
							<Button variant="contained" component="label" sx={{ ml: 4}}>
								Upload
								<input hidden accept=".png,.jpeg,.jpg" type="file" onChange={
									(event) => {
										fileToDataUrl(event.target.files[0]).
											then((data) => {
												setBase64(data);
												var temp = newInfo;
												temp.image = data;
												setNewInfo(temp);
											})
											.catch(() => {
												setAlertInfo({
													status: 3,
													msg: "Upload fails"	
											})
										});
										return false;
									}}/>
							</Button>
						</Grid>
					</Grid>
						
				<Grid container item xs={6} zeroMinWidth sx={{ mt: 3 }}>
					<Grid item xs={12} justifyContent="left">
						<TextField
							margin="normal"
							required
							sx={{ minWidth: 300 }}
							id="username"
							label="Username"
							name="username"
							defaultValue={profile.username}
							onChange={(event) => {
								var temp = newInfo;
								temp.username = event.target.value;
								setNewInfo(temp)
							}}
						/>
					</Grid>
					<Grid item xs={12} justifyContent="left">
						<TextField
							margin="normal"
							disabled
							id="id"
							sx={{ minWidth: 350 }}
							label="User_id"
							name="user_id"
							defaultValue={profile.id}
						/>
					</Grid>
					<Grid item xs={12} justifyContent="left">
						<TextField
							margin="normal"
							fullWidth
							multiline
							rows={3}
							id="signature"
							label="Signature"
							name="signature"
							defaultValue={profile.signature}
							onChange={(event) => {
								var temp = newInfo;
								temp.signature = event.target.value;
								setNewInfo(temp)
							}}
						/>
					</Grid>
					<Grid item xs={12} justifyContent="left">
						
					<TextField
							margin="normal"
							id="password"
							label="Password"
							name="password"
							type="password"
							sx={{ minWidth: 350 }}
							onChange={(event) => {
								newInfo.current_password = event.target.value
							}}
						/>
					</Grid>
					<Grid item xs={12} justifyContent="left">
						
					<TextField
							margin="normal"
							id="newpassword"
							label="New Password"
							name="newpassword"
							type="password"
							sx={{ minWidth: 350 }}
							onChange={(event) => {
								newInfo.new_password = event.target.value;
							}}
						/>
					</Grid>
					<Grid item xs={12} justifyContent="left">
						<TextField
							error={isError}
							margin="normal"						
							id="confirm_password"
							label="Confirm Password"
							name="confirm_password"
							type="password"
							sx={{ minWidth: 350 }}
							onChange={(event) => {
								newInfo.double_check = event.target.value;
								if (event.target.value !== newInfo.new_password) {
									setIsError(true);
								} else {
									setIsError(false);
								}
							}}
						/>
					</Grid>




				</Grid>

				<Grid container item xs={2} zeroMinWidth sx={{ mt: 3 }}>
					<Grid item xs={12} justifyContent="left">
						<Box
							sx={{
								display: 'flex',
								'& > *': {
									m: 1,
								},
							}}
						>
							{
								localStorage.getItem("id") === id ?
									<ButtonGroup
										orientation="vertical"
										aria-label="vertical outlined button group"
									>
										{/* todo */}
										<Button onClick={changeProfile}>
											Save
										</Button>
										<Button onClick={() => { setIsEdit(false) }}>
											Back
										</Button>
									</ButtonGroup> : null
							}
						</Box>
					</Grid>
				</Grid>
			</Grid> 
		}
		</>
		
	)
};
  
export default Userprofile;




// <Button onClick={() => {console.log(base64)}}>
// asd
// </Button>
// <Button variant="contained" component="label">
// Upload
// <input hidden accept=".png,.jpeg,.jpg" type="file" onChange={
// 	(event) => {
// 		fileToDataUrl(event.target.files[0]).
// 			then((data) => {
// 				setBase64(data);
// 			})
// 			.catch(() => {
// 				setAlertInfo({
// 					status: 3,
// 					msg: "Upload fails"	
// 			})
// 		});
// 		return false;
// 	}}/>
// </Button>