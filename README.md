# poly2BB




Polygon to Bounding Box (poly2BB) is a tool for converting the XML annotations produced by MIT's [LabelMe Tool](http://labelme.csail.mit.edu "MIT Label Me") into the [KITTI](http://www.cvlibs.net/datasets/kitti/index.php "Karlsruhe Institute") annotation format. 

## Requirements:
- Python
- wxPython (to run GUI version)

![screenshot](poly2BB.png)

## LabelMe format

LabelMe annotations are stored as XML as an annotation element. I believe the intent is for LabelMe to enable multi-user functionaity for image annotation and thus each annotation element represents a the annotations created by a each user. Within the annotation element the tags are:

 - filename       name image file associated with this annotation
 - folder         parent directory of image file on the LabelMe server
 - source         user who made annotations
 - object         an annotated object
