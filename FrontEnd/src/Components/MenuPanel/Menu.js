import { useState } from "react";
import { ChevronDown, LayoutDashboard, FileText, Layers } from "lucide-react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./Menu.css";

function Sidebar ({ setActiveComponent }) {
  const [isDashboardOpen, setIsDashboardOpen] = useState(false);
  const [isPhysicalComponentsOpen, setIsPhysicalComponentsOpen] = useState(false);
    const [isinventoryOpen, setIsInventoryOpen] = useState(false);

  return (
    <div className="sidebar bg-slate-950 text-white p-3 ">

      <nav>
        <button
          className="btn btn-dark w-100 text-start d-flex align-items-center"
          onClick={() => setIsDashboardOpen(!isDashboardOpen)}>
          
          {/* <LayoutDashboard className="me-2 text-xs" /> */}
          <span className="text-[11pt]"> Dashboard</span>
          {/* <ChevronDown className={`ms-auto ${isDashboardOpen ? "rotate-180" : ""}`} /> */}
        </button>
        {isDashboardOpen && (
          <div className="ms-4">
            <a href="#" className="d-block py-2" onClick={() => setActiveComponent("Dashboad")}>Overview</a>
            <a href="#" className="d-block py-2">Analytic</a>
            <a href="#" className="d-block py-2">Saas</a>
          </div>
        )}

        <button
          className="btn btn-dark w-100 text-start d-flex align-items-center mt-2"
          onClick={() => setIsPhysicalComponentsOpen(!isPhysicalComponentsOpen)}
        >
          {/* <Layers className="me-2 text-xs" /> */}
          Physical Assets
          <ChevronDown className={`ms-auto ${isPhysicalComponentsOpen ? "rotate-180" : ""}`} />
        </button>
        {isPhysicalComponentsOpen && (
          <div className="ms-3">
            <a href="#" className="d-block py-1" onClick={() => {setActiveComponent("EditVehicle");
           setIsInventoryOpen(!isinventoryOpen);
            }}>🚗Vehicles</a>

          {isinventoryOpen && (
            <div className="ms-4">
              <a href="#" className="d-block py-1">Fuel Consumption</a>
            </div>
          )} 
            <a href="#" className="d-block py-1" onClick={() => setActiveComponent("EditInventory")}>🏪Inventory</a>
          </div>
        )}



        

        <a href="#" className="btn btn-dark w-100 text-start d-flex align-items-center mt-2">
          <FileText className="me-2 text-xs" />
          Installation
        </a>
      </nav>
    </div>
  );
};

export default Sidebar;
