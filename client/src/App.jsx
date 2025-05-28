import React, { useState } from 'react';
import axios from 'axios';
import SpiralLoader from './SpiralLoader';

const App = () => {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading,setLoading] = useState(false);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setPreview(URL.createObjectURL(file)); // Show preview
  };

    const handleUpload = async () => {
    const formData = new FormData();
    formData.append('image', image);
      setLoading(true)
    try {
      const res = await axios.post('http://localhost:5000/upload', formData);
      setResult(res.data);
      setError("");
    } catch (err) {
      console.error("Upload failed:", err.message);
      setError("Upload failed: " + (err.response?.data?.error || err.message));
    }
    setLoading(false)
  };

  return (
    <div className="min-h-screen bg-gradient-to-r from-green-100 to-green-200 p-8">
      <div className="max-w-md mx-auto bg-white rounded-xl shadow-md p-6 space-y-4">
        <h1 className="text-2xl font-bold text-green-800">🍔 FoodSnap AI</h1>

        <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-green-400 rounded-lg cursor-pointer bg-green-50 hover:bg-green-100">
          <span className="text-green-700 font-medium">📁 Choose an image</span>
          <input
            type="file"
            accept="image/*"
            className="hidden"
            onChange={handleFileChange}
          />
        </label>

        {preview && (
          <div className="text-center">
            <p className="text-sm text-gray-600 mt-2">{image?.name}</p>
            <img src={preview} alt="Preview" className="mt-3 w-full h-50 object-contain mx-auto rounded shadow" />
          </div>
        )}

        <button
          className={`w-full px-4 py-2 text-white rounded ${image ? 'bg-green-600 hover:bg-green-700' : 'bg-gray-400 cursor-not-allowed'}`}
          onClick={handleUpload}
          disabled={!image}
        >
          🚀 Upload & Analyze
        </button>
        {loading  && 
        <div className=' flex justify-center'>
            <SpiralLoader/>
        </div>
        }

        {error && <p className="text-red-500 font-semibold">{error}</p>}

        {result && (
          <div className="pt-4">
            <h2 className="text-xl font-semibold text-green-700">{result.food}</h2>
            <ul className="mt-2 space-y-1 text-gray-700">
              <li>🔥 Calories: {result.calories}</li>
              <li>💪 Protein: {result.protein}g</li>
              <li>🍞 Carbs: {result.carbs}g</li>
              <li>🧈 Fat: {result.fat}g</li>
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
