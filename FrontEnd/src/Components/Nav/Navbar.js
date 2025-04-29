// // src/Navbar.js
import React, {useContext} from 'react';
import { Navbar,  Dropdown } from 'react-bootstrap';
// import { FaUserCircle } from 'react-icons/fa'; // You can use react-icons for the user icon

import './Navbar.css'; // Import custom CSS
import logo from '../../Resource/images/logo.svg';
import Profile from '../../Resource/images/profile.png';
import AuthContext from '../ApiService/api.js';
import { useNavigate } from 'react-router-dom';


function CustomNavbar() {

  // const [showDropdown, setShowDropdown] = useState(false);

  // // Toggle dropdown visibility
  // const toggleDropdown = () => setShowDropdown(!showDropdown);
  const { logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogOut = async (e) => {
    e.preventDefault();
    try {
      await logout();
      navigate("/"); // or wherever you need to redirect
    } catch (error) {
      console.error("LogOut failed:", error.response || error);
      // setErrorMessage("LogOut failed. Please try again.");
    }
  };

  return (
    <Navbar className='navbar nav-custom bg-black'>
      <Navbar.Brand href="/">
        <img
          alt="Logo"
          src={logo}
          width="60"
          height="60"
          className="d-inline-block align-top"
        />
        
      </Navbar.Brand>

      <nav className='login'>
        <Dropdown drop="down" align="end">
        {/* Dropdown Toggle with custom class to remove the arrow and fit to icon */}
        <Dropdown.Toggle
          variant="link"
          id="dropdown-basic"
          className="exact-fit no-arrow"
        >
         <img
          alt="Logo"
          src={Profile}
          width="30"
          height="30"
          className="remove-back"
          />
        </Dropdown.Toggle>

        <Dropdown.Menu>
          <Dropdown.Item href="#profile">Profile</Dropdown.Item>
          <Dropdown.Item href="#settings">Settings</Dropdown.Item>
          <Dropdown.Divider />
          <Dropdown.Item onClick={handleLogOut}>Log out</Dropdown.Item>
        </Dropdown.Menu>
      </Dropdown>
      </nav>

    </Navbar>
  );
};

export default CustomNavbar;



