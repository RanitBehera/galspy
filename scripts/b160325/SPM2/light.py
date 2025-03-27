import galspy
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.ndimage import maximum_filter

from galspy.utility.visualization import CubeVisualizer
from scipy.ndimage import zoom

import cv2
import pickle




SNAPSPATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS/"
SNAPNUM=43
PIG = galspy.NavigationRoot(SNAPSPATH).PIG(SNAPNUM)
print("Reading ...")
all_star_gid  = PIG.Star.GroupID()
all_star_mass = PIG.Star.Mass()
all_star_pos  = PIG.Star.Position()
all_star_id   = PIG.Star.ID()
print("Done")



def PostProcess(img,convolve=True,mask_count=1):
    if convolve:
        kernel = np.array([[0.25,0.25],[0.25,0.25]])
        img = signal.convolve2d(img,kernel,"same")

    img = np.where(img>mask_count,img,0)

    img=np.log10(1+img)
    img=(img/np.max(img))**0.5
    
    return img #+ np.maximum(np.random.normal(0.1,0.04,img.shape),0)


def OpenCV(img):
    img = img.astype(np.uint8)
    # img = cv2.resize(img, tuple(2*np.array(img.T.shape)), interpolation=cv2.INTER_CUBIC)

    _, binary_image = cv2.threshold(img, 64, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(binary_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    label_map = -1*np.ones(binary_image.shape, dtype=int)

    ellipse_index = 0

    bgr_img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    for contour in contours:
        if len(contour) >= 5:  # Minimum 5 points are required to fit an ellipse
            ellipse = cv2.fitEllipse(contour)
            center, axes, angle = ellipse
            
            angle = -angle

            # Extract ellipse parameters
            center = (int(center[0]), int(center[1]))
            axes = (int(axes[0] / 2), int(axes[1] / 2))  # Half-length of the axes
            angle = angle  # Rotation angle of the ellipse


            cv2.ellipse(bgr_img, ellipse, (0, 0, 255), 1)

            major_axis_end = (int(center[0] + (axes[0]/2) * np.cos(np.deg2rad(angle))),
                                int(center[1] - (axes[0]/2) * np.sin(np.deg2rad(angle))))

            minor_axis_end = (int(center[0] - (axes[1]/2) * np.sin(np.deg2rad(angle))),
                                int(center[1] - (axes[1]/2) * np.cos(np.deg2rad(angle))))


            cv2.line(bgr_img, center, (major_axis_end), (0, 255, 0), 1)
            cv2.line(bgr_img, center, (minor_axis_end), (255, 0, 0), 1)



            text = f"{ellipse_index}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            color = (255, 0, 255)
            thickness = 1
            text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
            
            text_x = center[0] - text_size[0] // 2
            text_y = center[1] + text_size[1] // 2

            cv2.putText(bgr_img, text, (text_x, text_y), font, font_scale, color, thickness)





            # Get the bounding box of the ellipse
            min_x = center[0] - axes[0]
            max_x = center[0] + axes[0]
            min_y = center[1] - axes[1]
            max_y = center[1] + axes[1]

            # Loop over the bounding box and check if the pixel is inside the ellipse
            for y in range(min_y, max_y):
                for x in range(min_x, max_x):
                    # Ensure that the pixel is within image bounds
                    if 0 <= x < binary_image.shape[1] and 0 <= y < binary_image.shape[0]:
                        # Translate pixel coordinates relative to ellipse center
                        dx = x - center[0]
                        dy = y - center[1]
                        
                        # Ellipse equation (standard form)
                        if (dx**2 / axes[0]**2 + dy**2 / axes[1]**2) <= 1:
                            # Assign this pixel to the current ellipse
                            label_map[y, x] = ellipse_index

            # Increment ellipse index for the next ellipse
            ellipse_index += 1


    bgr_img = cv2.cvtColor(bgr_img,cv2.COLOR_BGR2RGB)


    return label_map,bgr_img,binary_image,ellipse_index



delta = 0.165*(1+7)*0.6736

def CheckPIG(tgid):
    gmask = all_star_gid==tgid
    tpos = all_star_pos[gmask]
    tid = all_star_id[gmask]
    tmass=all_star_mass[gmask]
    x,y,z=tpos.T
    x,y,z=x-np.min(x),y-np.min(y),z-np.min(z)
    sx,sy,sz=np.max(x),np.max(y),np.max(z)
    Nx,Ny,Nz=np.int64(sx/delta),np.int64(sy/delta),np.int64(sz/delta)

    hist_xy, xedges_xy, yedges_xy = np.histogram2d(x, y, bins=(Nx,Ny))
    hist_yz, yedges_yz, zedges_yz = np.histogram2d(y, z, bins=(Ny,Nz))
    hist_xz, xedges_xz, zedges_xz = np.histogram2d(x, z, bins=(Nx,Nz))
    

    img_xy = 255*PostProcess(hist_xy)
    img_yz = 255*PostProcess(hist_yz)
    img_xz = 255*PostProcess(hist_xz)

    img=img_xy

    label,ovrlay,binary,EC =OpenCV(img)

    ovrlay=np.transpose(ovrlay,(1,0,2))


    plt.imshow(ovrlay,origin="lower")
    # plt.imshow(binary.T,origin="lower",cmap="gist_gray")
    plt.title(f"N={EC}")
    plt.show()

    return

    unq_labels = np.unique(label)[1:]
    
    # print(unq_labels)


    dx=xedges_xy[1]-xedges_xy[0]
    dy=yedges_xy[1]-yedges_xy[0]
    xind = np.int32(x/dx)
    yind = np.int32(y/dy)

    xind=xind.clip(None,Nx-1)
    yind=yind.clip(None,Ny-1)

    id_list=[[] for ul in unq_labels]
    mass_list=[[] for ul in unq_labels]
    for xi,yi,pid,pmass in zip(xind,yind,tid,tmass):
        l = label[xi,yi]
        print(l)
        if l==-1:continue
        id_list[l].append(pid)
        mass_list[l].append(pmass)

    with open("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM2/cache/specindex.dict","rb") as fp:
        specindex = pickle.load(fp)

    with open("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM2/cache/specs.list","rb") as fp:
        speclist = pickle.load(fp)

    plt.figure()

    i=0
    for blob_id_list,blob_mass_list in zip(id_list,mass_list):
        tspecs=[speclist[specindex[ind]] for ind in blob_id_list]
        tspecs=np.array(tspecs)
        blob_mass_list=np.array(blob_mass_list)
        tspecs *=blob_mass_list[:,None]/1e-4
        print("mass :",np.sum(blob_mass_list))

        total=np.sum(tspecs.T,axis=1)

        # np.savetxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM2/data/testspec.txt",np.column_stack((speclist[0],total)))

        plt.plot(speclist[0],total,label=f"{i}")
        plt.xscale("log")
        plt.yscale("log")
        i=i+1
    

    plt.legend()
    plt.show()





for i in range(1,100):
    # if i!=1:continue
    # CheckPIG(i)
    try:
        print(i)
        CheckPIG(i)
    except:
        # CheckPIG(i)
        print("CHECK :",i)