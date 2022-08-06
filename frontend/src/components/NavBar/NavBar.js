import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import MenuItem from '@mui/material/MenuItem';
import AdbIcon from '@mui/icons-material/Adb';
import logo from "../../asset/new_logo.png";
import AccountCircle from '@mui/icons-material/AccountCircle';
import { ButtonGroup } from '@mui/material';
import axios from 'axios';
import "./NavBar.css"

const NavBar = ({ setAuth, setAlertInfo }) => {
  const navigate = useNavigate();

  const [anchorElNav, setAnchorElNav] = useState(null);
  const [anchorElUser, setAnchorElUser] = useState(null);
  const [loginStatus, setLoginStatus] = useState(false);

  useEffect(() => {
    if (localStorage.getItem("token") !== null && 
      localStorage.getItem("token").replace(/\s/g, "").length &&
      localStorage.getItem("token") !== "null") {
      setLoginStatus(true);
    } else {
      setLoginStatus(false);
    }
  }, [])

  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget);
  };

  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  const logout = () => {
    setAnchorElUser(null);
    console.log(localStorage.getItem("email"));
    console.log(localStorage.getItem("token"));
    axios
      .post("http://127.0.0.1:8080/logout", {
        email: localStorage.getItem("email"),
        token: localStorage.getItem("token")
      })
      .then(function (response) {
        setAuth(null, null, null, null, false)
        navigate("/");
        setAlertInfo({
          status: 1,
          msg: "Logout!",
        });
        setLoginStatus(false);
        navigate(0);
      })
      .catch(function (error) {
        console.log(error);
        setAlertInfo({
          status: 3,
          msg: error.response.data.message
        });
      });
  }

  return (
    <AppBar position="static">
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          <Typography
            variant="h6"
            noWrap
            component="a"
            href="/"
            sx={{
              mr: 2,
              display: { xs: 'none', md: 'flex' },
              fontFamily: 'monospace',
              fontWeight: 700,
              letterSpacing: '.3rem',
              color: 'inherit',
              textDecoration: 'none',
            }}
          >
            <div className="header-logo">
              <img src={logo} alt="logo" /> 
            </div>
          </Typography>

          <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleOpenNavMenu}
              color="inherit"
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorElNav}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'left',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'left',
              }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
              sx={{
                display: { xs: 'block', md: 'none' },
              }}
            >
              {/* {pages.map((page) => (
                <MenuItem key={page} onClick={handleCloseNavMenu}>
                  <Typography textAlign="center">{page}</Typography>
                </MenuItem>
              ))} */}
              
            </Menu>
          </Box>
          <AdbIcon sx={{ display: { xs: 'flex', md: 'none' }, mr: 1 }} />
          <Typography
            variant="h5"
            noWrap
            component="a"
            href=""
            sx={{
              mr: 2,
              display: { xs: 'flex', md: 'none' },
              flexGrow: 1,
              fontFamily: 'monospace',
              fontWeight: 700,
              letterSpacing: '.3rem',
              color: 'inherit',
              textDecoration: 'none',
            }}
          >
            {/* LOGO */}
          </Typography>
          <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
            {/* <Button
              onClick={handleCloseNavMenu}
              sx={{ my: 2, color: 'white', display: 'block' }}
            >
              SEARCH
            </Button> */}
            <Button
              onClick={() => { navigate('/search'); handleCloseNavMenu(); }}
              sx={{ ml: 16, my: 2, color: 'white', display: 'block' }}
            >
              SEARCH
            </Button>
            <Button
              onClick={() => { navigate('/genres'); handleCloseNavMenu(); }}
              sx={{ ml: 4, my: 2, color: 'white', display: 'block' }}
            >
              GENRES
            </Button>
            <Button
              onClick={() => { navigate('/forums'); handleCloseNavMenu(); }}
              sx={{ ml: 4, my: 2, color: 'white', display: 'block' }}
            >
              FORUMS
            </Button>
            <Button
              onClick={() => { navigate('/events'); handleCloseNavMenu(); }}
              sx={{ ml: 4, my: 2, color: 'white', display: 'block' }}
            >
              EVENT
            </Button>
          </Box>
          
          {loginStatus === false ?
            <ButtonGroup variant="contained">
              <Button onClick={() => navigate("/login")}>LOGIN</Button>
              <Button onClick={() => navigate("/register")}>REGISTER</Button>
            </ButtonGroup>
            :
            <Box sx={{ flexGrow: 0 }}>
            <Tooltip title="Open settings">
              <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                <AccountCircle />
              </IconButton>
            </Tooltip>
            <Menu
              sx={{ mt: '45px' }}
              id="menu-appbar"
              anchorEl={anchorElUser}
              anchorOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              open={Boolean(anchorElUser)}
              onClose={handleCloseUserMenu}
            >
              <MenuItem onClick={() => { navigate(`/userprofile/${localStorage.getItem("id")}`); setAnchorElUser(null); navigate(0);}}>
                <Typography textAlign="center">Profile</Typography>
              </MenuItem>
              <MenuItem onClick={logout}>
                <Typography textAlign="center">Logout</Typography>
              </MenuItem>
            </Menu>
          </Box>
          }
          
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default NavBar;
