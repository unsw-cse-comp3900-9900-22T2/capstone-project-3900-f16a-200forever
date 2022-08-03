import { useEffect, useState } from "react";
import Typography from '@mui/material/Typography';
import {Button} from "@mui/material";
import axios from "axios";
import Pagination from '@mui/material/Pagination';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import { useNavigate, useParams } from "react-router-dom";
import Paper from '@mui/material/Paper';
import { styled } from '@mui/material/styles';

const pageSize = 20;

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'left',
  color: theme.palette.text.secondary,
}));

function getResult(id, page, setResult, setTotal, setAlertInfo) {
  axios
    .get("http://127.0.0.1:8080/thread", {
      params: {
        "genre_id": id,
        "num_per_page": pageSize,
        "page": page
      }
    })
    .then(function (response) {
      console.log(response.data);
      setTotal(response.data.num_threads);
      setResult(response.data.threads);
    })
    .catch(function (error) {
      console.log(error.response);
      setAlertInfo({
        status: 3,
        msg: error.response.data.message
      });
    });
}

const ForumPage = ({ setAlertInfo }) => {
  const { genre, id } = useParams();
	const [page, setPage] = useState(1);
	const [total, setTotal] = useState(0);
  const [result, setResult] = useState([]);
	const navigate = useNavigate();

  useEffect(() => {
    getResult(id, 1, setResult, setTotal, setAlertInfo);
  }, [])

	const submit = (event) => {
		event.preventDefault();
    const data = new FormData(event.currentTarget);
		if (
      !data.get("title").replace(/\s/g, "").length ||
      !data.get("content").replace(/\s/g, "").length
    ) {
      setAlertInfo({
        status: 2,
        msg: "Please enter valid info",
      });
      return;
    }
		axios
      .post("http://127.0.0.1:8080/thread", {
        email: localStorage.getItem("email"),
        token: localStorage.getItem("token"),
				genre_id: parseInt(id),
				is_anonymous: 0,
				title: data.get("title"),
				content: data.get("content")
      })
      .then(function (response) {
        console.log(response);
        setAlertInfo({
          status: 1,
          msg: "Post successfully!",
        });
				const temp = result;
				setResult([{
					id: response.data.thread_id,
					title: data.get("title"),
					content: data.get("content"),
					created_time: new Date().toLocaleString()
				}].concat(result))
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
				Forum of genre: {genre}
			</Typography>

			<Typography variant="h5" component="div" sx={{ ml:2, mb: 3 }}>
				Posting new thread here
			</Typography>

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
					label="Title"
					name="title"
					multiline
					rows={1}
				/>
				<TextField
					margin="normal"
					required
					fullWidth
					label="Content"
					name="content"
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

			<Typography variant="h5" component="div" sx={{ ml:2, mb: 3, mt: 3}}>
				All posts
			</Typography>

			<Box sx={{ width: '100%' }}>
				<Stack spacing={2}>
					{result.map((post) => {
						return (
						<Item
						// todo url
							onClick={() => { navigate(`/forum/${post.id}`)}}>
							<Typography variant="subtitle1" component="div" sx={{ ml: 4 }}>
								Title: {post.title}
							</Typography>
							<Typography variant="body2" component="div" sx={{ ml: 2 }}>
								Content: {post.content}
							</Typography>
							<Typography variant="caption" component="div" sx={{ ml: 2 }}>
								Created at: {post.created_time.replace(/\..*/g, "")}
							</Typography>
						</Item>)
					})}
				</Stack>
			</Box>

      {parseInt((total - 1) / pageSize) === 0 ?
        null:
        <Pagination 
          sx={{ mt: 3 }}
          count={parseInt((total - 1) / pageSize) + 1} page={page} 
          onChange={(event, value) => { setPage(value); getResult(id, value, setResult, setTotal, setAlertInfo); }}
          />
      }
		</>
  )
};

export default ForumPage;