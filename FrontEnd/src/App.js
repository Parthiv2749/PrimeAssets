// import logo from './logo.svg';
// import './App.css';
import Login from './Pages/Login/Login.js';

// import MenuNav from './Components/MenuNav/MenuNav';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from './Components/ApiService/api.js';
import ProtectedRoute from './Components/ProtectedRoutes/ProtectedRoutes.js';
import PrimeAsstes from './Pages/MainPage/MainPage.js';
function App() {
  return (
    <AuthProvider>

      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />}/>

          <Route element={<ProtectedRoute />}>
           
            <Route path="PrimeAsstes" element={<PrimeAsstes />} />
            {/* Other protected routes can go here */}
          </Route>
        </Routes>
      </BrowserRouter>

    </AuthProvider>
  //   <div className="flex items-center justify-center h-screen bg-blue-500 text-white text-3xl">
  //   Tailwind is working!
  // </div>
//  
//     <div className="App">
//       <Login/>

//     </div> 

   
  );
}

export default App;
