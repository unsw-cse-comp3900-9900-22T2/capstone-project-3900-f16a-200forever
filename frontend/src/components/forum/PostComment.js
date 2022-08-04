import { useNavigate } from 'react-router-dom';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Avatar from '@mui/material/Avatar';
import FavoriteIcon from '@mui/icons-material/Favorite';
import Fab from '@mui/material/Fab';

const PostComment = ({ comment }) => {
	const navigate = useNavigate();
	const imgLink = "";

  return (
		<Paper style={{ padding: "40px 20px", marginTop: 100 }}>
			<Grid container wrap="nowrap" spacing={2}>
				<Grid item>
					{/* todo add url to userprofile */}
					<Avatar alt="" src={imgLink} />
				</Grid>
				<Grid justifyContent="left" item xs zeroMinWidth>
					<h4 style={{ margin: 0, textAlign: "left" }}>Michel Michel</h4>
					<p style={{ textAlign: "left" }}>
						{comment.content}.{" "}
					</p>
					<p style={{ textAlign: "left", color: "gray" }}>
						{comment.comment_time.replace(/\..*/g, "")}
					</p>
				</Grid>
				
			</Grid>
				<Fab disabled aria-label="like" size='small' sx={{ ml: 3 }}>
					<FavoriteIcon />
				</Fab>
		</Paper>
  )
};

export default PostComment;
