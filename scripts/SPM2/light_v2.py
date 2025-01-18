#%%
import galspy
import numpy as np
import astropy
from scipy.signal import convolve2d
from typing import Literal
import matplotlib.pyplot as plt
import cv2 as cv



class ClumpManager:
    def __init__(self,snapspath:str,snapnum:int,gid:int):
        self.snapspath = snapspath
        self.snapnum = snapnum
        self.gid = gid 
        if gid<1:
            raise ValueError("Group ID must be greter than or equal to 1.")

        PIG=galspy.NavigationRoot(snapspath).PIG(int(snapnum))
        self.PIG = PIG

        star_gid        = PIG.Star.GroupID()
        target_mask     = star_gid==gid

        self.position   = PIG.Star.Position()[target_mask]
        self.mass       = PIG.Star.Mass()[target_mask]
        self.ids        = PIG.Star.ID()[target_mask]

        self.pixel_resolution = self._GetPixelResolution(PIG.Header.Redshift())


    def _GetPixelResolution(self,z):
        RB = 0.031          #arcsecond per pixel : JWST 
        RB *= 1/3600        #degree per pixel
        RB *= np.pi/180     #radian per pixel
        sim = galspy.NavigationRoot(self.snapspath)
        cosmo=sim.GetAstropyFlatLCDM()
        DA=cosmo.angular_diameter_distance(z).value #in Mpc
        DA*=1000 #To Kpc
        res = DA * RB   #pKpc per pixel
        res *=(1+z)*self.PIG.Header.HubbleParam()   #cKpc per pixel
        return res
    

    def GetProjection(self,direction:Literal["XY","YZ","ZX"]="XY"):
        if direction not in ["XY","YZ","ZX"]:
            raise ValueError("Invalid Direction")

        x,y,z = self.position.T
        if direction=="XY": u,v = x,y
        elif direction=="YZ": u,v = y,z
        elif direction=="ZX": u,v = z,x

        begin_u,begin_v = np.min(u),np.min(v)
        end_u,end_v = np.max(u),np.max(v)
        # span_u,span_v = end_u-begin_u,end_v-begin_v

        pr = self.pixel_resolution
        bin_edges_u = np.arange(begin_u-0.5*pr,end_u+0.5*pr,pr)
        if bin_edges_u[-1]<end_u+0.5*pr:
            np.append(bin_edges_u,bin_edges_u[-1]+pr)
        bin_edges_v = np.arange(begin_v-0.5*pr,end_v+0.5*pr,pr)
        if bin_edges_v[-1]<end_v+0.5*pr:
            np.append(bin_edges_v,bin_edges_v[-1]+pr)

        height,uedges,vedges=np.histogram2d(u,v,bins=(bin_edges_u,bin_edges_v))
        return height


    def OpenCVPostProcess(self,img):
        # Foreground should be white and background should be black.
        
        # Propor Normalise
        max_count = np.max(img)
        norm_img = (255*(img/max_count))
        norm_img = img.astype(np.uint8)
        unit_count    = 255*(1/max_count)     # single star count normalised value

        # Binary
        _,binary = cv.threshold(norm_img,0,255,cv.THRESH_BINARY)
        _,binary_th = cv.threshold(norm_img,0*unit_count,255,cv.THRESH_BINARY)

        # Morphological Operations
        kernel = np.ones((2,2),np.uint8)
        closed = cv.morphologyEx(binary_th, cv.MORPH_CLOSE, kernel)
        kernel = np.ones((3,3),np.uint8)
        opened = cv.morphologyEx(closed, cv.MORPH_OPEN, kernel)

        # Ellipse Fitting
        fit_img = opened
        contours, hierarchy = cv.findContours(fit_img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        pixel_label_img = -1*np.ones(binary.shape, dtype=int)
        overlay_img = cv.cvtColor(fit_img,cv.COLOR_GRAY2BGR)
        ellipse_index = 0
        for contour in contours:
            # Minimum 5 points are required to fit an ellipse
            if len(contour)<5:continue
            ellipse = cv.fitEllipse(contour)
            
            # Extract ellipse parameters
            center, axes, angle = ellipse
            center = (int(center[0]), int(center[1]))
            axes = (int(axes[0] / 2), int(axes[1] / 2))
            angle = -angle

            major_axis_end = (int(center[0] + (axes[0])*np.cos(np.deg2rad(angle))),int(center[1] - (axes[0])*np.sin(np.deg2rad(angle))))
            minor_axis_end = (int(center[0] - (axes[1])*np.sin(np.deg2rad(angle))),int(center[1] - (axes[1])*np.cos(np.deg2rad(angle))))

            # Draw Overlays
            cv.ellipse(overlay_img, center,axes,-angle, 0,365,(0, 0, 255), 1)
            cv.line(overlay_img, center, (major_axis_end), (0, 255, 0), 1)
            cv.line(overlay_img, center, (minor_axis_end), (255, 0, 0), 1)


            ellipse_index += 1


        overlay_img = cv.cvtColor(overlay_img,cv.COLOR_BGR2RGB)


        return binary, binary_th, closed, opened,overlay_img



SNAPSPATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS/"


# %%
for i in range(1,100):
    if not i==5:continue
    print(i)
    cm = ClumpManager(SNAPSPATH,43,i)

    img=cm.GetProjection()

    ppimgs = cm.OpenCVPostProcess(img)


    # PLOT
    INTERACTIVE = True
    if INTERACTIVE:
        plt.figure()
        plt.imshow(img,cmap="grey")
        plt.title("Projection Original")

        plt.figure()
        plt.imshow(ppimgs[0],cmap="grey")
        plt.title(f"Binary")

        plt.figure()
        plt.imshow(ppimgs[1],cmap="grey")
        plt.title(f"Binary Thresold")

        plt.figure()
        plt.imshow(ppimgs[2],cmap="grey")
        plt.title(f"Morphological (Closed)")

        plt.figure()
        plt.imshow(ppimgs[3],cmap="grey")
        plt.title(f"Morphological (Opened)")

        plt.figure()
        plt.imshow(ppimgs[4])
        plt.title(f"Overlay")
    else:
        fig,axs = plt.subplots(2,4,figsize=(9,6))
        ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8 = axs[0,0],axs[0,1],axs[0,2],axs[0,3],axs[1,0],axs[1,1],axs[1,2],axs[1,3]

        ax1.imshow(img,cmap="grey")
        ax1.set_title("Projection Original")
    
        ax2.imshow(ppimgs[0],cmap="grey")
        ax2.set_title(f"Binary")

        ax3.imshow(ppimgs[1],cmap="grey")
        ax3.set_title(f"Binary Thresold")

        ax4.imshow(ppimgs[2],cmap="grey")
        ax4.set_title(f"Morphological (Closed)")

        ax5.imshow(ppimgs[3],cmap="grey")
        ax5.set_title(f"Morphological (Opened)")

        ax6.imshow(ppimgs[4],cmap="grey")
        ax6.set_title(f"Overlay")

        for ax in [ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8]:
            ax:plt.Axes
            ax.set_axis_off()


    # plt.tight_layout()
    plt.show()






# %%




# import galspy
# import numpy as np
# from scipy import signal
# import matplotlib.pyplot as plt
# from scipy.ndimage import maximum_filter

# from galspy.utility.visualization import CubeVisualizer
# from scipy.ndimage import zoom

# import cv
# import pickle


# SNAPSPATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS/"
# SNAPNUM=43
# PIG = galspy.NavigationRoot(SNAPSPATH).PIG(SNAPNUM)
# print("Reading ...")
# all_star_gid  = PIG.Star.GroupID()
# all_star_mass = PIG.Star.Mass()
# all_star_pos  = PIG.Star.Position()
# all_star_id   = PIG.Star.ID()
# print("Done")



# def PostProcess(img,convolve=True,mask_count=1):
#     if convolve:
#         kernel = np.array([[0.25,0.25],[0.25,0.25]])
#         img = signal.convolve2d(img,kernel,"same")

#     img = np.where(img>mask_count,img,0)

#     img=np.log10(1+img)
#     img=(img/np.max(img))**0.5
    
#     return img #+ np.maximum(np.random.normal(0.1,0.04,img.shape),0)


# def OpenCV(img):
#     img = img.astype(np.uint8)

#     _, binary_image = cv.threshold(img, 64, 255, cv.THRESH_BINARY)

#     contours, _ = cv.findContours(binary_image,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
#     print(contours)

#     # exit()


#     label_map = -1*np.ones(binary_image.shape, dtype=int)

#     ellipse_index = 0

#     bgr_img = cv.cvtColor(img,cv.COLOR_GRAY2BGR)

#     for contour in contours:
#         if len(contour) >= 5:  # Minimum 5 points are required to fit an ellipse
#             print("\tEI",ellipse_index)
#             # print("\t",contour)
#             ellipse = cv.fitEllipse(contour)
#             print(ellipse)
#             center, axes, angle = ellipse
            
#             angle = -angle

#             # Extract ellipse parameters
#             center = (int(center[0]), int(center[1]))
#             axes = (int(axes[0] / 2), int(axes[1] / 2))  # Half-length of the axes
#             angle = angle  # Rotation angle of the ellipse

#             # print(axes)
#             axes=tuple(np.array(axes)+10)
#             if axes[0]<2 or axes[1]<2:continue

#             # cv.ellipse(bgr_img, ellipse, (0, 0, 255), 1)
#             cv.ellipse(bgr_img, center,axes,-angle, 0,365,(0, 0, 255), 1)

#             major_axis_end = (int(center[0] + (axes[0]) * np.cos(np.deg2rad(angle))),
#                                 int(center[1] - (axes[0]) * np.sin(np.deg2rad(angle))))

#             minor_axis_end = (int(center[0] - (axes[1]) * np.sin(np.deg2rad(angle))),
#                                 int(center[1] - (axes[1]) * np.cos(np.deg2rad(angle))))


#             cv.line(bgr_img, center, (major_axis_end), (0, 255, 0), 1)
#             cv.line(bgr_img, center, (minor_axis_end), (255, 0, 0), 1)



#             text = f"{ellipse_index}"
#             font = cv.FONT_HERSHEY_SIMPLEX
#             font_scale = 0.5
#             color = (255, 0, 255)
#             thickness = 1
#             text_size = cv.getTextSize(text, font, font_scale, thickness)[0]
            
#             text_x = center[0] - text_size[0] // 2
#             text_y = center[1] + text_size[1] // 2

#             cv.putText(bgr_img, text, (text_x, text_y), font, font_scale, color, thickness)





#             # Get the bounding box of the ellipse
#             min_x = center[0] - axes[0]
#             max_x = center[0] + axes[0]
#             min_y = center[1] - axes[1]
#             max_y = center[1] + axes[1]

#             # Loop over the bounding box and check if the pixel is inside the ellipse
#             for y in range(min_y, max_y):
#                 for x in range(min_x, max_x):
#                     # Ensure that the pixel is within image bounds
#                     if 0 <= x < binary_image.shape[1] and 0 <= y < binary_image.shape[0]:
#                         # Translate pixel coordinates relative to ellipse center
#                         dx = x - center[0]
#                         dy = y - center[1]
                        
#                         # Ellipse equation (standard form)
#                         if (dx**2 / axes[0]**2 + dy**2 / axes[1]**2) <= 1:
#                             # Assign this pixel to the current ellipse
#                             label_map[y, x] = ellipse_index

#             # Increment ellipse index for the next ellipse
#             ellipse_index += 1
#             print("\tPassed")



#     bgr_img = cv.cvtColor(bgr_img,cv.COLOR_BGR2RGB)


#     return label_map,bgr_img,binary_image,ellipse_index



# delta = 0.165*(1+7)*0.6736

# def CheckPIG(tgid):
#     gmask = all_star_gid==tgid
#     tpos = all_star_pos[gmask]
#     tid = all_star_id[gmask]
#     tmass=all_star_mass[gmask]
#     x,y,z=tpos.T
#     x,y,z=x-np.min(x),y-np.min(y),z-np.min(z)
#     sx,sy,sz=np.max(x),np.max(y),np.max(z)
#     Nx,Ny,Nz=np.int64(sx/delta),np.int64(sy/delta),np.int64(sz/delta)

#     hist_xy, xedges_xy, yedges_xy = np.histogram2d(x, y, bins=(Nx,Ny))
#     hist_yz, yedges_yz, zedges_yz = np.histogram2d(y, z, bins=(Ny,Nz))
#     hist_xz, xedges_xz, zedges_xz = np.histogram2d(x, z, bins=(Nx,Nz))
    

#     img_xy = 255*PostProcess(hist_xy)
#     img_yz = 255*PostProcess(hist_yz)
#     img_xz = 255*PostProcess(hist_xz)

#     img=img_xy

#     label,ovrlay,binary,EC =OpenCV(img)

#     ovrlay=np.transpose(ovrlay,(1,0,2))


#     plt.imshow(ovrlay,origin="lower")
#     # plt.imshow(binary.T,origin="lower",cmap="gist_gray")
#     plt.title(f"N={EC}")
#     plt.show()

#     return

#     unq_labels = np.unique(label)[1:]
    
#     # print(unq_labels)


#     dx=xedges_xy[1]-xedges_xy[0]
#     dy=yedges_xy[1]-yedges_xy[0]
#     xind = np.int32(x/dx)
#     yind = np.int32(y/dy)

#     xind=xind.clip(None,Nx-1)
#     yind=yind.clip(None,Ny-1)

#     id_list=[[] for ul in unq_labels]
#     mass_list=[[] for ul in unq_labels]
#     for xi,yi,pid,pmass in zip(xind,yind,tid,tmass):
#         l = label[xi,yi]
#         print(l)
#         if l==-1:continue
#         id_list[l].append(pid)
#         mass_list[l].append(pmass)

#     with open("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM2/cache/specindex.dict","rb") as fp:
#         specindex = pickle.load(fp)

#     with open("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM2/cache/specs.list","rb") as fp:
#         speclist = pickle.load(fp)

#     plt.figure()

#     i=0
#     for blob_id_list,blob_mass_list in zip(id_list,mass_list):
#         tspecs=[speclist[specindex[ind]] for ind in blob_id_list]
#         tspecs=np.array(tspecs)
#         blob_mass_list=np.array(blob_mass_list)
#         tspecs *=blob_mass_list[:,None]/1e-4
#         print("mass :",np.sum(blob_mass_list))

#         total=np.sum(tspecs.T,axis=1)

#         # np.savetxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM2/data/testspec.txt",np.column_stack((speclist[0],total)))

#         plt.plot(speclist[0],total,label=f"{i}")
#         plt.xscale("log")
#         plt.yscale("log")
#         i=i+1
    

#     plt.legend()
#     plt.show()





# for i in range(1,100):
#     print(i)
#     if i!=1:continue
#     CheckPIG(i)
#     # try:
#     #     CheckPIG(i)
#     # except:
#     #     # CheckPIG(i)
#     #     print("CHECK :",i)
# %%
