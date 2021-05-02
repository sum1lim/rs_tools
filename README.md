# Remote Sensing Image Processing Tools                        
## A set of programs that are widely used in Remote Sensing image processing software 
*Third-party Python Libraries used: [Pillow](https://pypi.org/project/Pillow/), [numpy](https://pypi.org/project/numpy/), [opencv-python](https://pypi.org/project/opencv-python/) and [scipy](https://pypi.org/project/scipy/)*
<br/><br/>
**To install packages:**
```
python -m venv venv
source venv/bin/activate
pip install .
```
<br/>

### Packages & scripts <br/>
* **RGB**<br/>
    Extracts and merges RGB components of images.<br/>
    <br/>
    To run `RGB_extract` script:<br/>
    ```
    RGB_extract --input [input image path] --extension {jpg, png, tiff}
    ```
    **To run `RGB_merge` script:**<br/>
    ```
    RGB_merge --input [input directory path] --red [red band] --blue [blue band] --green [green band] --extension {jpg, png, tiff}
    ```
    <br/>
* **NDVI**<br/>
    Creates a b/w NDVI image using NIR and VIS bands.<br/>
    **To run `NDVI` script:**<br/>
    ```
    NDVI --input [input directory path] --NIR [NIR band] --VIS [VIS band] --extension {jpg, png, tiff}
    ```
    <br/>
* **K-Means Classification**<br/>
    Classifies land covers using K-Means algorithm.<br/>
    **To run `K_Means` script:**<br/>
    ```
    K_Means --input [input directory path] --NIR [NIR band] --VIS [VIS band] --num_iterations [# iterations] --num_classes [# classes] --extension {jpt, png, tiff}
    ```
    <br/>
* **SOBEL Filter**<br/>
    Detects edges using SOBEL filter.<br/>
    **To run `SOBEL` script:**<br/>
    ```
    SOBEL --input [input image path] --extension {jpt, png, tiff}
    ```
