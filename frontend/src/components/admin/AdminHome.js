import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import { useNavigate } from "react-router-dom";

const AdminHome = () => {
	const navigate = useNavigate();
	return (
		<Box sx={{ flexGrow: 1, mt: 10}}>
      <Grid container spacing={2}>
        <Grid item xs={4}>
					<Card sx={{ minWidth: 275 }} onClick={() => { navigate('/admin/events') }}>
						<CardContent>
							<Typography variant="h4" component="div">
								EVENT
							</Typography>
							<Typography variant="body2" sx={{ mt: 3}}>
								Manage event system
							</Typography>
						</CardContent>
					</Card>
        </Grid>
				{/* todo */}
        <Grid item xs={4}>
					<Card sx={{ minWidth: 275 }}>
						<CardContent>
							<Typography variant="h4" component="div">
								Set admins
							</Typography>
							<Typography variant="body2" sx={{ mt: 3}}>
								Manage event system
							</Typography>
						</CardContent>
					</Card>
        </Grid>
        <Grid item xs={4}>
					<Card sx={{ minWidth: 275 }}>
						<CardContent>
							<Typography variant="h4" component="div">
								EVENT
							</Typography>
							<Typography variant="body2" sx={{ mt: 3}}>
								Manage event system
							</Typography>
						</CardContent>
					</Card>
        </Grid>
      </Grid>
    </Box>
	)
};

export default AdminHome;