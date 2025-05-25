"use client";
import { useState, useEffect } from "react";
import ClickableMap from "./components/ClickableMap";

export default function Home() {
  const nivelesSocioeconomicos = ["AB","B","BC", "C", "CD", "D"];
  const tiposEntorno = ["BASE", "HOGAR", "PEATONAL", "RECESO"]
  const [lat, setLat] = useState("");
  const [lng, setLng] = useState("");
  const [profilability, setProfilability] = useState("");
  const [entorno, setEntorno] = useState(tiposEntorno[0]);
  const [nivelSocioeconomico, setNivelSocioeconomico] = useState(nivelesSocioeconomicos[0]);


  const handleLatChange = (event) => {
    // Validate latitude input
    const value = event.target.value;
    if (value && (isNaN(value))) {
      alert("Please enter a valid latitude value.");
      return;
    }
    setLat(event.target.value);
  }
  const handleLngChange = (event) => {
    // Validate longitude input
    const value = event.target.value;
    if (value && (isNaN(value))) {
      alert("Please enter a valid longitude value.");
      return;
    }
    setLng(event.target.value);
  }

  const handleEntornoChange = (event) => {
    setEntorno(event.target.value);
  }

  const handleNivelSocioeconomicoChange = (event) => {
    setNivelSocioeconomico(event.target.value);
  }

  const handleButtonClick = async () => {
    // Validate inputs before making the request
    if (!lat || !lng) {
      alert("Please enter both latitude and longitude.");
      return;
    }
    if (isNaN(lat) || isNaN(lng)) {
      alert("Latitude and longitude must be numbers.");
      return;
    }
    if (!entorno) {
      alert("Please select un entorno.");
      return;
    }
    if (!nivelSocioeconomico) {
      alert("Please select a socio-economic level.");
      return;
    }


    const res = await fetch("http://localhost:8000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        lat: Number(lat),
        lng: Number(lng),
        entorno,
        nivelSocioeconomico 
       }),
    })

    const data = await res.json();
    console.log(data);

    if (res.ok) {
      setProfilability(data.profitability  === true ? "Yes" : "No");
      }
    else {
      alert("Error: " + data.error);
    }
  }

  useEffect(() => {
    // set entorno to the first option on initial render
    // if (houseCategories.length > 0) {
    //   setEntorno(houseCategories[0]);
    // }
  }
  , [houseCategories]);

  const handleMapCoordinatesUpdate = (newCoords) => {
    setLat(newCoords.lat.toString()); // Update lat state in page.js
    setLng(newCoords.lng.toString()); // Update lng state in page.js
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="text-2xl font-bold">
        <h1>onde quieres la sucursal pá</h1>
        {/* Horizontal input fields */}
        <div className="flex flex-row gap-6 mt-8 mb-4">
          <div className="flex flex-col gap-2">
            <label htmlFor="lat">Latitude</label>
            <input
              type="text"
              id="lat"
              value={lat}
              onChange={handleLatChange}
              className="border border-gray-300 rounded p-2"
            />
          </div>
          <div className="flex flex-col gap-2">
            <label htmlFor="lng">Longitude</label>
            <input
              type="text"
              id="lng"
              value={lng}
              onChange={handleLngChange}
              className="border border-gray-300 rounded p-2"
            />
          </div>
        {/* divider horizonal line */}
        </div>
        <div className="border-t border-gray-300 my-4 w-full"></div>
          <div className="flex flex-col gap-2">
            <label htmlFor="entorno">Entorno</label>
            <select
              id="entorno"
              value={entorno}
              onChange={(e) => handleEntornoChange(e)}
              className="border border-gray-300 rounded p-2"
            >
              {houseCategories.map((entorno) => (
                <option key={entorno} value={entorno}>
                  {entorno}
                </option>
              ))}
            </select>
          </div>
          <div className="flex flex-col gap-2">
            <label htmlFor="nivelSocioeconomico">Nivel Socioeconomico</label>
            <select
              id="nivelSocioeconomico"
              value={nivelSocioeconomico}
              onChange={(e) => handleNivelSocioeconomicoChange(e)}
              className="border border-gray-300 rounded p-2"
            >
              {nivelesSocioeconomicos.map((nivel) => (
                <option key={nivel} value={nivel}>
                  {nivel}
                </option>
              ))}
            </select>
          </div>
          <button
            onClick={handleButtonClick}
            className="bg-blue-500 text-white rounded p-2 h-12 self-end hover:bg-blue-600 transition duration-200 mt-4"
          >
            Predict
          </button>
        <div className="text-xxl font-bold mt-8">
          {profilability && <p>Rentable?: <span className={profilability === "Yes" ? "text-green-500" : "text-red-500"}>{profilability}</span></p>}
        </div>
        <div className="mt-8">
          <h2 className="text-xl font-bold mb-4">Map</h2>
          <ClickableMap onCoordinatesChange={handleMapCoordinatesUpdate} />
        </div>
      </div>
    </div>
  );
}