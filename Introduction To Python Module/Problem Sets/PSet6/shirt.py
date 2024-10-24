import os
import sys
from PIL import Image, ImageOps

def main():

    input_image = sys.argv[1]
    output_image = sys.argv[2]

    check_args_validity(input_image, output_image)
    files_check(input_image, output_image)
    fit_shirt(input_image, output_image)


def check_args_validity(input_image, output_image):

    if len(sys.argv) < 3:
        sys.exit("Too few command-line arguments")

    elif len(sys.argv) > 3:
        sys.exit("Too many command-line arguments")

    elif not os.path.isfile(input_image):
        sys.exit("Invalid input")


def files_check(input_image, output_image):

    if not (
        input_image.endswith((".jpg", ".jpeg", ".png")) and
        output_image.endswith((".jpg", ".jpeg", ".png")) and
        os.path.splitext(input_image)[-1] == os.path.splitext(output_image)[-1]
    ):
        sys.exit("Both input and output files must be either .jpg, .jpeg, or .png and have the same extension")

def fit_shirt(input_image, output_image):

     # Open the shirt image and resize the input image to match the shirt's dimensions
    shirt = Image.open("shirt.png")
    image = Image.open(input_image)

    image = ImageOps.fit(image, shirt.size)

    image.paste(shirt, (0, 0))

    image.save(output_image)

if __name__ == "__main__":
    main()