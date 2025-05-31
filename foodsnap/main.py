import requests

def get_nutrition(food_name, api_key):
    url = f"https://api.spoonacular.com/recipes/guessNutrition?title={food_name}&apiKey={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Estimated Calories: {data['calories']['value']} kcal")
        print(f"Fat: {data['fat']['value']} g")
        print(f"Carbs: {data['carbs']['value']} g")
        print(f"Protein: {data['protein']['value']} g")
    else:
        print("Error fetching data:", response.status_code, response.text)

if __name__ == "__main__":
    food = input("Enter the food item: ")
    api_key = "2c303386a88c42af8870115216f3c85c"  # Replace with your Spoonacular API key
    get_nutrition(food, api_key)
