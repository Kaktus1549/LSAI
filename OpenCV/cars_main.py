import cv2
import numpy as np
import matplotlib.pyplot as plt
# Google jupyter patch for opencv -> just for google colab
# from google.colab.patches import cv2_imshow

image = cv2.imread('./data/cars.jpg')

# Load the uploaded car classifier
car_cascade_path = './data/cars.xml'
# Setup cascade:
car_cascade = cv2.CascadeClassifier(car_cascade_path)
# Check if the cascade file is loaded properly
if car_cascade.empty():
    raise IOError('Failed to load cascade classifier')

# Convert the image to grayscale:
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect cars in the image
cars = car_cascade.detectMultiScale(gray, 1.1, 1)

# Draw rectangles around detected cars
for (x, y, w, h) in cars:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

# Display the image with detected cars
cv2.imshow('Cars', image)

# Print the number of cars detected
print(f'Number of cars detected: {len(cars)}')