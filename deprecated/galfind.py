import numpy as np
from galspy.utility.visualization import CubeVisualizer
from queue import Queue
import time

class SubFinder:
    def __init__(self,pos,vel):
        self._pos = pos
        self._vel = vel



    def _FOF3D(self,linking_length=0.2):
        # Find spans of the box
        x_span = np.max(self._pos[:,0])-np.min(self._pos[:,0])
        y_span = np.max(self._pos[:,1])-np.min(self._pos[:,1])
        z_span = np.max(self._pos[:,2])-np.min(self._pos[:,2])
        volume = x_span*y_span*z_span
        
        # Find average interparticle separation
        n_particles = len(self._pos)
        avg_vol = volume/n_particles
        avg_sep = avg_vol**(1/3)

        # Find linking length in terms of average separation
        linking_length = linking_length*avg_sep

        # FOF Grouping
        t0 = time.time()                         
        ids = np.array(np.arange(n_particles))
        
        id_grp=[]

        groups=np.zeros((len(self._pos),1)).tolist()
        particles=list(ids)
        b=1 # linking length
        while len(particles)>0:
            index = particles[0]
            # remove the particle from the particles list
            particles.remove(index)
            groups[index]=[index]
            # print("#N ", index)
            dr=np.sqrt(np.sum((self._pos-self._pos[index])**2,axis=1))
            id_to_look = list(np.where(dr<b)[0].tolist())
            id_to_look.remove(index)
            nlist = id_to_look
            # remove all the neighbors from the particles list
            for i in nlist:
                if (i in particles):
                    particles.remove(i)
            # print("--> neighbors", nlist)
            groups[index]=groups[index]+nlist
            new_nlist = nlist
            while len(new_nlist)>0:
                    index_n = new_nlist[0]
                    new_nlist.remove(index_n)
                    # print ("----> neigh", index_n)
                    dr=np.sqrt(np.sum((self._pos-self._pos[index_n])**2,axis=1))
                    id_to_look = np.where(dr<b)[0].tolist()
                    id_to_look = list(set(id_to_look) & set(particles))
                    nlist = id_to_look
                    if (len(nlist)==0):
                        # print ("No new neighbors found")
                        pass
                    else:
                        groups[index]=groups[index]+nlist
                        new_nlist=new_nlist+nlist
                        # print ("------> neigh-neigh", new_nlist)
                        for k in nlist:
                            particles.remove(k)




        te = time.time()                         
        print("Time taken: ", te-t0)

        print("Groups: ", groups)





        # cv = CubeVisualizer()
        # cv.add_points(self._pos )
        # cv.show()



    def find(linking_length=0.2):
        pass    
    
    def ROCKSTAR(self):
        pass








if __name__ == "__main__":
    import galspy
    SNAPSPATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS/"
    SNAPNUM=43
    ROOT=galspy.NavigationRoot(SNAPSPATH)
    star_pos = ROOT.PIG(SNAPNUM).Star.Position()
    star_vel = ROOT.PIG(SNAPNUM).Star.Velocity()
    star_gid = ROOT.PIG(SNAPNUM).Star.GroupID()
    mask=star_gid==1
    GF = SubFinder(star_pos[mask],star_vel[mask])
    GF._FOF3D()



















