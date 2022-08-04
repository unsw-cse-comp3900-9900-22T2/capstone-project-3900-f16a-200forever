import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import Avatar from '@mui/material/Avatar';
import { useNavigate } from 'react-router-dom';
import { styled } from '@mui/material/styles';

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'center',
  color: theme.palette.text.secondary,
}));

const UserCard = ({ info }) => {
	const navigate = useNavigate();
	return (
		<Paper elevation={4}>
			<Box>
				<Stack spacing={2} alignItems="center" textAlign="center">
					<Avatar onClick={()=> { navigate(`/userprofile/${info.id}`)}} src={info.image} sx={{ height:150, width: 150}}/>
					<Item>{info.name}</Item>
					<Item>{info.email}</Item>
				</Stack>
			</Box>
		</Paper>
	)
};

export default UserCard;