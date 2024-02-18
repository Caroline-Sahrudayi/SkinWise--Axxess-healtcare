# import required libraries
import shutil
import os
from PIL import Image
import imagehash
import random
import pandas as pd


# load and preview dataset
image_df = pd.read_csv('C:/Users/sahca/AXXESS/Skin-Disease-Image-Classifier-for-Accurate-and-Accessible-Diagnosis-main/Data/data1-294.csv')
print(image_df.shape)
print(image_df.head())

# Labels representing acne in DermNet's scrapped data
acne_labels = list(image_df[image_df['skin_disorder_name'].str.contains('acne')]['skin_disorder_name'].unique())

# removing acne labels whose images will not be used because there are not clear
acne_labels.remove('infantile acne images')
acne_labels.remove('steroid acne images')

print(acne_labels)


# Getting the acne images file names
original_acne_img = [image_name for image_name in os.listdir('Images/') \
                     if ('acne affecting the back images' in image_name) |\
                        ('acne affecting the face images' in image_name) |\
                        ('acne and other follicular disorder images' in image_name) |\
                        ('facial acne images' in image_name)
                        ]

# Confirming the number of acne images before any cleaning
print('There are', len(original_acne_img),'acne images')
print(original_acne_img[:5])

# Creating a new folder with just acne images to make cleaning easier
folder_name = 'cleaned_images/acne_images/'

# Checking if the folder exists and deleting it if it exists
if os.path.exists(folder_name):
    # deleting the folder and its contents
    shutil.rmtree(folder_name)

# create the new folder
os.mkdir(folder_name)

# Moving the images into that folder
for img in original_acne_img:
    origin = os.path.join('C:/Users/sahca/AXXESS/Skin-Disease-Image-Classifier-for-Accurate-and-Accessible-Diagnosis-main/Images/', img)
    destination = os.path.join(folder_name, img)
    shutil.copy(origin, destination)

# Confirming that the number of acne images after moving them to a separate folder is still 702
acne_img = [image_name for image_name in os.listdir('C:/Users/sahca/AXXESS/Skin-Disease-Image-Classifier-for-Accurate-and-Accessible-Diagnosis-main/cleaned_images/acne_images/')]
print('There are', len(acne_img),'acne images.')


# extra acne images
extra_acne = [image_name for image_name in os.listdir('C:/Users/sahca/AXXESS/Skin-Disease-Image-Classifier-for-Accurate-and-Accessible-Diagnosis-main/extra_images/extra_acne_images')]
print(extra_acne[:5])


# moving the extra images into the acne folder
for img in extra_acne:
    origin = os.path.join('extra_images/extra_acne_images/', img)
    destination = os.path.join('cleaned_images/acne_images/', img)
    shutil.copy(origin, destination)

# Confirming that the total acne images is 1427 before any cleaning
acne_img = [image_name for image_name in os.listdir('cleaned_images/acne_images/')]
print('There are a total of', len(acne_img),'acne images.')

# Function for removing duplicated images.
def drop_duplicated_images(folder):

    # Define a threshold for image similarity
    threshold = 8

    # Define a dictionary to store the hash values and file paths of the images
    image_hashes = {}
    duplicated_images = []

    # Loop through all the image files in a directory
    for filename in os.listdir(folder):
        # Load the image file
        image = Image.open(os.path.join(folder, filename))

         # Compute the hash value of the image using the average hash algorithm
        hash_value = imagehash.average_hash(image)

        # Check if the hash value is already in the dictionary
        if hash_value in image_hashes:
            # If a similar hash value already exists, delete the duplicate image
            duplicated_images.append(filename)
            os.remove(os.path.join(folder, filename))
        else:
             # Otherwise, add the hash value and file path to the dictionary
            image_hashes[hash_value] = os.path.join(folder, filename)

    return duplicated_images

# Dropping duplicates
duplicated_images = drop_duplicated_images('cleaned_images/acne_images/')

# number of acne images after removing duplicated images (1109)
acne_img = [image_name for image_name in os.listdir('cleaned_images/acne_images/')]
print('There are', len(acne_img),'acne images after removing duplicated images')

