# Remote Sensing Image Processing Tools                        
## rs-tools provides Python programs for Remote Sensing image processing. 
*Third-party Python Libraries used: [matplotlib](https://pypi.org/project/matplotlib/), [numpy](https://pypi.org/project/numpy/), [opencv-python](https://pypi.org/project/opencv-python/), [Pillow](https://pypi.org/project/Pillow/), [scikit-image](https://pypi.org/project/scikit-image/), [scikit-learn](https://pypi.org/project/scikit-learn/), [scipy](https://pypi.org/project/scipy/) and [tqdm](https://pypi.org/project/tqdm/)
**To install the package:**
```
python -m venv venv
source venv/bin/activate
pip install .
```

### Scripts 
* **ROI**
    Clips the Region of Interest (ROI) defined by `(left, right, top, bottom)` pixel coordinates from an input image. The `input path` may be either a directory or a file. The `flip` argument is used to flip the image left to right. If the coordinates are not pre-defined in the commandline, press `c` in the preview window and define the coordinates interactively. Erase the undesired parts in the image using the `e` key. Press `q` in the preview window if the clipped image is satisfied. 
    ```
    ROI --input [input path] --left [left coordinate] --right [right coordinate] --top [top coordinate] --bottom [bottom coordinate] --flip {True/False} --extension {jpg, png, tiff}
    ```


* **RGB_extract**
    Extracts RGB components from a True Colour Image (TCI).
    ```
    RGB_extract --input [input path] --red [red band name] --blue [blue band name] --green [green band name] --extension {jpg, png, tiff}
    ```
    
* **RGB_merge**
    Merges three grayscale images into a single TCI image.
    ```
    RGB_merge --input [input path] --red [red band (ex. B04)] --blue [blue band (ex. B03)] --green [green band (ex. B02)] --extension {jpg, png, tiff}
    ```
    
* **downscale**
    Downscales the image dimension. The `divisor` parameter determines the level of downscaling
    ```
    downscale --input [input path] --divisor [integer] --extension {jpg, png, tiff}
    ```
    
* **contrast**
    Enhances the contrast of a grayscale image.
    ```
    contrast --input [input path] --extension {jpg, png, tiff}
    ```
    
* **gaussian**
    Low-pass Guassian filter.
    ```
    gaussian --input [input path] --extension {jpg, png, tiff}
    ```
    
* **SOBEL**
    High-pass Sobel filter.
    ```
    SOBEL --input [input path] --extension {jpg, png, tiff}
    ```
    
* **NDVI**
    Calclates and creates a grayscale Normalized Difference Vegetation Index (NDVI) image using optical NIR and VIS band images.
    <em>NDVI = (NIR — VIS)/(NIR + VIS)</em> (Weier and Herring, 2000).
    ```
    NDVI --input [input directory path] --NIR [NIR band] --VIS [VIS band] --extension {jpg, png, tiff}
    ```
    
* **K_Means**
    Unsupervised K-Means classification. The module utilizes the `scikit-learn`'s `KMeans` function (Pedregosa et al. 2011)
    ```
    K_Means --input [input directory path] --features [spaced delimited list of feature names (ex. NIR VIS)] --num_classes [# classes] --extension {jpt, png, tiff}
    ```
    ![alt text](https://raw.githubusercontent.com/sum1lim/rs_tools/master/tests/optical/IMG_DATA_ROI_contrast_KMeans/B03_B08_KMeans.png)
    ![alt text](https://github.com/sum1lim/rs_tools/blob/master/tests/optical/IMG_DATA_ROI_contrast_KMeans/B03_B08_KMeans_plot.png)
    
* **GLCM**
    Generates GLCM products (entropy, energy, contrast, homogeneity and dissimilarity) following the methods suggested by Ressel et al. (2015).
    ```
    GLCM --input [input image path] --products [spaced delimited list of desired products] --window_size [GLCM window size] --extension {jpt, png, tiff}
    ```
    
### References
Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, D., Brucher, M., Perrot, M., & Duchesnay, E. (2011). Scikit-learn: Machine Learning in Python. <em>Journal of Machine Learning Research, 12</em>, 2825–2830.

Ressel, R., Frost, A., & Lehner, S. (2015). A neural network-based classification for sea ice types on X-band SAR images. <em>IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, 8</em>(7), 3672-3680.<br/><br/>
Weier, J., & Herring, D. (2000). Measuring vegetation (ndvi & evi). <em>NASA Earth Observatory, 20</em>. <br/><br/>
