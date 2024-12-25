# Eyelid Image Analysis

## Overview
This script analyzes images to detect and measure white stripes within an eyelid image. It processes images from a `data` folder and saves results to a CSV file.

## Project Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)

### Installation Steps

1. Clone or download the project to your local machine

2. Create and activate a virtual environment:

    Windows:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```

    Linux/Mac:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install required dependencies:
    ```bash
    pip install -r dependencies.txt
    ```

### Project Structure
```bash
project_root/
├── data/ # Place your .jpg images here
├── result/ # Contains results.csv
├── main.py # Main program file
└── .venv/ # Virtual environment
```


## Using the Analysis Script

1. Place your JPG images in the `data/analysis` folder

2. Run the script:
    ```bash
    python analysis.py
    ```

3. Program Flow:
   - Enter the image filename (without .jpg extension)
   - Choose threshold mode:
     - Press 'M' for manual threshold setting
     - Press any other key for automatic threshold
   - If manual mode:
     - Enter a threshold value (lower values = stricter filtering)
   - Review the results in the displayed windows (Remember to close the windows to proceed with the program by pressing 0)
   - Confirm if satisfied with results (Y/N)
     - Y: Results saved to results.csv
     - N: Retry with different parameters

### Output
The script saves results to `result/results.csv` with the following columns:
- Filename
- Number of pixels representing the white stripes
- Total pixels

### Tips
- Ensure images have clear black outlines around the eyelids
- Start with automatic threshold mode
- If results aren't satisfactory, try manual mode:
  - Lower threshold values filter out more pixels
  - Higher threshold values include more pixels
- Close image windows to proceed with the program

### Troubleshooting
- If image not found: Verify file is in data folder with .jpg extension
- If no black outline detected: Check image has clear black boundaries
- If program crashes: Ensure virtual environment is activated and dependencies installed

## Using the Area Script

1. Place your JPG images in the `data/area` folder

2. Run the script:
    ```bash
    python area.py
    ```

3. Program Flow:
   - The script will process all images in the `data/area` folder
   - It will calculate the area of the subject in each image
   - It will save the results to `result/area.csv`

### Output
The script saves results to `result/area.csv` with the following columns:
- Filename
- Area

### Troubleshooting
- If program crashes: Ensure virtual environment is activated and dependencies installed
