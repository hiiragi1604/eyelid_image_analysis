import cv2
import numpy as np
import csv
import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def calculate_white_stripes(image, threshold_level=None):
    height, width, _ = image.shape  # Extract dimensions
    total_pixels = height * width

    # Convert to HSV color space to isolate the black outline
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the black color range (HSV)
    lower_black = np.array([0, 0, 0])  # Lower bound for black (H=0, S=0, V=0)
    upper_black = np.array([180, 255, 50])  # Upper bound for black 

    # Create a mask for black color
    black_mask = cv2.inRange(hsv_image, lower_black, upper_black)

    contours, _ = cv2.findContours(black_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the largest contour bounded by the black outline
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Create a mask for the largest contour to isolate the eyelid region
        contour_mask = np.zeros_like(black_mask)
        cv2.drawContours(contour_mask, [largest_contour], -1, 255, thickness=-1)

        # Apply the mask to the grayscale image and extract the ROI
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        masked_image = cv2.bitwise_and(gray_image, gray_image, mask=contour_mask)
        x, y, w, h = cv2.boundingRect(largest_contour)
        roi = masked_image[y:y+h, x:x+w]

        # Apply CLAHE to enhance contrast in the cropped ROI
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced_roi = clahe.apply(roi)

        # Find the brightest pixel in the enhanced ROI
        brightest_pixel = np.max(enhanced_roi)
        print(Fore.YELLOW + f"Brightest pixel intensity: {brightest_pixel}")

        if threshold_level is None:
            # Calculate mean and standard deviation of pixel intensities in the enhanced ROI
            mean_intensity = np.mean(enhanced_roi)
            std_intensity = np.std(enhanced_roi)

            # Dynamically calculate the threshold level as a function of standard deviation
            threshold_level = int(std_intensity * 1)  # Adjust multiplier as needed (e.g., 0.8)
            manual_threshold = brightest_pixel - threshold_level
            print(Fore.YELLOW + f"Mean intensity: {mean_intensity}, Standard deviation: {std_intensity}")
            print(Fore.YELLOW + f"Dynamic threshold level: {threshold_level}")
            print(Fore.YELLOW + f"Dynamic manual threshold intensity: {manual_threshold}")
        else:
            manual_threshold = brightest_pixel - threshold_level

        # Apply binary thresholding using the adjustable level
        _, thresholded_roi = cv2.threshold(enhanced_roi, manual_threshold, 255, cv2.THRESH_BINARY)

        # Display results
        cv2.imshow("Original ROI", roi)
        cv2.imshow("Black Mask", black_mask)
        cv2.imshow("Enhanced ROI", enhanced_roi)
        cv2.imshow("Manual Thresholding", thresholded_roi)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Count white pixels representing the stripes
        white_pixel_count = np.sum(thresholded_roi == 255)
        print(f"The number of pixels representing the white stripes in the cropped eyelid ROI is: {white_pixel_count}/{total_pixels}")
        return white_pixel_count, total_pixels
    else:
        print(Fore.RED + "No black outline was detected in the image.")
        return 0, total_pixels

def save_results(file_name, white_pixel_count, total_pixels):
    # Ensure the 'result' directory exists
    os.makedirs("./result", exist_ok=True)

    # Path to the results CSV file
    results_path = "./result/analysis.csv"

    # Check if the CSV file exists, and if not, create it with the header
    file_exists = os.path.exists(results_path)
    with open(results_path, mode="a", newline='') as file:
        writer = csv.writer(file)
        
        # Write header only if the file is new (does not exist)
        if not file_exists:
            writer.writerow(["File Name", "White Pixel Count", "Total Pixels"])

        # Write the results for the current file
        writer.writerow([file_name, white_pixel_count, total_pixels])

    print(Fore.GREEN + f"Results for {file_name}.jpg have been saved to results.csv")

def program():
    fileName = None
    while True:
        if fileName is None:
            print(Fore.GREEN + "=== File Processing Program ===")
            fileName = input(Fore.GREEN + "Enter the file name (or type 'exit' to quit): ")
            if fileName.lower() == 'exit':
                print(Fore.YELLOW + "Exiting the program. Goodbye!")
                break

        print(Fore.GREEN + f"Processing {fileName}.jpg")
        # Load the image
        image_path = f"./data/analysis/{fileName}.jpg"
        image = cv2.imread(image_path)

        if image is None:
            print(Fore.RED + f"Error: Image {fileName}.jpg not found.")
            fileName = None
            continue

        manual_mode = input(Fore.CYAN + "Enter 'm' to manually set the threshold level, or any other key to use the default threshold level: ")
        if manual_mode.lower() == 'm':
            print(Fore.CYAN + "Manual mode selected.")
            print(Fore.CYAN + "The lower the threshold level, the stricter the thresholding (filtering out more white pixels) will be.")
            threshold_level = int(input(Fore.CYAN + "Enter the threshold level: "))
            white_pixel_count, total_pixels = calculate_white_stripes(image, threshold_level)
        else:
            white_pixel_count, total_pixels = calculate_white_stripes(image, None)

        print(Fore.CYAN + "Are you satisfied with the results? (y/n)")
        user_satisfied = input(Fore.CYAN).lower()
        if user_satisfied == "y":
            save_results(fileName, white_pixel_count, total_pixels)
            fileName = None  # Reset to allow input for a new file
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            print(Fore.CYAN + "Retrying the same file. You can adjust the parameters.")

if __name__ == "__main__":
    program()
