const express = require('express');
const multer = require('multer');
const cors = require('cors');
const axios = require('axios');

const app = express();
app.use(cors());
app.use(express.json());

const upload = multer({ dest: 'uploads/' });

// Fake image processor (Replace with actual ML/API logic)
const identifyFoodFromImage = async (filePath) => {
  // For demo, return dummy result
  return 'banana';
};

// Fake nutrition API (Replace with real API like Edamam or USDA)
const getNutritionValues = async (food, weight) => {
  // For demo, return fixed values
  return {
    food,
    weight,
    calories: 89 * (weight / 100),
    protein: 1.1 * (weight / 100),
    fat: 0.3 * (weight / 100),
    carbs: 22.8 * (weight / 100),
  };
};

// 🥗 Endpoint 1: Process image and identify food
app.post('/process-image', upload.single('image'), async (req, res) => {
  try {
    const foodName = await identifyFoodFromImage(req.file.path);
    res.json({ food: foodName });
  } catch (error) {
    res.status(500).json({ error: 'Failed to process image' });
  }
});

// 🍽️ Endpoint 2: Get nutrition values
app.post('/get-nutrition', async (req, res) => {
  const { food, weight } = req.body;
  if (!food || !weight) {
    return res.status(400).json({ error: 'Missing food or weight' });
  }

  try {
    const data = await getNutritionValues(food, weight);
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to get nutrition info' });
  }
});

app.listen(3000, () => console.log('Server running on http://localhost:3000'));
