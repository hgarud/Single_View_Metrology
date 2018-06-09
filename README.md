# Single_View_Metrology

## Requirements
* Python 3.6.2
* OpenCV 3.3.0
* [LabelMe](http://labelme.csail.mit.edu/Release3.0/)
* [view3dscene] (to view the 3D model)

## Abstract
Reconstruction of a 3 dimensional object/scene by computing necessary and sufficient aspects of the affine 3-D geometry of the object/scene in consideration.

## Methodology
A 3D scene captured using a pin-hole camera is characterized by the intrinsic and extrinsic parameters of the camera used. [This] blog is an excellent resource for a brief introduction on the pinhole camera parameters.

As per the available literature, the first step to reconstruct any scene is to estimate the camera parameters or the projection matrix of the pinhole camera.
The projection matrix, according to [Wikipedia], is a 3X4 matrix which describes the mapping of a pinhole camera from 3D points in the world to 2D points in an image.
In order to predict these parameters, we need vanishing points in all three coordinate axes. Vanishing points are calculated using the cross product of two "parallel" lines along each of the 3 coordinate axes. These lines were annotated using the LabelMe tool. Conversely, we can use extract parallel lines using Line Segment Detector(LSD), then apply RANSAC to further refine these lines to get better accuracy in estimating the vanishing points.
Using these and reference coordinates in the world coordinate system, we are able to estimate the camera projection matrix.

After we have the projection matrix, we extract affine homography planes for each X-Y, Y-Z, X-Z planes, apply this perspective transform to the original image and get three homography planes of the image.
Using view3dscene, we are able to stitch these three planes together to form 3D object.

### The original input image:
![alt text][input_image]

### The annotation interface to extract lines (LabelMe):
![alt text][anno_image]

### The homography planes after calculating the projection matrix:
#### XY:
![alt text][XY_image]

#### YZ:
![alt text][YZ_image]

#### XZ:
![alt text][XZ_image]

## References
* Criminisi, A., Reid, I. and Zisserman, A., 2000. Single view metrology. International Journal of Computer Vision, 40(2), pp.123-148.
* Fotouhi, M., Fouladi, S. and Kasaei, S., 2017. Projection matrix by orthogonal vanishing points. Multimedia Tools and Applications, 76(15), pp.16189-16223.

[view3dscene]: https://castle-engine.io/view3dscene.php
[This]: http://ksimek.github.io/2012/08/14/decompose/
[Wikipedia]: https://en.wikipedia.org/wiki/Camera_matrix
[input_image]: https://github.com/hgarud/Single_View_Metrology/blob/master/images/input/s8_test.jpg
[anno_image]: https://github.com/hgarud/Single_View_Metrology/blob/master/images/screenshot_labelme.png
[XY_image]: https://github.com/hgarud/Single_View_Metrology/blob/master/images/output/XY.JPG
[YZ_image]: https://github.com/hgarud/Single_View_Metrology/blob/master/images/output/YZ.JPG
[XZ_image]: https://github.com/hgarud/Single_View_Metrology/blob/master/images/output/XZ.JPG
