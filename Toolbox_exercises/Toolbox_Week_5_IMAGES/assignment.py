"""
ASSIGNMENT
1. Change script in a class for manipulating a single image.
2. Add three filters:
    - Gray filter
    - Horizontal mirror filter
    - Blur filter
3. Add a function to process a directory filled with images with one filter.
"""

from PIL import Image
from pathlib import Path
import sys


class ImageManipulator:
    def __init__(self, image_path):
        # Open image and convert to RGBA
        self.image_path = Path(image_path)

        try:
            self.image = Image.open(self.image_path).convert("RGBA")
        except Exception as e:
            sys.exit(f"Image.open {self.image_path} failed:\n{e}")

    def get_width(self):
        # Return image width
        width, height = self.image.size
        return width

    def get_height(self):
        # Return image height
        width, height = self.image.size
        return height

    def get_pixel(self, x, y):
        # Return pixel at x, y
        return self.image.getpixel((x, y))

    def set_pixel(self, x, y, pixel):
        # Change pixel at x, y
        self.image.putpixel((x, y), pixel)

    def save_copy(self, output_path):
        # Save image copy
        output_path = Path(output_path)
        self.image.save(output_path)

    def show(self):
        # Show image
        self.image.show()

    def gray_filter(self):
        # Make image gray
        width = self.get_width()
        height = self.get_height()

        for x in range(width):
            for y in range(height):
                r, g, b, a = self.get_pixel(x, y)

                gray = int((r + g + b) / 3)

                self.set_pixel(x, y, (gray, gray, gray, a))

    def mirror_horizontal_filter(self):
        # Mirror image horizontally
        width = self.get_width()
        height = self.get_height()

        new_image = Image.new("RGBA", (width, height))

        for x in range(width):
            for y in range(height):
                pixel = self.get_pixel(x, y)

                new_x = width - 1 - x

                new_image.putpixel((new_x, y), pixel)

        self.image = new_image

    def blur_filter(self):
        # Blur image using surrounding pixels
        width = self.get_width()
        height = self.get_height()

        original_image = self.image.copy()
        new_image = Image.new("RGBA", (width, height))

        for x in range(width):
            for y in range(height):
                red_total = 0
                green_total = 0
                blue_total = 0
                alpha_total = 0
                amount_of_pixels = 0

                # Check 9 surrounding pixels
                for neighbor_x in range(x - 1, x + 2):
                    for neighbor_y in range(y - 1, y + 2):

                        # Check image borders
                        if 0 <= neighbor_x < width and 0 <= neighbor_y < height:
                            r, g, b, a = original_image.getpixel(
                                (neighbor_x, neighbor_y)
                            )

                            red_total += r
                            green_total += g
                            blue_total += b
                            alpha_total += a
                            amount_of_pixels += 1

                average_red = int(red_total / amount_of_pixels)
                average_green = int(green_total / amount_of_pixels)
                average_blue = int(blue_total / amount_of_pixels)
                average_alpha = int(alpha_total / amount_of_pixels)

                new_image.putpixel(
                    (x, y),
                    (average_red, average_green, average_blue, average_alpha),
                )

        self.image = new_image


def process_directory(directory_path, filter_name):
    # Process all images in directory
    directory = Path(directory_path)

    for image_path in directory.iterdir():

        # Only process image files
        if image_path.suffix.lower() not in [".png", ".jpg", ".jpeg"]:
            continue

        manipulator = ImageManipulator(image_path)

        # Choose filter
        if filter_name == "gray":
            manipulator.gray_filter()

        elif filter_name == "mirror":
            manipulator.mirror_horizontal_filter()

        elif filter_name == "blur":
            manipulator.blur_filter()

        else:
            print("Unknown filter.\n")
            return

        # Create output filename
        output_name = image_path.stem + "_" + filter_name + image_path.suffix
        output_path = directory / output_name

        manipulator.save_copy(output_path)

        print("Saved:", output_path)


def main():
    print("\n1. Process one image")
    print("2. Process directory")

    choice = input("Choose 1 or 2: ").strip()

    if choice == "1":
        image_path = input("\nImage path: ").strip()

        manipulator = ImageManipulator(image_path)

        print("\nChoose filter:")
        print("gray")
        print("mirror")
        print("blur")

        filter_name = input("\nFilter: ").strip().lower()

        # Apply selected filter
        if filter_name == "gray":
            manipulator.gray_filter()

        elif filter_name == "mirror":
            manipulator.mirror_horizontal_filter()

        elif filter_name == "blur":
            manipulator.blur_filter()

        else:
            print("Unknown filter.")
            return

        output_path = input("\nOutput filename, for example output: ").strip()
        
        if not ".png" in output_path:
            output_path = output_path + ".png"
           
        manipulator.save_copy(output_path)

        print("Saved:", output_path)

    elif choice == "2":
        directory_path = input("\nDirectory path: ").strip()

        print("\nChoose filter:")
        print("gray")
        print("mirror")
        print("blur")

        filter_name = input("\nFilter: ").strip().lower()

        process_directory(directory_path, filter_name)

    else:
        print("\nInvalid choice.")


if __name__ == "__main__":
    main()