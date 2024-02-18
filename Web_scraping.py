import selenium
from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import re
import time
from IPython.core.display import HTML
import webbrowser
import requests as rq
import os
import pathlib
import pandas as pd

# DataFrame with all the 294 images:
image_df = pd.read_csv('C:/Users/sahca/AXXESS/Skin-Disease-Image-Classifier-for-Accurate-and-Accessible-Diagnosis-main/Data/data1-294.csv')

# Previewing the first 3 rows of the dataframe
print(image_df.head(3))

# Function takes in the image url and returns an html <img> tag that displays the image
def to_img_tag(path):
    return '<img src="'+ path + '" width="50" >'

# Save the HTML table to a file
with open('C:/Users/sahca/AXXESS/Skin-Disease-Image-Classifier-for-Accurate-and-Accessible-Diagnosis-main/Data/image_table.html', 'w') as f:
    f.write(image_df.to_html(escape=False,formatters=dict(images=to_img_tag)))

webbrowser.open('C:/Users/sahca/AXXESS/Skin-Disease-Image-Classifier-for-Accurate-and-Accessible-Diagnosis-main/Data/image_table.html')



# Downloading and Saving the images into a folder:
def save_image(folder: str, name: str, url: str, index:int):
    # Get the data from the url
    image_source = rq.get(url)

    # If there's a suffix, we will grab that
    suffix = pathlib.Path(url).suffix

    # Check if the suffix is one of the following
    if suffix not in ['.jpg', '.jpeg', '.png', '.gif']:
        # Default to .png
        output = name + str(index) + '.png'

    else:
        output = name + str(index) + suffix

    # Check first if folder exists, else create a new one
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Create our output in the specified folder (wb = write bytes)
    with open(f'{folder}{output}', 'wb') as file:
        file.write(image_source.content)
        print(f'Successfully downloaded: {output}')


if __name__ == '__main__':
    # Load the dataframe with image urls and disease names
    df = pd.read_csv('C:/Users/sahca/AXXESS/Skin-Disease-Image-Classifier-for-Accurate-and-Accessible-Diagnosis-main/Data/data1-294.csv')

    # Loop through the dataframe
    for index, row in df.iterrows():
        # Get the image url and disease name
        image_url = row['images']
        disease_name = row['skin_disorder_name']

        # Save the image
        save_image('Images/', disease_name, image_url, index)
