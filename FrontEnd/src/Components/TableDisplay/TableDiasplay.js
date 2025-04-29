import "./TableDispla.css"


import React, { useState, useMemo } from "react";
import { Pencil, Trash, Settings, Filter, X, Plus } from "lucide-react";

const InvoiceTable = ({ columns, rows, addDataComponent = false }) => {
  const [isFilterPopupOpen, setIsFilterPopupOpen] = useState(false);
  const [isSettingsPopupOpen, setIsSettingsPopupOpen] = useState(false);
  const [isAddDataPopupOpen, setIsAddDataPopupOpen] = useState(false);
  const [filterColumn, setFilterColumn] = useState(columns[0]?.key || "");
  const [filterValue, setFilterValue] = useState("");
  const [tempVisibleColumns, setTempVisibleColumns] = useState(
    columns.reduce((acc, col) => ({ ...acc, [col.key]: true }), {})
  );

  const [visibleColumns, setVisibleColumns] = useState(tempVisibleColumns);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: "asc" });

  const handleColumnToggle = (key) => {
    setTempVisibleColumns((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const handleSaveSettings = () => {
    setVisibleColumns(tempVisibleColumns);
    setIsSettingsPopupOpen(false);
  };

  const handleSort = (key) => {
    setSortConfig((prev) => ({
      key,
      direction: prev.key === key && prev.direction === "asc" ? "desc" : "asc"
    }));
  };

  const sortedData = useMemo(() => {
    if (!sortConfig.key) return rows;
    return [...rows].sort((a, b) => {
      if (a[sortConfig.key] < b[sortConfig.key]) return sortConfig.direction === "asc" ? -1 : 1;
      if (a[sortConfig.key] > b[sortConfig.key]) return sortConfig.direction === "asc" ? 1 : -1;
      return 0;
    });
  }, [sortConfig, rows]);

  const filteredData = useMemo(() => {
    return sortedData.filter((row) =>
      row[filterColumn]?.toString().toLowerCase().includes(filterValue.toLowerCase())
    );
  }, [filterColumn, filterValue, sortedData]);

  return (
    <div className=" relative" disabled={true}>
      <div className="flex justify-between mb-2 pr-2">
        <button className="p-2 border rounded bg-black text-white flex items-center" onClick={() => setIsAddDataPopupOpen(!isAddDataPopupOpen)}>
          <Plus className="w-5 h-5 mr-1" /> Add Data
        </button>
        <div className="flex space-x-2">
          <button className="p-2 border rounded" onClick={() => setIsFilterPopupOpen(!isFilterPopupOpen)}>
            <Filter className="w-5 h-5" />
          </button>
          <button className="p-2 border rounded " onClick={() => setIsSettingsPopupOpen(!isSettingsPopupOpen)}>
            <Settings className="w-5 h-5" />
          </button>
        </div>
      </div>

      {isFilterPopupOpen && (
        <div className="absolute right-0 mr-2 bg-white border p-4 shadow-md z-50 w-64 rounded">
          <div className="flex justify-between items-center mb-2">
            <h3 className="text-lg font-semibold">Filter</h3>
            <button onClick={() => setIsFilterPopupOpen(false)}><X className="w-5 h-5" /></button>
          </div>
          <hr/>
          <select className="w-full p-2 border mb-2" value={filterColumn} onChange={(e) => setFilterColumn(e.target.value)}>
            {columns.map(col => <option key={col.key} value={col.key}>{col.label}</option>)}
          </select>
          <input
            type="text"
            className="w-full p-2 border mb-2"
            placeholder="Filter value"
            value={filterValue}
            onChange={(e) => setFilterValue(e.target.value)}
          />
        </div>
      )}

      {isSettingsPopupOpen && (
        <div className="absolute right-0 mr-2 bg-white border p-4 shadow-md z-50 w-48 rounded">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold"> Visibility</h3>
            <button onClick={() => setIsSettingsPopupOpen(false)}><X className="w-5 h-5 " /></button>
          </div>
          <hr/>
          {columns.map(col => (
            <label key={col.key} className="flex items-center space-x-1 mb-1">
              <input
                type="checkbox"
                checked={tempVisibleColumns[col.key]}
                onChange={() => handleColumnToggle(col.key)}
              />
              <span>{col.label}</span>
            </label>
          ))}
          <button className="w-full p-2 bg-black text-white mt-2" onClick={handleSaveSettings}>Save</button>
        </div>
      )}

      {isAddDataPopupOpen && (
        <div className="absolute left-1/2 -translate-x-1/2 top-[10px] bg-white border shadow-md z-50 rounded">
          <div className="flex justify-between items-center p-6 pb-0">
            <h2 className="text-xl font-bold mb-4">Add New Vehicle</h2>
            <button 
            onClick={() => setIsAddDataPopupOpen(false)}
            className=" mb-4"
            >
                <X className="w-5 h-5" />
            </button>
          </div>
          <div className="block m-1">
            <div>
              {addDataComponent ? React.createElement(addDataComponent) : null}
            </div>
          </div>

        </div>
      )}

      <div className="customParentTableClass TableClass relative h-96 overflow-auto border border-gray-300 ">
        <table className="min-w-full border-collapse ">
          <thead className="sticky top-0 bg-black text-white z-10 text-center">
            <tr>
              {columns.map(col => visibleColumns[col.key] && (
                <th key={col.key} className="px-4 py-2 cursor-pointer " onClick={() => handleSort(col.key)}>{col.label}</th>
              ))}
              <th className="px-4 py-2 \">Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredData.map((row, index) => (
              <tr key={index} className="hover:bg-gray-100">
                {columns.map(col => visibleColumns[col.key] && (
                  <td key={col.key} className="px-4 py-2 text-center">{row[col.key]}</td>
                ))}
                <td className="px-4 py-2 flex justify-center space-x-2">
                  <button className="p-1 text-blue-500"><Pencil className="w-4 h-4" /></button>
                  <button className="p-1 text-red-500"><Trash className="w-4 h-4" /></button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
    </div>
  );
};

export default InvoiceTable;