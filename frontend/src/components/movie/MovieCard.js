
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { CardActionArea } from '@mui/material';
import image from "../../asset/NoMovieImg.png";
import Rating from '@mui/material/Rating';
import { useNavigate } from 'react-router-dom';

const MovieCard = ({ data }) => {
	const navigate = useNavigate();
  return (
		// todo add url
    <Card sx={{ maxWidth: 250, height: 520 }}
			onClick={() => { console.log(data.id) }}>
			<CardActionArea>
				<CardMedia
					component="img"
					height="375"
					src={
						data.backdrop === null ?
						image : data.backdrop
					}
					alt="No image"
				/>
				<CardContent>
					<Rating value={parseInt(data.total_rating / data.rating_count) } readOnly />
					<Typography component="legend">Rating: {(data.total_rating / data.rating_count).toFixed(2)}  By ({data.rating_count})</Typography>
					<Typography gutterBottom variant="h6" component="div">
						{data.title}
					</Typography>
				</CardContent>
			</CardActionArea>
		</Card>
  )
};

export default MovieCard;
