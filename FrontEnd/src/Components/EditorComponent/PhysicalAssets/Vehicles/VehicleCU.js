import { useState } from "react";
import axios from "axios";

function VehicleCU() {
  const [formData, setFormData] = useState({
    VehicleRegNo: "",
    Make: "",
    Model: "",
    VehicleType: "",
    FuelType: "",
    Mileage: "",
    EngineCapacity: "",
    Status: "",
    CategoryID: 1,
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };


  async function addvehicle( e) {
    e.preventDefault();

    console.log(formData);
    try {
      const response = await axios.post("http://192.168.83.1:8000/addvehicle", formData, {
        headers: { 
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          "Content-Type": "application/json"
        }

      });
      
      console.log("Response:", response.data);

    } catch (error) {
      console.error("Error submitting form:", error);

    }

  }

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <form onSubmit={addvehicle} className="grid grid-cols-2 gap-4">
        {/* Vehicle No */}
        <div className="col-span-2">
          <input
            type="text"
            name="VehicleRegNo"
            value={formData.VehicleRegNo}
            onChange={handleChange}
            className="w-full p-2 border rounded"
            placeholder="Vehicle No"
          />
        </div>

        {/* Make & Model (Same Row) */}
        <div>
          <select
            name="Make"
            value={formData.Make}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          >
            <option value="">Select Make</option>
            <option value="Toyota">Toyota</option>
            <option value="Honda">Honda</option>
            <option value="Ford">Ford</option>
          </select>
        </div>

        <div>
          <select
            name="Model"
            value={formData.Model}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          >
            <option value="">Select Model</option>
            <option value="Corolla">Corolla</option>
            <option value="CR-V">CR-V</option>
            <option value="F-150">F-150</option>
          </select>
        </div>

        {/* Vehicle Type */}
        <div>
          <select
            name="VehicleType"
            value={formData.VehicleType}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          >
            <option value="">Select Type</option>
            <option value="Sedan">Sedan</option>
            <option value="SUV">SUV</option>
            <option value="Truck">Truck</option>
          </select>
        </div>

        {/* Fuel Type */}
        <div>
          <select
            name="FuelType"
            value={formData.FuelType}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          >
            <option value="">Select Fuel Type</option>
            <option value="Petrol">Petrol</option>
            <option value="Diesel">Diesel</option>
            <option value="Electric">Electric</option>
          </select>
        </div>

        {/* Mileage */}
        <div>
          <input
            type="number"
            name="Mileage"
            value={formData.Mileage}
            onChange={handleChange}
            className="w-full p-2 border rounded"
            placeholder="Mileage"
          />
        </div>

        {/* Engine Capacity */}
        <div>
          <input
            type="number"
            step="0.1"
            name="EngineCapacity"
            value={formData.EngineCapacity}
            onChange={handleChange}
            className="w-full p-2 border rounded"
            placeholder="Engine Capacity"
          />
        </div>

        {/* Status */}
        <div className="col-span-2">
          <select
            name="Status"
            value={formData.Status}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          >
            <option value="">Select Status</option>
            <option value="Active">Active</option>
            <option value="Inactive">Inactive</option>
            <option value="Under Maintenance">Under Maintenance</option>
          </select>
        </div>

        {/* Submit Button */}
        <div className="col-span-2">
          <button
            type="submit"
            className="w-full bg-black text-white p-2 rounded"
          >
            Submit
          </button>
        </div>
      </form>
    </div>
  );
};

export default VehicleCU;