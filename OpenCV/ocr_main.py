import cv2
import pytesseract

image_path = './data/uctenka.png'
# Jak pomocí OpenCV otevřeš obrázek?
image = cv2.imread(image_path)

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
preprocessed_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

# Kód pro čtení z obrázku dej sem:
extracted_text = pytesseract.image_to_string(preprocessed_image)

# Print the extracted text
print(extracted_text)