# dropping those images from the acne_images folder
indexes_to_drop = [295, 296, 297, 298, 300, 303, 304, 307, 308, 309, 310, 311, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 325, 326, 328, 329, 330, 333, 337, 338, 339, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 354, 355, 359, 361, 362, 363, 364, 366, 367, 368, 371, 372, 373, 374, 375, 376, 378, 380, 381, 382, 384, 385, 387, 388, 389, 390, 392, 393, 395, 396, 397, 398, 402, 403, 405, 408, 409, 411, 413, 415, 416, 417, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 431, 432, 433, 434, 436, 437, 438, 441, 443, 444, 445, 446, 447]

for filename in os.listdir('cleaned_images/acne_images/'):
    for index in indexes_to_drop:
        if f"images{index}" in filename.lower():
            os.remove(os.path.join('cleaned_images/acne_images/', filename))

print("Number of acne images left:", len(os.listdir('cleaned_images/acne_images/')))


# Labels representing eczema in Dermnet's scraped data.
eczema_labels = image_df[(image_df['skin_disorder_name'].str.contains('eczema')) | \
                         (image_df['skin_disorder_name'].str.contains('atopic dermatitis images')) |\
                         (image_df['skin_disorder_name'].str.contains('hand dermatitis images')) |\
                         (image_df['skin_disorder_name'] == 'dermatitis images') |\
                         (image_df['skin_disorder_name'].str.contains('nummular dermatitis images'))] \
                         ['skin_disorder_name'].unique()
len(eczema_labels)

# Getting the eczema images file names
eczema_img = [image_name for image_name in os.listdir('Images/') if ('eczema' in image_name) |
                                                                    ('atopic dermatitis images' in image_name) |
                                                                    ('hand dermatitis images' in image_name) |
                                                                    (image_name.startswith('dermatitis images'))|
                                                                    ('nummular dermatitis images' in image_name)
                                                                     ]

# Confirming the number of eczema images before any cleaning
print('There are', len(eczema_img),'eczema images.')
eczema_img[:5]

# Creating a new folder with just eczema images to make cleaning easier
folder_name = 'cleaned_images/eczema_images/'

# Note📝: For reproducibility of the code, this step is important.
         # If the folder is not dropped before an error will occur if you rerun this cell

# Checking if the folder exists and deleting it if it exists
if os.path.exists(folder_name):
    # deleting the folder and its contents
    shutil.rmtree(folder_name)

# create the new folder
os.mkdir(folder_name)

# Moving the images into that folder
for img in eczema_img:
    origin = os.path.join('Images/', img)
    destination = os.path.join(folder_name, img)
    shutil.copy(origin, destination)
    

# Confirming that the number of eczema images after moving them to a separate folder is still 631
eczema_img = [image_name for image_name in os.listdir('cleaned_images/eczema_images/')]
print('There are', len(eczema_img),'eczema images.')


 # Extra eczema images
extra_eczema = [image_name for image_name in os.listdir('extra_images/extra_eczema')]

# The folder has a mixture of images. We will filter out the eczema images only
extra_eczema_images = [image_name for image_name in extra_eczema\
                        if ('dermatitis' in image_name) |\
                        ('eczema' in image_name)]
print(extra_eczema_images[:5])

  # This was done by moving the extra images into the eczema folder
for img in extra_eczema_images:
    origin = os.path.join('extra_images/extra_eczema_images_clean/', img)
    destination = os.path.join('cleaned_images/eczema_images/', img)
    shutil.copy(origin, destination)

# Confirming that the total acne images is 1367 before any cleaning
eczema_img = [image_name for image_name in os.listdir('cleaned_images/eczema_images/')]
print('There are a total of', len(eczema_img),'eczema images.')
 
 
# Using a function created earlier to drop duplicates
duplicated_images = drop_duplicated_images('cleaned_images/eczema_images/')

# Confirming the number of images after dropping duplicates
eczema_img = [image_name for image_name in os.listdir('cleaned_images/eczema_images/')]
print('There are', len(eczema_img),'eczema images after removing duplicated images.') 

# image labels with the name keratosis in DermNet's scrapped data
print(image_df[image_df['skin_disorder_name'].str.contains('keratosis')]['skin_disorder_name'].unique())

