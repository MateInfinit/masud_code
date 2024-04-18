import boto3
from PIL import Image
import copy
import tkinter as tk

handwritten_text_detected = ''
loading_label = None  # Define loading label globally
result_label = None  # Define label to display result globally
detected_text = None  # Define label to display detected text globally

def analyze_cell(image_path, region='us-east-1'):
    client = boto3.client('rekognition', region_name=region)

    with open(image_path, 'rb') as image:
        image_data = image.read()

    # Detect labels
    response_labels = client.detect_labels(Image={'Bytes': image_data})
    labels = [label['Name'].lower() for label in response_labels['Labels']]

    # Detect text
    response_text = client.detect_text(Image={'Bytes': image_data})
    detected_texts = [text['DetectedText'] for text in response_text['TextDetections']]

    # Save detected text if found
    detected_text = ', '.join(detected_texts)

    return 'tree' in labels, detected_text

def create_matrix(image_path):
    matrix = [[0 for _ in range(5)] for _ in range(5)]

    for i in range(5):
        for j in range(5):
            cell_image_path = crop_cell(image_path, i, j)
            tree_found, text_found = analyze_cell(cell_image_path)
            matrix[i][j] = 1 if tree_found else 0

            # If text is found, update the detected text label
            if text_found:
                detected_text.config(text=f"This is your forest: {text_found}")

    return matrix

def crop_cell(image_path, row, col):
    img = Image.open(image_path)

    width, height = img.size
    cell_width = width // 5
    cell_height = height // 5

    left = col * cell_width
    upper = row * cell_height
    right = (col + 1) * cell_width
    lower = (row + 1) * cell_height

    cell_image = img.crop((left, upper, right, lower))

    cell_image_path = f'cell_{row}_{col}.png'
    cell_image.save(cell_image_path)

    return cell_image_path

def has_nearby_fire(x, y, matrixSimulation):
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 5 and 0 <= ny < 5 and matrixSimulation[ny][nx] == -1:
            return True
    return False

averageFinalDensity = 0.0

def simulation(i, j):
    global result_matrix
    matrixSimulation = copy.deepcopy(result_matrix)
    matrixSimulation[i][j] = -1
    copymatrix = copy.deepcopy(matrixSimulation)
    foundFire = True
    while foundFire:
        foundFire = False
        for x in range(5):
            for y in range(5):
                if has_nearby_fire(x, y, matrixSimulation) and matrixSimulation[x][y] == 1:
                    copymatrix[x][y] = -1
                    foundFire = True
                elif matrixSimulation[x][y] == -1:
                    copymatrix[x][y] = 0
                    foundFire = True
        matrixSimulation = copy.deepcopy(copymatrix)
    cont = 0
    for x in range(5):
        for y in range(5):
            if matrixSimulation[x][y] == 1:
                cont += 1
    global averageFinalDensity
    averageFinalDensity += cont / 25 * 100

def matrix_burn():
    global result_matrix
    cont = 0
    for i in range(5):
        for j in range(5):
            if result_matrix[i][j] == 1:
                simulation(i, j)
                cont += 1
    initialPercentage = cont / 25 * 100
    initial_label.config(text=f"Initial Percentage: {initialPercentage:.2f}%")
    global averageFinalDensity
    averageFinalDensity = averageFinalDensity / cont
    average_label.config(text=f"Average Final Percentage: {averageFinalDensity:.2f}%")

    # Update the UI with the forest matrix
    update_ui(result_matrix)

def create_ui():
    root = tk.Tk()
    root.title("Forest Fire Simulation")

    frame = tk.Frame(root)
    frame.pack()

    # Create placeholders for the matrix cells
    matrix_cells = [[None] * 5 for _ in range(5)]

    for i in range(5):
        for j in range(5):
            cell = tk.Label(frame, text="", bg="white", width=15, height=8, borderwidth=1, relief="solid")
            cell.grid(row=i, column=j)
            matrix_cells[i][j] = cell

    return root, matrix_cells

def update_ui(matrix):
    for i in range(5):
        for j in range(5):
            cell_color = "green" if matrix[i][j] == 1 else "white"
            matrix_cells[i][j].config(bg=cell_color)

def show_loading():
    global loading_label
    loading_label = tk.Label(root, text="Processing matrix, please wait...", font=('Arial', 12))
    loading_label.pack()

def hide_loading():
    global loading_label
    if loading_label:
        loading_label.destroy()

def calculate_score():
    bestmatrices = [54,51.5,51.2,49.6,49.0667,48.5714,48,46.7692,46.1538,44.9231,44.3077,44,43.3333,42.6667,42,41.3333,40.6667,40,39.2727,38.5455,37.8182,37.0909,36.3636,36,35.2]
    if averageFinalDensity < bestmatrices[24]:
        print("Your forest didn't make it into the top 25 best forests. Try again!")
    else:
        for i, score in enumerate(bestmatrices):
            if bestmatrices[i] == averageFinalDensity:
                score_forest.config(text=f"Score of the forest:{i+1}")
                break

# Example usage
image_path = 'C:\\matei\\masud\\treePhoto.jpeg'
result_matrix = create_matrix(image_path)

# Create the UI window
root, matrix_cells = create_ui()

# Initial Percentage Label
initial_label = tk.Label(root, text="", font=('Arial', 30))
initial_label.pack()

# Average Final Percentage Label
average_label = tk.Label(root, text="", font=('Arial', 30))
average_label.pack()

calculate_score()
score_forest = tk.Label(root,text ="", font = ('Arial', 30))
score_forest.pack()

detected_text = tk.Label(root, text="", font=('Arial', 14))
detected_text.pack()

# Show loading message
show_loading()

# Process matrix
matrix_burn()

# Hide loading message
hide_loading()

# Start the UI event loop
root.mainloop()