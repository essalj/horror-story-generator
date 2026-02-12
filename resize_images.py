import os
from PIL import Image

def resize_image(input_path, output_path, size=(1920, 1080)):
    """
    Resizes an image to a specified size.

    Args:
        input_path (str): Path to the input image file (PNG or JPG).
        output_path (str): Path to save the resized image file.
        size (tuple): The desired output size as (width, height). Defaults to 1920x1080.
    """
    try:
        img = Image.open(input_path)
        img = img.resize(size, Image.Resampling.LANCZOS) # Use LANCZOS for high-quality downsampling
        img.save(output_path)
        print(f"Successfully resized {input_path} to {output_path}")
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
    except Exception as e:
        print(f"Error resizing {input_path}: {e}")


# resize_image(input_path='/Users/lasse/Downloads/trucker.png', output_path='/Users/lasse/Downloads/trucker_1024.png', size=(1792, 1024))
# '/Users/lasse/Desktop/my/youtube/tn images/tn_trucker_1024p.webp', size=(1792, 1024))
def resize_images_in_directory(input_dir, output_dir, size=(1920, 1080)):
    """
    Resizes all PNG and JPG images in a directory to a specified size.

    Args:
        input_dir (str): Path to the directory containing input image files.
        output_dir (str): Path to save the resized image files.
        size (tuple): The desired output size as (width, height). Defaults to 1920x1080.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        if os.path.isfile(input_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            resize_image(input_path, output_path, size)
        else:
            print(f"Skipping non-image file: {filename}")

if __name__ == "__main__":
    # Example Usage:
    # Create dummy files for testing
    # try:
    #     os.makedirs("input_images", exist_ok=True)
    #     os.makedirs("output_images", exist_ok=True)
    #     # Create dummy image files (requires Pillow)
    #     from PIL import Image
    #     img1 = Image.new('RGB', (100, 200), color = 'red')
    #     img1.save("input_images/test1.png")
    #     img2 = Image.new('RGB', (500, 300), color = 'blue')
    #     img2.save("input_images/test2.jpg")
    #     print("Created dummy image files in 'input_images' directory.")
    # except ImportError:
    #     print("Pillow not installed. Cannot create dummy images. Please install with 'pip install Pillow'")
    # except Exception as e:
    #     print(f"Error creating dummy images: {e}")


    # --- Uncomment the section below to run the resizing ---

    # input_directory = "input_images" # Replace with your input directory
    # output_directory = "output_images" # Replace with your output directory
    # target_size = (1920, 1080) # Desired size (width, height)

    # print(f"Resizing images in '{input_directory}' to {target_size} and saving to '{output_directory}'")
    # resize_images_in_directory(input_directory, output_directory, target_size)
    # print("Image resizing process finished.")

    print("Script created. Please uncomment the example usage section and modify the input/output directories and target size as needed.")