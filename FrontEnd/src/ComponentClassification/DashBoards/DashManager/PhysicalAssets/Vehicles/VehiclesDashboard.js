import {React, useState, useEffect} from "react";
import axios from 'axios';

import {
  LineChart,
  BarChart,
  Bar,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  Line,
  ResponsiveContainer,
} from "recharts";

async function getfuelOnModelData( fetchfrom ) {
  try {

    const response = await axios.get(fetchfrom, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    });

    let data = response.data;
    if (typeof data === 'string') {
      data = JSON.parse(data);
    }

    // console.log("Fetched API data:", data);
    return data;
  } catch (error) {
    console.error("Failed to fetch inventory:", error);
    return null;
  }
}

const chartData = [
  { month: "January", desktop: 186, mobile: 80 },
  { month: "February", desktop: 305, mobile: 200 },
  { month: "March", desktop: 237, mobile: 120 },
  { month: "April", desktop: 73, mobile: 190 },
  { month: "May", desktop: 209, mobile: 130 },
  { month: "June", desktop: 214, mobile: 140 },
];

const chartConfig = {
  desktop: {
    label: "Desktop",
    color: "#2563eb",
  },
  mobile: {
    label: "Mobile",
    color: "#60a5fa",
  },
};

const colors = ["#8884d8", "#82ca9d", "#ffc658"];

export function VehiclesDashboard() {
  // const [data, setData] = useState([]);
  const [fuelOnModeldata, setFuelOnModel] = useState([])

  const [fuelconsumptionOverTime, getFuelconsumptionOverTime] = useState([])
  const [groupedfuelconsumptionOverTime, getGroupedFuelconsumptionOverTime] = useState([])
  

  useEffect(() => {
    async function fetchData(fetchLink) {
      const result = await getfuelOnModelData(fetchLink);
      if (!result || !result.data) return;

      const chartData = result.data.map(([vehicle_id, total_fuel]) => ({
        vehicle_id,
        total_fuel,
      }));
      
      setFuelOnModel(chartData);
    }

    fetchData("http://192.168.83.1:8000/fuelOnModel");

    async function fuelConsumpation(fetchLink) {
      const result = await getfuelOnModelData(fetchLink);
      if (!result || !result.data) return;

      const chartData = result.data.map(([vehicle_id, fuel_date, fuel_amount]) => ({
        vehicle_id,
        fuel_date,
        fuel_amount,
      }));

      const groupedData = chartData.reduce((acc, { vehicle_id, fuel_date, fuel_amount }) => {
        let record = acc.find(entry => entry.fuel_date === fuel_date);
        if (!record) {
          record = { fuel_date };
          acc.push(record);
        }
        record[`vehicle_${vehicle_id}`] = fuel_amount;
        return acc;
      }, []);
      
      getFuelconsumptionOverTime(chartData);
      getGroupedFuelconsumptionOverTime(groupedData);
      // console.log(chartData);
    }

    fuelConsumpation("http://192.168.83.1:8000/fuelconsumptionOverTime")

  }, []);


  return (
    <div className='grid grid-cols-2 gap-2 m-2'>

        <div className="p-4 bg-white shadow-lg rounded-xl">
          <h2 className="text-xl font-bold mb-4">Fuel Consumption Per Vehicle</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={fuelOnModeldata} margin={{ top: 10, right: 30, left: 10, bottom: 5 }}>
            <CartesianGrid vertical={false} stroke="#ccc" />
              <XAxis dataKey="vehicle_id" label={{ value: "Vehicle ID", position: "insideBottom", dy: 10 }} />
              <YAxis label={{ value: "Fuel (Liters)", angle: -90, position: "insideLeft" }} />
              <Tooltip />
              <Bar dataKey="total_fuel" fill="#82ca9d" barSize={50} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div  className="block bg-white border border-gray-500 rounded-lg shadow-sm hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700">
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={groupedfuelconsumptionOverTime}>
            <CartesianGrid vertical={false} stroke="#ccc" />
              <XAxis dataKey="fuel_date" />
              <YAxis />
              <Tooltip />
              <Legend />
              {Array.from(new Set(fuelconsumptionOverTime.map(d => d.vehicle_id))).map((id, index) => (
                <Line
                  key={id}
                  type="monotone"
                  dataKey={`vehicle_${id}`}
                  stroke={colors[index % colors.length]}
                  name={`Vehicle ${id}`}
                />
              ))}
            </LineChart>
         </ResponsiveContainer>
        </div>


    </div>
  );
}

export default VehiclesDashboard;
