from flask import Flask, request, jsonify
import math

# Initialize Flask app
app = Flask(__name__)

# Step 1: Define the stock information for each center
centers = {
    "C1": {"A": 3, "B": 2, "C": 8},
    "C2": {"D": 12, "E": 25, "F": 15},
    "C3": {"G": 0.5, "H": 1, "I": 2}
}

# Step 2: Define the distances between centers and L1
distances = {
    "C1": 10,  # Distance from C1 to L1
    "C2": 8,   # Distance from C2 to L1
    "C3": 12   # Distance from C3 to L1
}

# Step 3: Function to calculate the delivery cost
def calculate_cost(order):
    total_weight = 0
    available_centers = []

    # Validate input JSON
    valid_products = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    for product in order.keys():
        if product not in valid_products:
            return float('inf'), None, "Invalid product in order"

    # Calculate total weight and find available centers
    for product, quantity in order.items():
        for center, products in centers.items():
            if product in products:
                total_weight += products[product] * quantity
                if center not in available_centers:
                    available_centers.append(center)
                break  # Stop searching once product is found

    # If no valid product found, return infinity
    if total_weight == 0:
        return float('inf'), None, "No products found in any center"

    # Determine cost per unit distance
    if total_weight <= 5:
        cost_per_unit_distance = 10
    else:
        additional_weight = total_weight - 5
        additional_units = math.ceil(additional_weight / 5)  # Simplified
        cost_per_unit_distance = 10 + additional_units * 8

    # Calculate the minimum delivery cost from available centers
    min_cost = float('inf')
    best_center = None

    for center in available_centers:
        if center in distances:
            total_cost = distances[center] * cost_per_unit_distance
            if total_cost < min_cost:
                min_cost = total_cost
                best_center = center  # Track the best center

    return min_cost, best_center, None

# Step 4: Create a home route to check if Flask is running
@app.route('/')
def home():
    return "Flask is running!"

# Step 5: Create the REST API endpoint
@app.route('/calculate_cost', methods=['POST'])
def calculate_delivery_cost():
    order = request.json
    min_cost, best_center, error_message = calculate_cost(order)

    if error_message:
        return jsonify({"error": error_message}), 400

    return jsonify({"minimum_cost": min_cost, "route": best_center})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)