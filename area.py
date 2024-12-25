import cv2
import numpy as np
import os
from colorama import Fore, Style, init
import csv

# Initialize colorama
init(autoreset=True)

def calculate_area(image):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and improve thresholding
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Threshold the image to isolate the subject from the black background
    _, binary_image = cv2.threshold(blurred_image, 50, 255, cv2.THRESH_BINARY)

    # Find contours from the binary image
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the largest contour (assuming the subject is the largest object)
        largest_contour = max(contours, key=cv2.contourArea)

        # Create a mask for the largest contour
        mask = np.zeros_like(gray_image)
        cv2.drawContours(mask, [largest_contour], -1, 255, thickness=-1)

        # Count non-zero pixels in the mask to calculate the area of the subject
        total_pixels = cv2.countNonZero(mask)
        return total_pixels
    else:
        return 0

def save_results(file_name, area):
    # Ensure the 'result' directory exists
    os.makedirs("./result", exist_ok=True)

    # Path to the results CSV file
    results_path = "./result/area.csv"

    # Check if the CSV file exists, and if not, create it with the header
    file_exists = os.path.exists(results_path)
    with open(results_path, mode="a", newline='') as file:
        writer = csv.writer(file)

        # Write header only if the file is new (does not exist)
        if not file_exists:
            writer.writerow(["File Name", "Area"])

        # Write the results for the current file
        writer.writerow([file_name, area])

    print(Fore.GREEN + f"Results for {file_name} have been saved to area.csv" + Style.RESET_ALL)

def program():
    # Loop through all the files in the data/analysis folder
    print(Fore.CYAN + "=== Area Calculation Program ===")
    print(Fore.CYAN + "Processing all files in ./data/area")
    for file in os.listdir("./data/area"):
        if file.endswith(".jpg"):
            print(Fore.YELLOW + f"Processing file: {file}...")
            image = cv2.imread(f"./data/area/{file}")
            area = calculate_area(image)
            if area > 0:
                print(Fore.GREEN + f"Area for {file}: {area}")
                save_results(file, area)
            else:
                print(Fore.RED + f"No black outline found in {file}")
                save_results(file, "Error")
            print(Fore.CYAN + "========================")
    print(Fore.CYAN + "=== Processing Completed ===")

if __name__ == "__main__":
    program()
