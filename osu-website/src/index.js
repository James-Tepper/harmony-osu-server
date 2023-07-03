import "./index.css";
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from "./components/Navbar"



const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <Router>
    {/* <Provider store={store}> */}
    <Routes>
      <Route path="/" element={<App />} />
    </Routes>
    {/* </Provider> */}
  </Router>
);
