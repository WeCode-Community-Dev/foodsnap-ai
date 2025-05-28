// server.js

require('dotenv').config();
const express = require('express');
const multer = require('multer');
const cors = require('cors');
const axios = require('axios');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());
app.use('/uploads', express.static('uploads'));

// Multer configuration
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, 'uploads/'),
  filename:   (req, file, cb) => cb(null, Date.now() + '-' + file.originalname)
});
const upload = multer({ storage });

// POST /upload
app.post('/upload', upload.single('image'), async (req, res) => {
  try {
    // 1. Classify image via Flask
    const imagePath = path.join(__dirname, req.file.path);
    console.log('📸 Uploaded:', imagePath);

    const flaskRes = await axios.post('http://localhost:5001/predict', {
      imagePath
    });
    const food = flaskRes.data.food;
    console.log('🍽️ Predicted:', food);

    // 2. Fetch nutrition from Spoonacular
    const SPOON_KEY = process.env.API_KEY;
    const spoonURL = `https://api.spoonacular.com/recipes/guessNutrition?title=${encodeURIComponent(food)}&apiKey=${SPOON_KEY}`;
    console.log('🌐 Spoonacular URL:', spoonURL);

    const spoonRes = await axios.get(spoonURL);
    const data = spoonRes.data;

    // 3. Build result (fallbacks if missing)
    const result = {
      food,
      calories: (data.calories?.value ?? 0).toFixed(1),
      protein:  (data.protein?.value  ?? 0).toFixed(1),
      carbs:    (data.carbs?.value    ?? 0).toFixed(1),
      fat:      (data.fat?.value      ?? 0).toFixed(1),
    };

    return res.json(result);

  } catch (err) {
    console.error('❌ Processing error:', err.message);
    if (err.response) {
      console.error('🔴 API error:', err.response.status, err.response.data);
    }
    return res.status(500).json({ error: 'Processing failed' });
  }
});

app.listen(PORT, () => {
  console.log(`🚀 Node server listening on http://localhost:${PORT}`);
});
