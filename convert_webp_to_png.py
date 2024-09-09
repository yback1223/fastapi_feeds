from PIL import Image

# List of image file paths (webp format)
image_paths = ["1.webp", "2.webp", "3.webp", "4.webp", "5.webp"]

# Function to convert webp to png and resize to 768x768
def convert_webp_to_png(image_path):
    try:
        img = Image.open(image_path)
        # Resize image to 768x768
        img = img.resize((768, 768))
        png_image_path = image_path.replace(".webp", ".png")
        img.save(png_image_path, "png")
        return f"Converted and resized {image_path} to {png_image_path} with resolution 768x768"
    except Exception as e:
        return f"Error converting {image_path}: {e}"

# Convert all images in the list
conversion_results = [convert_webp_to_png(image_path) for image_path in image_paths]

# Output the results
for result in conversion_results:
    print(result)
