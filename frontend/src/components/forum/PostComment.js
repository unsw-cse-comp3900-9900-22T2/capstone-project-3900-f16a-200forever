import { useNavigate } from 'react-router-dom';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Avatar from '@mui/material/Avatar';

const PostComment = ({ comment }) => {
	const navigate = useNavigate();
	const imgLink = "";

  return (
		<Paper style={{ padding: "40px 20px", marginTop: 100 }}>
			<Grid container wrap="nowrap" spacing={2}>
				<Grid item onClick={() => { navigate(`/userprofile/${comment.user_id}`)}}>
					<Avatar src={comment.user_image}/>
				</Grid>
				<Grid justifyContent="left" item xs zeroMinWidth>
					<h4 style={{ margin: 0, textAlign: "left" }} onClick={() => { navigate(`/userprofile/${comment.user_id}`)}}>
						{comment.user_email}
					</h4>
					<p style={{ textAlign: "left" }}>
						{comment.content}.{" "}
					</p>
					<p style={{ textAlign: "left", color: "gray" }}>
						{comment.comment_time.replace(/\..*/g, "")}
					</p>
				</Grid>
				
			</Grid>
		</Paper>
  )
};

export default PostComment;
