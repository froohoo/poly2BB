# poly2BB

Polygon to Bounding Box (poly2BB) is a tool for converting the XML annotations produced by MIT's [LabelMe Tool](http://labelme.csail.mit.edu "MIT Label Me") into the [KITTI](http://www.cvlibs.net/datasets/kitti/index.php "Karlsruhe Institute") annotation format. The KITTI format is used by the Nvidia Digits platform for training neural networks. 

## Requirements:
- Python
- wxPython (to run GUI version)

![screenshot](poly2BB.png)

## LabelMe Format

LabelMe annotations are stored as XML as an annotation element. I believe the intent is for LabelMe to enable multi-user functionaity for image annotation and thus each annotation element represents a the annotations of a unique user. Within the annotation element the tags are:
'''
 - filename:       name image file associated with this annotation
 - folder:         parent directory of image file on the LabelMe server
 - source:         user who made annotations
 - object:         an annotated object
 - imagesize:      image dimensions
 - object:         an annotated object within the image
 '''
 Each object contains n coordinates of a polygon (pt elements). Since the KITTI format only supports bounding boxes poly2BB defines the bounding box by extracting the largest and smallest x and y coordinates from the polygon. 

 ## KITTI Format
 Chart below from [https://github.com/NVIDIA/DIGITS/tree/master/digits/extensions/data/objectDetection](https://github.com/NVIDIA/DIGITS/tree/master/digits/extensions/data/objectDetection)
 '''
 #Values    Name      Description
----------------------------------------------------------------------------
   1    type         Describes the type of object: 'Car', 'Van', 'Truck',
                     'Pedestrian', 'Person_sitting', 'Cyclist', 'Tram',
                     'Misc' or 'DontCare'
   1    truncated    Float from 0 (non-truncated) to 1 (truncated), where
                     truncated refers to the object leaving image boundaries
   1    occluded     Integer (0,1,2,3) indicating occlusion state:
                     0 = fully visible, 1 = partly occluded
                     2 = largely occluded, 3 = unknown
   1    alpha        Observation angle of object, ranging [-pi..pi]
   4    bbox         2D bounding box of object in the image (0-based index):
                     contains left, top, right, bottom pixel coordinates
   3    dimensions   3D object dimensions: height, width, length (in meters)
   3    location     3D object location x,y,z in camera coordinates (in meters)
   1    rotation_y   Rotation ry around Y-axis in camera coordinates [-pi..pi]
   1    score        Only for results: Float, indicating confidence in
                     detection, needed for p/r curves, higher is better.
'''