# extra keratosis images and dataframe
df = pd.read_csv('C:/Users/sahca/AXXESS/Skin-Disease-Image-Classifier-for-Accurate-and-Accessible-Diagnosis-main/Data/ISIC_2019_Training_GroundTruth.csv')

# filter df to get rows where AK = 1.0
df1 = df.copy()
df1 = df1[df1['AK'] == 1.0]
df1['skin_disorder_name'] = df1['images']

# drop the unwanted columns from df
df1 = df1.drop(['MEL', 'NV', 'BCC', 'AK', 'BKL', 'DF', 'VASC', 'SCC', 'UNK'], axis=1)

# Loop through each file in the folder and add the skin disorder name to the list
img_names = []
image_paths = []

for file in os.listdir('extra_images/extra_actinic_keratosis_images'):
    if file.endswith(".jpg"):
        skin_disorder_name = file.split(".")[0]
        img_names.append(skin_disorder_name)
        image_paths.append(file)
        
# Getting the keratosis images file names
keratosis_img = [image_name for image_name in os.listdir('Images/') if ('actinic keratosis' in image_name) | ('solar keratosis' in image_name)]
AK_img = [image_name for image_name in os.listdir('extra_images/extra_AK_and_BKL_images') if any(x in image_name for x in df1['images'].tolist())]
AK_img2 = [image_name for image_name in os.listdir('extra_images/extra_actinic_keratosis_images')]

# Checking if the folder exists and deleting it if it exists
if os.path.exists('cleaned_images/keratosis_images/'):
    # deleting the folder and its contents
    shutil.rmtree('cleaned_images/keratosis_images/')

# Creating a new folder with just keratosis images to make cleaning easier
os.mkdir('cleaned_images/keratosis_images/')
for img in keratosis_img:
    origin = os.path.join('Images/', img)
    destination = os.path.join('cleaned_images/keratosis_images/', img)
    shutil.copy(origin, destination)

for img in AK_img:
    origin = os.path.join('extra_images/extra_AK_and_BKL_images/', img)
    destination = os.path.join('cleaned_images/keratosis_images/', img)
    shutil.copy(origin, destination)

for img in AK_img2:
    origin = os.path.join('extra_images/extra_actinic_keratosis_images/', img)
    destination = os.path.join('cleaned_images/keratosis_images/', img)
    shutil.copy(origin, destination)

# Confirming that the number of keratosis images after moving them to a separate folder is still 1391
keratosis_img = [image_name for image_name in os.listdir('cleaned_images/keratosis_images/')]
print('There are', len(keratosis_img),'actinic keratosis images') 

# call function to drop duplicates from image folder
duplicated_images = drop_duplicated_images('cleaned_images/keratosis_images/')

# number of images after removing duplicates
keratosis_img = [image_name for image_name in os.listdir('cleaned_images/keratosis_images/')]
print('Number of actinic keratosis images after removing duplicated images:', len(keratosis_img)) 

# filter df to get rows where BKL = 1.0
BKL_df = df.copy()
BKL_df = BKL_df[BKL_df['BKL'] == 1.0]
BKL_df = BKL_df[~BKL_df["images"].str.contains("downsampled")]
BKL_df['skin_disorder_name'] = BKL_df['images']

# drop the unwanted columns and rows from df
BKL_df = BKL_df.drop(['MEL', 'NV', 'BCC', 'AK', 'BKL', 'DF', 'VASC', 'SCC', 'UNK'], axis=1)
BKL_df = BKL_df[:1003]

# Getting the BKL images file names
BKL_img = [image_name for image_name in os.listdir('extra_images/extra_AK_and_BKL_images') if any(x in image_name for x in BKL_df['images'].tolist())]

# Checking if the folder exists and deleting it if it exists
if os.path.exists('cleaned_images/BKL_images/'):
    # deleting the folder and its contents
    shutil.rmtree('cleaned_images/BKL_images/')

# Creating a new folder with just BKL images to make cleaning easier
os.mkdir('cleaned_images/BKL_images/')
for img in BKL_img:
    origin = os.path.join('extra_images/extra_AK_and_BKL_images/', img)
    destination = os.path.join('cleaned_images/BKL_images/', img)
    shutil.copy(origin, destination)

