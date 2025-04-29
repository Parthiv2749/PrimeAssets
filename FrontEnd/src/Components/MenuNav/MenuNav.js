// import CustomNavbar from './Nav/Navbar';
import CustomNavbar from '../Nav/Navbar.js';
import Sidebar from '../MenuPanel/Menu.js';
import VehicleRecords from '../../ComponentClassification/PhysicalAsstes/Vehicles/VehicleRecords.js';
import { useState } from "react";
import "./MenuNav.css";

import Dashboad from '../../ComponentClassification/DashBoards/Dashboard.js';
import EditVehicle from '../../Components/EditorComponent/PhysicalAssets/Vehicles/Vehicle.js';
import EditInventory from '../../Components/EditorComponent/PhysicalAssets/Inventory/Inventory.js';
function MenuNav(){
    const [activeComponent, setActiveComponent] = useState("Dashboad");
    
    return(
        <>
            <CustomNavbar/>
            <div className="MainDiv">
                <Sidebar setActiveComponent={setActiveComponent}/>
                <div className="ComponentView">
                   
                    {activeComponent === "Dashboad" && <Dashboad />}
                    {activeComponent === "EditInventory" && <EditInventory/>}
                    {activeComponent === "EditVehicle" && <EditVehicle />}
                </div>  
            </div>
        </>
    );
}

export default MenuNav;