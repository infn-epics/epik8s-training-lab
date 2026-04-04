# Camera bob

Description of the features of the Camera.bob display for General Camera interactions

## General Description 
This interface allows the user to show the output of a single camera and correctly interact with the ioc of the camera.
The box in the left top corner, allows users to choose the camera to control.
The other parts of the interface are basically two:

A tabs Container
A Screen with some control buttons

### The Screen
The screen section shows the current selected channel from the chosen camera.
It is possible to change the displayed channel via the "Image Selection" radiobutton group, choosing between:  
**RAW**  - The output from the camera just as it is  
**ROI**  - The camera image after a software ROI  
**PROCESSED** - The ROI image after various manipulation  
**REFERENCE** - A RAW version, in which it's possible to set a reference on the image  

The Settings button  will open a different display settings according to the selected channel.  
The Histogram button will open a new window, with the histogram page for the current channel.  

In the PROCESSED output, the button "CENTROID" allows the user to let calculate and show the centroid for the current image  
Below the screen is present a check box, that shows in the image a selection box used to apply a ROI or if REFERENCE is selected, to apply a reference

## The tabs Container
The tabs are 4:  
**Aquire** (the default one) It contains the tools for starting or stopping the camera.  
the regulation of exposure time and shutter time, the settings for the trigger and some other information  
**Save** This tab is used to save frames from the camera. It allows to set the path of the saved pictures and to take multiple picture in a row  
**Camera info**  This tab shows some info about the hardware of the camera  
**Links**   This tab collects the button links to more specified interfaces for expert users  

## Implementation  
The interface relies on several plugin that work at IOC level. Those plugins produce the four channels for the camera image and also the tiff generation  



```mermaid
graph LR
    Raw --> ROI
    ROI --> Processed
    Raw --> Overlay
    Raw --> TIFF1
    Raw --> CA1
    Raw --> PVA1
    ROI --> TIFF2
    ROI --> CA2
    ROI --> PVA2
    Processed --> CA3
    Processed --> PVA3
    Processed --> TIFF3
    Overlay --> CA4
    Overlay --> PVA4
    TIFF1[TIFF]
    TIFF2[TIFF]
    TIFF3[TIFF]
    CA1[CA]
    CA2[CA]
    CA3[CA]
    CA4[CA]
    PVA1[PVA]
    PVA2[PVA]
    PVA3[PVA]
    PVA4[PVA]




