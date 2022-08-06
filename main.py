import os
import sys
from typing import List, Tuple

from PIL import Image

FOLDERS: Tuple[str, str] = ('optimized_images', 'original_images')
EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".gift"]

ARGUMENT_IMAGE: str = "img"
ARGUMENT_QUALITY: str = "q"
ARGUMENT_C_DIRECTORY: str = "c_directory"
ARGUMENT_OUT_PUT: str = "output"
ARGUMENT_HELP: str = "help"
ARGUMENTS: List[str] = [ARGUMENT_IMAGE, ARGUMENT_QUALITY, ARGUMENT_C_DIRECTORY, ARGUMENT_OUT_PUT, ARGUMENT_HELP]
README: str = 'readme.txt'
CREATED: str = " created"
EXISTS: str = " exists"
CAN_NOT_BE_CREATED: str = " can not be created"
NOT_FOUND: str = " not found or not exist"
COMPRESSED: str = "compress_by_infolojo_"


class Readme:
    def __init__(self):
        self.readme_name = README
        self.readme_content = """
ImageOptimizeScript

Its an script with params to optimize images. 

INSTALL
pip install -r requirements.txt
python3 main.py -> will run and optimize all the images in the current folder.

USAGE use commands to run specific files

Commands :
  - img=example.jpg             -> image to optimize / default * (all)
  - q=55                        -> quality to optimize / default 60 %
  - c_directory="new_folder"    -> folder to search images / default "." (current directory)
  - output="new_folder"         -> folder where found images / default "." (current directory)
  - help                        -> show instructions
"""


class OSHelper:
    def __init__(self):
        self.folders = FOLDERS
        self.readmeIn = Readme()
        self.readme_created = False
        self.check_readme()

        if not self.readme_created:
            self.create_readme()

    def check_readme(self):
        """
        Scan folders and create necessary folders if is needed
        :return:
        """
        for item in os.scandir("."):
            if item.name == self.readmeIn.readme_name:
                self.readme_created = True

    def create_readme(self):
        """
        Create a readme.txt file with instructions if this not exists
        """
        if not self.readme_created:
            print(self.readmeIn.readme_name + NOT_FOUND)
            try:
                file = open(self.readmeIn.readme_name, "w")
                file.write(self.readmeIn.readme_content + os.linesep)
                file.close()
            except:
                show_error(3, self.readmeIn.readme_name)

    @staticmethod
    def check_if_folder_exists(directory: str):
        """
        Check if a folder exist
        """
        os.path.exists(directory)

    @staticmethod
    def create_folder(directory: str):
        """
        Create directory
        """
        try:
            os.mkdir(directory)
        except:
            show_error(3, directory)


class Optimizer:
    def __init__(self, file: str = "*", q: int = 60, current_directory: str = ".", output: str = ".",
                 os_helper: OSHelper = OSHelper()):
        self.file: str = file
        self.quality: int = q
        self.output: str = output
        self.os_helper: OSHelper = os_helper
        self.images_to_optimize = list()
        self.current_folder: str = current_directory
        self.start()

    def start(self):
        if not self.os_helper.check_if_folder_exists(self.current_folder) and self.current_folder != ".":
            show_error(4, self.current_folder)

        # create destination directory
        if self.output != ".":
            self.os_helper.create_folder(self.output)

        # optimize all the images
        if self.file == "*":
            for image in os.listdir(self.current_folder):
                self.optimize_image(image)
        # optimize only one image
        else:
            for image in os.listdir(self.current_folder):
                if image == self.file:
                    self.optimize_image(image)

        # check if images has been optimized
        if len(self.images_to_optimize) == 0:
            show_error(2)
            return

        print("\n Working ...\n")

        for image in self.images_to_optimize:
            print(image + "has been saved in " + self.output + " and optimized with " + str(self.quality)
                  + " of quality")

    def optimize_image(self, image):
        """
        Optimize an image
        """

        # split image between name and extension
        name, extension = os.path.splitext(self.current_folder + image)
        if extension in EXTENSIONS:
            # Optimize image
            picture = Image.open(self.current_folder + "/" + image)
            picture.save(self.output + "/" + COMPRESSED + str(self.quality) + "%_" + image, optmize=True,
                         quality=self.quality)
            self.images_to_optimize.append(name[2:] + extension)


def show_error(error: int, pre: str = ""):
    """
    Exception control
    :param pre: previous string of the error
    :param error: error default message
    :return:
    """
    if error == 1:
        print("\nquality input is not valid, default 60% will be applied")
    elif error == 2:
        print("\nThere is no src to optimize")
        exit(-1)
    elif error == 3:
        print(pre + CAN_NOT_BE_CREATED)
    elif error == 4:
        print(pre + NOT_FOUND)
        exit(-1)


def run():
    """
    Init script
    :return (unit):
    """
    os_helper = OSHelper()
    img = "*"
    quality: int = 60
    current_directory = "."
    output = "."

    arguments = sys.argv
    arguments.pop(0)
    if len(arguments) >= 1:

        if ARGUMENT_HELP in arguments:
            print(os_helper.readmeIn.readme_content)
            arguments.remove(ARGUMENT_HELP)
            continue_flag = input("Do you want to continue with execute?\n> ").lower()
            if "si" != continue_flag != "true":
                exit(-1)

        for argument in arguments:
            arg, value = argument.split("=")
            arg = arg.lower()
            if arg == ARGUMENT_IMAGE:
                img = value
            elif arg == ARGUMENT_QUALITY:
                value = int(value)
                try:
                    if 0 < value < 100:
                        quality = value
                    else:
                        show_error(1)
                except:
                    show_error(1)
            elif arg == ARGUMENT_C_DIRECTORY:
                current_directory = value
            elif arg == ARGUMENT_OUT_PUT:
                output = value
    Optimizer(
        file=img,
        q=quality,
        current_directory=current_directory,
        output=output,
        os_helper=os_helper
    )


if __name__ == '__main__':
    run()
