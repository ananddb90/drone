#---------------------------------------------------------------------
# current implementation with discreate steps for zooming
# can be improved by linear linear steps for zooming
# for linear zooming, increment factor would be 0.1
#---------------------------------------------------------------------
import cv2
import numpy as np
import pdb
from numpy import random
from scipy.spatial import distance
import math

img = cv2.imread('car1.jpg',-1)
[h,w,c]= img.shape
origin = [w/2,h/2]
total_area = w*h
bbox = (120,30, 40,80)
# ROI details (x, y, w, h)
[roi_w, roi_h] = [bbox[2], bbox[3]]
roi_c = [bbox[0]+roi_w/2, bbox[1]+roi_h/2]
roi_area = roi_w * roi_h
ratio = total_area/roi_area
c_ref = np.array(origin)
zoom = 1	#initial frame
zoom_max = 4	#maximum allowed zoom 4x
im_crop = img[:,:]


def zoom_func(total_area, roi_w, roi_h, roi_c, roi_area, ratio, c_ref, zoom, zoom_max, im_crop):
    print ratio
    while (ratio >= 8):
        #-----------------------------------------------------
        # Zoom by factor of 2 (GP)
        # a_n = a_0*r**(n-1)
        #-----------------------------------------------------
        pdb.set_trace()
        zoom += 1
        factor = 2**(zoom-1)
        # clock wise block numbering starting from lefttop c1->c2->c3->c4
        c1 = np.array([c_ref[0] - c_ref[0]/factor, c_ref[1] - c_ref[1]/factor])
        c2 = np.array([c_ref[0] + c_ref[0]/factor, c_ref[1] - c_ref[1]/factor])
        c3 = np.array([c_ref[0] + c_ref[0]/factor, c_ref[1] + c_ref[1]/factor])
        c4 = np.array([c_ref[0] - c_ref[0]/factor, c_ref[1] + c_ref[1]/factor])
        c_list = np.array([c1,c2,c3,c4])
        c_id = distance.cdist([roi_c],c_list).argmin()
        
        # copy the new block into im_crop to zoom
        if (c_id == 0):
            im_crop = im_crop[0:2*c1[0], 0:2*c1[1]]
        elif (c_id == 1):
            im_crop = im_crop[c_ref[0]:2*c2[0], 0:2*c2[1]]
        elif (c_id == 2):
            im_crop = im_crop[c_ref[0]:2*c3[0], c_ref[1]:2*c3[1]]
        else:
            im_crop = im_crop[c_ref[0]:2*c4[0], c_ref[1]:2*c4[1]]
        
        # copy the center of block as new reference to zoom in
        c_ref = c_list[c_id]
        new_area = total_area/(2**zoom)
        ratio = new_area/roi_area
        
        if (zoom == zoom_max):
            print "maximum allowed zoom reached"
            break
	return im_crop

def main():
    return zoom_func(total_area, roi_w, roi_h, roi_c, roi_area, ratio, c_ref, zoom, zoom_max, im_crop)

if __name__ == '__main__' :
    im_crop = main()
    pdb.set_trace()
    print zoom
    #cv2.circle(img,(w/2,h/2), 2, (0,0,255), 2)
    res= cv2.resize(im_crop,(img.shape[1], img.shape[0]), interpolation = cv2.INTER_LANCZOS4)
    cv2.imshow("zoom",res)
    cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[0]+bbox[2], bbox[1]+bbox[3]), (255,0,0), 2)
    cv2.imshow("original",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


	
