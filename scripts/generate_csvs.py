import csv
import os
from PIL import Image


"""
READ ME

The purpose of this script is to save images as a valid PyMIC file type (png) and 
create the csvs for use in the dataset section of the PyMIC training configs. If 
you don't want to make your own CSVs, you can use the ones found in 
src/ssl_entropy_minimization/config/data/. Just comment out the "with open" loop

This script anticipates the images and their labels are stored in a directory structured
as follows:

Note: the train.txt and valid.txt are specifically called out below because they aren't 
images or labels and they are necessary for the code. The images and labels should be 
placed appropriately in the folders below

main_directory
    |
    ---- "images"
    |       |
    |       --'AppleA/'
    |       |
    |       --'AppleB/'
    |       |
    |       -- 'Pear/'
    |       |
    |       --'Peach/'
    |
    ---- "labels"
            |
            --'AppleA/'
            |   * valid.txt 
            |   * train.txt
            |
            --'AppleB/'
            |
            -- 'Pear/'
            |
            --'Peach/'

"""
# assign directory
main_directory = 'fruit_data/'

"""
## AppleA Pre-processing
# Original AppleA data is handled differently than the other three classes which is 
# why it has its own section.
# This takes a while - would recommend leaving it commented unless you need it

appleA_dir = main_directory + 'images/AppleA'
for filename in os.listdir(appleA_dir):
        f = os.path.join(appleA_dir, filename)
        pathname, _ = os.path.splitext(f)
        pathname = pathname.replace("IMG_0", "")
        
        img = Image.open(f)
        new_name = pathname+".png"
        img.save(pathname+".png")
"""
with open(main_directory+'/labels/AppleA/train.txt', 'r') as f:
    appleA_train_raw = f.readlines()
appleA_train = [i.replace("IMG_0", "").replace("\n", "") for i in appleA_train_raw]

with open(main_directory+'/labels/AppleA/train.txt', 'r') as f:
    appleA_valid_raw = f.readlines()
appleA_valid = [i.replace("IMG_0", "").replace(".JPG\n", ".png") for i in appleA_valid_raw]
print("Finished AppleA Processing, moving on")

# iterate over the remaining fruit classes
file_list = []
fruits = ['AppleB/', 'Pear/', 'Peach/']
for fruit in fruits:
    print(f"Beginning processing for {fruit} directory")
    fruit_files = []
    directory = main_directory + 'images/' + fruit 
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        pathname, _ = os.path.splitext(f)
        
        # Save a downsampled .png file because PyMIC cannot 
        # ingest .bmp files
        img = Image.open(f)
        new_name = pathname+".png"
        img.save(pathname+".png")

    for filename in os.listdir(directory):
        # checking if it is a file
        f = os.path.join(directory, filename)
        if os.path.isfile(f) and f.endswith(".png"):
            train_pair = ['images/'+fruit+filename, 'labels/'+fruit+filename]
            fruit_files.append(train_pair)

    file_list.append(fruit_files)

print("Beginning CSV file Creation")
with open('image_train.csv', 'w') as f:
    write = csv.writer(f)
    for fruit_list in file_list:
        write.writerows(fruit_list[2:-5])
    write.writerows(appleA_train[:-15])
with open('image_valid.csv', 'w') as f:
    write = csv.writer(f)
    for fruit_list in file_list:
        write.writerows(fruit_list[:2])
    write.writerows(appleA_valid)
with open('image_test.csv', 'w') as f:
    write = csv.writer(f)
    for fruit_list in file_list:
        write.writerows(fruit_list[-5:])
    write.writerows(appleA_valid[-15:])

