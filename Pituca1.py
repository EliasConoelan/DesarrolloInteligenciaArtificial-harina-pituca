#!/usr/bin/env python
# coding: utf-8

# In[7]:


# CONVERTIR XML A CSV
import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET


def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for member in root.findall('object'):
            value = ('images/'+root.find('filename').text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text),
                     member[0].text,
                     )
            xml_list.append(value)
    column_name = ['filename', 'xmin','ymin','xmax', 'ymax', 'class']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


# In[8]:


#tenemos toda la información de todo los data frame de panda - estrucura
image_path = os.path.join(os.getcwd(), 'images/')
dataset_df = xml_to_csv(image_path)


print('Completed')


# In[9]:


#comprobar las regiones de las imagenes y las imagenes de interes
import skimage.io as io
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import matplotlib.patches as patches

get_ipython().run_line_magic('matplotlib', 'inline')

def showObjects(image_df):

    img_path = image_df.filename

    image = io.imread(img_path)
    draw = image.copy()
    
    # Create figure and axes
    fig,ax = plt.subplots(1)
    ax.imshow(draw)
    rect = patches.Rectangle((image_df.xmin,image_df.ymin),
                             image_df.xmax-image_df.xmin,image_df.ymax-image_df.ymin,
                             linewidth=1,edgecolor='r',facecolor='none')

    plt.axis('off')
    ax.add_patch(rect)
    plt.show()


# In[10]:


#imprimimos cada foto mediante la función 
showObjects(dataset_df.iloc[10])


# In[12]:


#definimos que parte sera para prueba y que parte 
#sera de entrenamiento mediante el split
train_df, test_df = train_test_split(
  dataset_df, 
  test_size=0.2, 
  random_state=2
)


# In[13]:


#guardamos tanto entrenamiento como prueba en los respectivos csv 
#y el archivo de clase y su indice
train_df.to_csv('annotations.csv', index=False, header=None)
test_df.to_csv('annotations_test.csv', index=False, header=None)

classes = set(['Pituca'])

with open('classes.csv', 'w') as f:
    for i, line in enumerate(sorted(classes)):
        f.write('{},{}\n'.format(line,i))


# In[ ]:




