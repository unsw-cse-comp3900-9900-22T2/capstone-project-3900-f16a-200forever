import { useNavigate, useParams } from "react-router-dom";
import Typography from '@mui/material/Typography';
import axios from "axios";
import { useEffect, useState } from "react";
import Box from '@mui/material/Box';
import {Button} from "@mui/material";
import TextField from '@mui/material/TextField';
import ButtonGroup from '@mui/material/ButtonGroup';
import PostComment from "./PostComment";
import Stack from "@mui/material/Stack";
import Pagination from '@mui/material/Pagination';
import FavoriteIcon from '@mui/icons-material/Favorite';
import Fab from '@mui/material/Fab';

const pageSize = 20;

function getResult(id, page, setResult, setTotal, setInfo, setReaction, setAlertInfo) {
  axios
    .get("http://127.0.0.1:8080/thread/thread", {
      params: {
        "thread_id": id,
        "num_per_page": pageSize,
        "page": page
      }
    })
    .then(function (response) {
      console.log(response.data);
      setTotal(response.data.num_comments);
      setResult(response.data.comments);
			setInfo(response.data.thread);
			setReaction(response.data.thread.react_num);
    })
    .catch(function (error) {
      console.log(error.response);
      setAlertInfo({
        status: 3,
        msg: error.response.data.message
      });
    });
}

const PostPage = ({ setAlertInfo }) => {
	const { id } = useParams();
	const [page, setPage] = useState(1);
	const [total, setTotal] = useState(0);
  const [result, setResult] = useState([]);
	const [info, setInfo] = useState({ created_time: "", user_id: "" });
	const [reaction, setReaction] = useState(0);
	const navigate = useNavigate();

	const submit = (event) => {
		event.preventDefault();
    const data = new FormData(event.currentTarget);
		if (
      !data.get("comment").replace(/\s/g, "").length
    ) {
      setAlertInfo({
        status: 2,
        msg: "Please enter valid info",
      });
      return;
    }
		axios
      .post("http://127.0.0.1:8080/thread/comment", {
        email: localStorage.getItem("email"),
        token: localStorage.getItem("token"),
				thread_id: id,
				content: data.get("comment"),
				is_anonymous: 0
      })
      .then(function (response) {
        console.log(response);
				setAlertInfo({
					status: 1,
					msg: "Sent"
				})
				navigate(0);
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
    getResult(id, 1, setResult, setTotal, setInfo, setReaction, setAlertInfo);
  }, [])

	const delete_post = () => {
		setAlertInfo({
			status: 2,
			msg: "Operating"
		});
		axios
			.delete("http://127.0.0.1:8080/thread/thread", {
				data:{
					thread_id: id,
					email: localStorage.getItem("email"),
					token: localStorage.getItem("token")
			}})
			.then(function (response) {
				console.log(response.data);
				setAlertInfo({
					status: 1,
					msg: "Delete successfully"
				});
				navigate("/forums")
			})
			.catch(function (error) {
				console.log(error.response);
				setAlertInfo({
					status: 3,
					msg: error.response.data.message
				});
			});
	}

	const react = () => {
		setAlertInfo({
			status: 2,
			msg: "Operating"
		});
		axios
      .post("http://127.0.0.1:8080/thread/react", {
        email: localStorage.getItem("email"),
				token: localStorage.getItem("token"),
				thread_id: id
      })
      .then(function (response) {
        console.log(response);
				if (response.data.is_remove === 0) {
					setReaction(reaction - 1);
					setAlertInfo({
						status: 1,
						msg: "Unde like",
					});
				} else {
					setReaction(reaction + 1);
					setAlertInfo({
						status: 1,
						msg: "like",
					});
				}
      })
      .catch(function (error) {
        console.log(error.response.data);
        setAlertInfo({
          status: 2,
          msg: error.response.data.message,
        });
      });
	}
	
	return (
		<>
			<Typography variant="h4" component="div" sx={{ mb: 3 }}>
				Post details
			</Typography>
			<Typography variant="h5" component="div" sx={{ mb: 2, ml: 2}}>
				Topic: {info.title}
			</Typography>
			<Typography variant="h5" component="div" sx={{ mb: 2, ml: 2}}>
				Content: {info.content}
			</Typography>
			<Typography variant="caption" component="div" sx={{ ml: 2, mb: 2 }}>
			 	Created at: {info.created_time.replace(/\..*/g, "")}
			</Typography>
			<ButtonGroup  sx={{ ml: 2, mb: 2 }} variant="outlined">
				<Button onClick={() => { navigate(`/userprofile/${info.user_id}`)}}>VIEW AUTHOR</Button>
				<Button onClick={delete_post}>DELETE</Button>
			</ButtonGroup>
			<Fab aria-label="like" size='small' sx={{ ml: 3 }} >
				<FavoriteIcon onClick={react} />
				{reaction}
			</Fab>
			<Box
				component="form"
				sx={{
					'& .MuiTextField-root': { m: 1, width: '50ch' },
				}}
				noValidate
				autoComplete="off"
				onSubmit={submit}
			>
				<TextField
					margin="normal"
					required
					fullWidth
					label="Comment"
					name="comment"
					multiline
					rows={4}
				/>
				<Button
					variant="text"
					type="submit"
					sx={{ mt: 1, mb: 2 }}
				>
					POST
				</Button>
			</Box>
			<Typography variant="h4" component="div" sx={{ mt: 3 }}>
				All comments
			</Typography>

			<Box sx={{ width: '100%' }}>
				<Stack spacing={1}>
					{result.map((comment) => {
						return (
							<PostComment comment={comment}/>
						)
					})}
				</Stack>
			</Box>
			{parseInt((total - 1) / pageSize) === 0 ?
        null:
        <Pagination 
          sx={{ mt: 3 }}
          count={parseInt((total - 1) / pageSize) + 1} page={page} 
          onChange={(event, value) => { setPage(value); getResult(id, value, setResult, setTotal, setInfo, setReaction, setAlertInfo); }}/>
      }
		</>
	)
};

export default PostPage;