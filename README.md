# Remote Sensing(RS) Image Processing Tools                        
## A set of programs that are widely used in Remote Sensing image processing software 
*Pillow library used for Image Processing*


### Packages & scripts <br/>
* **RGB**<br/>
    Extracts and merges RGB components of an image(s).<br/>
    <br/>
    To run `RGB_extract` script:<br/>
    ```
    RGB_extract --input input_image --extension {jpg, png, tiff}
    ```
    To run `RGB_merge` script:<br/>
    ```
    RGB_merge --input inDir --red red_band --blue blue_band --green green_band --extension {jpg, png, tiff}
    ```
    <br/>
* **NDVI**<br/>
    Creates a b/w NDVI image using NIR and VIS bands.<br/>
    <br/>
    To run `NDVI` script:<br/>
    ```
    NDVI --input inDir --NIR NIR_band --VIS VIS_band --extension {jpt, png, tiff}
    ```
    <br/>
* **K-Means classification**<br/>
    Classifies land covers using K-Means algorithm.<br/>
    <br/>
    To run `K_Means` script:<br/>
    ```
    K_Means --input inDir --NIR NIR_band --VIS VIS_band --iterations number_of_iterations --No_classes number_of_classes --extension {jpt, png, tiff}
    ```
