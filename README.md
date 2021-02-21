# Remote Sensing(RS) Image Processing Tools                        
## A set of programs that are widely used in Remote Sensing image processing software 
*Pillow library used for Image Processing*
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
    Extracts and merges RGB components of an image(s).<br/>
    <br/>
    To run `RGB_extract` script:<br/>
    ```
    RGB_extract --input [input image path] --extension {jpg, png, tiff}
    ```
    **To run `RGB_merge` script:**<br/>
    ```
    RGB_merge --input [in directory path] --red [red band] --blue [blue band] --green [green band] --extension {jpg, png, tiff}
    ```
    <br/>
* **NDVI**<br/>
    Creates a b/w NDVI image using NIR and VIS bands.<br/>
    <br/>
    ![Example NDVI output](https://github.com/sum1lim/Remote_Sensing/blob/master/tests/test1/input_NDVI.png)
    <br/>
    **To run `NDVI` script:**<br/>
    ```
    NDVI --input [input directory path] --NIR [NIR band] --VIS [VIS band] --extension {jpg, png, tiff}
    ```
    <br/>
* **K-Means Classification**<br/>
    Classifies land covers using K-Means algorithm.<br/>
    <br/>
    ![Example K-Means output](https://github.com/sum1lim/Remote_Sensing/blob/master/tests/test2/input_KMeans.png)
    <br/>
    ![Example K-Means plot graph](https://github.com/sum1lim/Remote_Sensing/blob/master/tests/test2/input_KMeans_plot.png)
    <br/>
    **To run `K_Means` script:**<br/>
    ```
    K_Means --input [input directory path] --NIR [NIR band] --VIS [VIS band] --num_iterations [# iterations] --num_classes [# classes] --extension {jpt, png, tiff}
    ```
    <br/>
* **SOBEL Filter**<br/>
    Detects edges using SOBEL filter.<br/>
    <br/>
    ![Example SOBEL output](https://github.com/sum1lim/Remote_Sensing/blob/master/tests/test2/input_NDVI_SOBEL.png)
    <br/>
    **To run `SOBEL` script:**<br/>
    ```
    SOBEL --input [input image path] --extension {jpt, png, tiff}
    ```
