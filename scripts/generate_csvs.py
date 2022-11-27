import csv
import os
from PIL import Image
# assign directory
main_directory = '../fruit_data/'
fruits = ['AppleB/', 'Pear/', 'Peach/']
 
# iterate over the different fruit classes
file_list = []
for fruit in fruits:
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
            file_list.append(train_pair)

with open('image_train_pngs.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(file_list)
