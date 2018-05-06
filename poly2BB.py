#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Forrest Edwards"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import xml.etree.ElementTree as ET
import glob
import os

def main(args):

    KITTI = {}
    if args.path[-1] != '/':
        args.path = args.path + '/'
    filelist = glob.glob(args.path + '*.xml')
    outputdir = args.path + "KITTI_txt"
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    for infile in filelist:
        tree = ET.parse(infile)
        root = tree.getroot()
        imgname = root.find('filename').text
        outfile = open(outputdir +"/" + imgname.split('.')[0] + '.txt', 'w')
        for obj in root.findall('object'):
            # labelme retains delted objects
            if obj.find('deleted').text == '1': continue
            poly = obj.find('polygon')
            xcoords =[]
            ycoords =[]
            for pt in poly.findall('pt'):
                xcoords.append(int(pt.find('x').text))
                ycoords.append(int(pt.find('y').text))
            
            if obj.find('occluded').text == 'yes':
                KITTI['occluded'] = '1'
            else: 
                KITTI['occluded'] = '0'
            
            KITTI['type']         =  obj.find('name').text
            KITTI['truncated']    =  '0.0'          
            KITTI['alpha']        =  '0.0'
            KITTI['left']         = min(xcoords)
            KITTI['right']        = max(xcoords)
            KITTI['top']          = min(ycoords)
            KITTI['bottom']       = max(ycoords)
            KITTI['height']       = '-1'
            KITTI['width']        = '-1'
            KITTI['length']       = '-1'
            KITTI['locx']         = '-1000'
            KITTI['locy']         = '-1000'
            KITTI['locz']         = '-1000'
            KITTI['roty']         = '-10'
            
            KITTIString = ""
            for key in ['type', 'truncated','occluded', 'alpha', 'left', 'right', 'top', 'bottom', 'height', 'width', 'length', 'locx', 'locy', 'locz', 'roty']:
                KITTIString += str(KITTI[key]) + " "
            outfile.write(KITTIString + "\n")
        outfile.close()
    print("\n%i xml files processed from %s" % (len(filelist), args.path))
    print("KITTI converted text files written to: %s\n" % outputdir)  
    
                    
if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("path", help="Parameter missing: Specify path to XML files")

    # Optional argument flag which defaults to False
    # parser.add_argument("-f", "--flag", action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    # parser.add_argument("-n", "--name", action="store", dest="name")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    #parser.add_argument(
    #    "-v",
    #    "--verbose",
    #    action="count",
    #    default=0,
    #    help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    #parser.add_argument(
    #    "--version",
    #    action="version",
    #    version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)

