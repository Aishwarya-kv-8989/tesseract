import streamlit as st
from PIL import Image
import numpy as np
import pytesseract
from decimal import Decimal
import pandas as pd

# Load the food calorie database
def load_food_database():
    # You can expand this database or load from a CSV file
    return {
        'apple': 52,
        'banana': 89,
        'orange': 47,
        'chicken breast': 165,
        'rice': 130,
        'bread': 265,
        'egg': 155,
        'milk': 42,
        'potato': 77,
        'tomato': 22,
    }

def calculate_calories(food_items, portions):
    total_calories = 0
    breakdown = []
    food_db = load_food_database()
    
    for food, portion in zip(food_items, portions):
        if food.lower() in food_db:
            calories = food_db[food.lower()] * float(portion)
            total_calories += calories
            breakdown.append({
                'Food': food,
                'Portion': portion,
                'Calories': calories
            })
    
    return total_calories, breakdown

def scan_food_image(image):
    # Convert the image to text using OCR
    try:
        text = pytesseract.image_to_string(image)
        # Process the text to identify food items
        food_db = load_food_database()
        found_items = []
        
        for food in food_db.keys():
            if food.lower() in text.lower():
                found_items.append(food)
        
        return found_items
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return []

def main():
    st.title("🍎 Food Calorie Calculator")
    
    # Create tabs for different functionalities
    tab1, tab2 = st.tabs(["Manual Calculator", "Image Scanner"])
    
    with tab1:
        st.header("Manual Calorie Calculator")
        
        # Dynamic food item input
        num_items = st.number_input("Number of food items", min_value=1, max_value=10, value=1)
        
        food_items = []
        portions = []
        
        for i in range(int(num_items)):
            col1, col2 = st.columns(2)
            with col1:
                food = st.text_input(f"Food item {i+1}", key=f"food_{i}")
                food_items.append(food)
            with col2:
                portion = st.number_input(f"Portion (in units) {i+1}", 
                                        min_value=0.0, 
                                        max_value=10.0, 
                                        value=1.0,
                                        step=0.1,
                                        key=f"portion_{i}")
                portions.append(portion)
        
        if st.button("Calculate Calories"):
            if all(food_items):
                total_calories, breakdown = calculate_calories(food_items, portions)
                
                # Display results
                st.subheader("Results")
                df = pd.DataFrame(breakdown)
                st.dataframe(df)
                
                st.success(f"Total Calories: {total_calories:.1f}")
            else:
                st.warning("Please enter all food items")
    
    with tab2:
        st.header("Food Image Scanner")
        st.write("Upload an image of your food or nutrition label")
        
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            if st.button("Scan Image"):
                with st.spinner("Processing image..."):
                    found_items = scan_food_image(image)
                    
                    if found_items:
                        st.success("Found the following food items:")
                        for item in found_items:
                            st.write(f"- {item} ({load_food_database()[item]} calories per unit)")
                    else:
                        st.warning("No recognized food items found in the image")

if __name__ == "__main__":
    main()
