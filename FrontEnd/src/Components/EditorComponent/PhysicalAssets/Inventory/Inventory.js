import React, { useState, useEffect } from 'react';
import InvoiceTable from '../../../TableDisplay/TableDiasplay.js';
import axios from 'axios';

async function getInventoryData() {
  try {
    const response = await axios.get("http://192.168.83.1:8000/inventory", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    });
    let data = response.data;
    if (typeof data === 'string') {
      data = JSON.parse(data);
    }
    console.log("Fetched API data:", data);
    return data;
  } catch (error) {
    console.error("Failed to fetch inventory:", error);
    return null;
  }
}

function EditInventory() {
  const [columns, setColumns] = useState([]);
  const [rows, setRows] = useState([]);

  useEffect(() => {
    async function fetchData() {
      const result = await getInventoryData();
      if (!result || !result.column || !result.data) return;
      
      const productColumns = result.column.map(label => {
        const key = label
          .toLowerCase()
          .split(' ')
          .map((word, index) =>
            index === 0 ? word : word.charAt(0).toUpperCase() + word.slice(1)
          )
          .join('');
        return { key, label };
      });
      
      const dataRows = result.data.map(row => {
        const obj = {};
        productColumns.forEach((col, index) => {
          obj[col.key] = row[index];
        });
        return obj;
      });
      
      console.log("Mapped columns:", productColumns);
      console.log("Mapped rows:", dataRows);
      
      setColumns(productColumns);
      setRows(dataRows);
    }
    fetchData();
  }, []);

  return (
    <div className="pt-2 pl-2">
      <InvoiceTable 
        key={JSON.stringify(columns) + JSON.stringify(rows)}
        columns={columns} 
        rows={rows} 
      />
    </div>
  );
}

export default EditInventory;
