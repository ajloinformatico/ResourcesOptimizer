from PIL import Image
import os

# import sys

FOLDERS = ('optimized_images', 'original_images')
EXTENSIONS = [".jpg", ".jpeg", ".png", ".gift"]
README = 'readme.txt'
CREATED = " created"
EXISTS = " exists"
CAN_NOT_BE_CREATED = " can not be created"
NOT_FOUND = " not found"
COMPRESSED = "compress_by_infolojo_"


class Readme:
    def __init__(self):
        self.readme_name = README
        self.readme_content = """
ImageOptimizeScript

- Put in original_images file the src you want to optimize
- In optimized_images you could find the optimized output
"""


class OSHelper:
    def __init__(self):
        self.folders = FOLDERS
        self.readmeIn = Readme()
        self.readme_created = False
        self.optimized_created = False
        self.original_images_created = False
        self.check_folders()
        self.create_folders_and_files()

    def check_folders(self):
        """
        Scan folders and create necessary folders if is needed
        :return:
        """
        print("Checking folders :\n")
        for item in os.scandir("."):
            if item.name == self.readmeIn.readme_name:
                self.readme_created = True
                print(self.readmeIn.readme_name + EXISTS)
            if item.name == self.folders[0]:
                self.optimized_created = True
                print(self.folders[0] + EXISTS)
            if item.name == self.folders[1]:
                self.original_images_created = True
                print(self.folders[1] + EXISTS)

    def create_folders_and_files(self):
        if not self.readme_created:
            print(self.readmeIn.readme_name + NOT_FOUND)
            try:
                file = open(self.readmeIn.readme_name, "w")
                file.write(self.readmeIn.readme_content + os.linesep)
                file.close()
                print(self.readmeIn.readme_name + CREATED)
            except:
                show_error(3, self.readmeIn.readme_name)

        if not self.optimized_created:
            print(self.folders[0] + NOT_FOUND)
            try:
                os.mkdir(self.folders[0])
                print(self.folders[0] + CREATED)
            except:
                show_error(3, self.folders[0])

        if not self.original_images_created:
            print(self.folders[1] + NOT_FOUND)
            try:
                os.mkdir(self.folders[1])
                print(self.folders[1] + CREATED)
            except:
                show_error(3, self.folders[1])


class Optimizer:
    def __init__(self, range: int = 60):
        self.range = range
        self.original_images = FOLDERS[1]
        self.optimized_folder = FOLDERS[0]
        self.images_to_optimize = list()
        self.check_images()

    def check_images(self):
        # Get the folder where search src
        original_folder = "./" + self.original_images
        optimized_folder = "./" + self.optimized_folder

        print("\nChecking src in " + self.original_images + " :")
        for image in os.listdir(original_folder):

            # split image between name and extension
            name, extension = os.path.splitext(original_folder + image)
            print(name[2:] + "-" + extension)

            if extension in EXTENSIONS:
                picture = Image.open(original_folder + "/" + image)
                picture.save(optimized_folder + "/" + COMPRESSED + str(self.range) + "%_" + image, optmize=True,
                             quality=self.range)
                self.images_to_optimize.append(name[2:] + extension)

        if len(self.images_to_optimize) == 0:
            show_error(2)
            return

        print("\n Working ...\n")

        for image in self.images_to_optimize:
            print(image + "has been saved in " + self.optimized_folder + " and optimized with " + str(self.range)
                  + " of quality")


def show_error(error: int, pre: str = ""):
    """
    Exception control
    :param pre: previous string of the error
    :param error: error default message
    :return:
    """
    if error == 1:
        print("\nrange input is not valid")
    elif error == 2:
        print("\nThere is no src to optimize")
    elif error == 3:
        print(pre + CAN_NOT_BE_CREATED)


def run():
    """
    Init script
    :return (unit):
    """
    global range
    OSHelper()
    try:
        range = input("\n> Input range to optimized or press enter to use default: ")
        if range.replace(" ", "") == "":
            range = 60
        range = int(range)

    except:
        show_error(1)

    if 0 <= range <= 100:
        Optimizer(range)
    else:
        show_error(1)


if __name__ == '__main__':
    run()
