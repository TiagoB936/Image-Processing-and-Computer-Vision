# This code is from authorship of Tiago Bachiega de Almeida
#
# It grabs a leaf infected with Asian Rust and tries to
# evaluate the degree of infection based on thresholds 
# inputed by the user and using K Means clustering.

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import utils
import cv2
from utils import infest_percent

# Image file's name
img_file = 'leaf_1.JPG'

# Number of clusters
n_clusters = 3

# Threshold o gray intensity for health and warning
thresh_health = 70
thresh_warning = 150

# Reads the image and coverts from opencv BGR to default RGB
image = cv2.imread(img_file)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

plt.figure()
plt.axis("off")
plt.imshow(image)

image = image.reshape((image.shape[0] * image.shape[1], 3))

# Apply the K Means
clt = KMeans(n_clusters = n_clusters)
clt.fit(image)

# build a histogram of clusters and then create a figure
# representing the number of pixels labeled to each color
hist = utils.centroid_histogram(clt)
bar = utils.plot_colors(hist, clt.cluster_centers_)

# Calculates the infestation status of the leaf
_ = infest_percent(hist, clt.cluster_centers_, thresh_health, thresh_warning)

# show our color bart
plt.figure()
plt.axis("off")
plt.imshow(bar)
plt.show()