# Number of BKL images after moving them to a separate folder
BKL_img = [image_name for image_name in os.listdir('cleaned_images/BKL_images/')]
print('There are', len(BKL_img),'BKL images') 


# use the function to drop duplicates from image folder
duplicated_images2 = drop_duplicated_images('cleaned_images/BKL_images/')

# number of images after removing duplicates
BKL_img = [image_name for image_name in os.listdir('cleaned_images/BKL_images/')]
print('Number of BKL images after removing duplicated images:', len(BKL_img))

## Labels representing melanoma in DermNet's scrapped data
melanoma_labels = image_df[image_df['skin_disorder_name'].str.contains('melanoma')]['skin_disorder_name'].unique()
print(melanoma_labels)

#number of labels representing melanoma
print(len(melanoma_labels))

# Getting the melanoma images file names
melanoma_img = [image_name for image_name in os.listdir('Images/') if 'melanoma' in image_name]

# Checking if melanoma folder exists and deleting it if it exists
if os.path.exists('cleaned_images/melanoma/'):
    # deleting the folder and its contents
    shutil.rmtree('cleaned_images/melanoma/')

# Creating a new folder with just melanoma images to make cleaning easier
os.mkdir('cleaned_images/melanoma/')
for img in melanoma_img:
    origin = os.path.join('Images/', img)
    destination = os.path.join('cleaned_images/melanoma/', img)
    shutil.copy(origin, destination)

for filename in os.listdir('extra_images/extra_melanoma_images/'):
    src_path = os.path.join('extra_images/extra_melanoma_images/', filename)
    dst_path = os.path.join('cleaned_images/melanoma/', filename)
    shutil.copy(src_path, dst_path)

# Number of melanoma images after moving them to a separate folder
melanoma_img = [image_name for image_name in os.listdir('cleaned_images/melanoma/')]
print('There are', len(melanoma_img),'melanoma images')

     
# Dropping duplicates
duplicated_images = drop_duplicated_images('cleaned_images/melanoma/')

melanoma_img = [image_name for image_name in os.listdir('cleaned_images/melanoma/')]
print('There are', len(melanoma_img),'melanoma images after removing duplicate images')

# Function to randomly select 1000 images
def reduce_images(folder_path):
    # Get the list of image file name
    file_names = os.listdir(folder_path)

    # Shuffle the file names
    random.shuffle(file_names)

    # Select the first 1000 file names
    selected_file_names = file_names[:1000]

    # Create a new folder to store the selected images
    selected_folder_path = f'{folder_path}_images'
    os.mkdir(selected_folder_path)

    # Copy the selected images to the new folder
    for file_name in selected_file_names:
        file_path = os.path.join(folder_path, file_name)
        selected_file_path = os.path.join(selected_folder_path, file_name)
        shutil.copy(file_path, selected_file_path)
        
# select 1000 images
reduce_images('cleaned_images/melanoma')
print('Number of melanoma images:', len([image_name for image_name in os.listdir('cleaned_images/melanoma_images/')]))

# Labels representing acne in DermNet's scrapped data
psoriasis_labels = list(image_df[image_df['skin_disorder_name'].str.contains('psoriasis')]['skin_disorder_name'].unique())
print(psoriasis_labels)

# Count of labels representing psoriasis
len(psoriasis_labels)

# Getting the psoriasis images file names
psoriasis_img = [image_name for image_name in os.listdir('Images/') if 'psoriasis' in image_name]

# Checking if psoriasis folder exists and deleting it if it exists
if os.path.exists('cleaned_images/psoriasis/'):
    # deleting the folder and its contents
    shutil.rmtree('cleaned_images/psoriasis/')

# Creating a new folder with just psoriasis images to make cleaning easier
os.mkdir('cleaned_images/psoriasis/')
for img in psoriasis_img:
    origin = os.path.join('Images/', img)
    destination = os.path.join('cleaned_images/psoriasis/', img)
    shutil.copy(origin, destination)

for filename in os.listdir('extra_images/extra_psoriasis_images/'):
    src_path = os.path.join('extra_images/extra_psoriasis_images/', filename)
    dst_path = os.path.join('cleaned_images/psoriasis/', filename)
    shutil.copy(src_path, dst_path)

# Number of psoriasis images after moving them to a separate folder
psoriasis_img = [image_name for image_name in os.listdir('cleaned_images/psoriasis/')]
print('There are', len(psoriasis_img),'psoriasis images')

# Dropping duplicates
duplicated_images = drop_duplicated_images('cleaned_images/psoriasis/')

psoriasis_img = [image_name for image_name in os.listdir('cleaned_images/psoriasis/')]
print('There are', len(psoriasis_img),'psoriasis images after removing duplicate images')

# select 1000 images
reduce_images('cleaned_images/psoriasis')
print('Number of psoriasis images:', len([image_name for image_name in os.listdir('cleaned_images/psoriasis_images/')]))

# filter df to get rows where BKL = 1.0
BCC_df = df.copy()
BCC_df = BCC_df[BCC_df['BCC'] == 1.0]
BCC_df = BCC_df[~BCC_df["images"].str.contains("downsampled")]
BCC_df['skin_disorder_name'] = BCC_df['images']

# drop the unwanted columns and rows from df
BCC_df = BCC_df.drop(['MEL', 'NV', 'BCC', 'AK', 'BKL', 'DF', 'VASC', 'SCC', 'UNK'], axis=1)
BCC_df = BCC_df[:1073]

# Getting the BCC images file names
BCC_img = [image_name for image_name in os.listdir('extra_images/extra_Bcc_images') if any(x in image_name for x in BCC_df['images'].tolist())]

# Checking if the folder exists and deleting it if it exists
if os.path.exists('cleaned_images/Bcc_images'):
    # deleting the folder and its contents
    shutil.rmtree('cleaned_images/Bcc_images')

# Creating a new folder with just BCC images to make cleaning easier
os.mkdir('cleaned_images/Bcc_images')
for img in BCC_img:
    origin = os.path.join('extra_images/extra_Bcc_images/', img)
    destination = os.path.join('cleaned_images/Bcc_images/', img)
    shutil.copy(origin, destination)

# Number of BCC images after moving them to a separate folder
BCC_img = [image_name for image_name in os.listdir('cleaned_images/Bcc_images')]
print('There are', len(BCC_img),'BCC images')


# use the function to drop duplicates from image folder
duplicated_images2 = drop_duplicated_images('cleaned_images/Bcc_images/')

# number of images after removing duplicates
BCC_img = [image_name for image_name in os.listdir('cleaned_images/Bcc_images')]
print('Number of BCC images after removing duplicated images:', len(BCC_img))

## Labels representing tinea in DermNet's scrapped data
tinea_labels = image_df[image_df['skin_disorder_name'].str.contains('tinea')]['skin_disorder_name'].unique()
tinea_labels

# Getting the tinea images file names
tinea_img = [image_name for image_name in os.listdir('Images/') if 'tinea' in image_name]

# Checking if tinea folder exists and deleting it if it exists
if os.path.exists('cleaned_images/tinea/'):
    # deleting the folder and its contents
    shutil.rmtree('cleaned_images/tinea/')

# Creating a new folder with just tinea images to make cleaning easier
os.mkdir('cleaned_images/tinea/')
for img in tinea_img:
    origin = os.path.join('Images/', img)
    destination = os.path.join('cleaned_images/tinea/', img)
    shutil.copy(origin, destination)

for filename in os.listdir('extra_images/extra_tinea_images/'):
    src_path = os.path.join('extra_images/extra_tinea_images/', filename)
    dst_path = os.path.join('cleaned_images/tinea/', filename)
    shutil.copy(src_path, dst_path)

# Number of tinea images after moving them to a separate folder
tinea_img = [image_name for image_name in os.listdir('cleaned_images/tinea/')]
print('There are', len(tinea_img),'tinea images')

# Dropping duplicates
duplicated_images = drop_duplicated_images('cleaned_images/tinea/')

tinea_img = [image_name for image_name in os.listdir('cleaned_images/tinea/')]
print('There are', len(tinea_img),'tinea images after removing duplicate images')

# select 1000 images
reduce_images('cleaned_images/tinea')
print('Number of tinea images:', len([image_name for image_name in os.listdir('cleaned_images/tinea_images/')]))