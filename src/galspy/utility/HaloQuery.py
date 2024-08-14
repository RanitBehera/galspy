import galspy.IO.MPGadget as mp
import galspy.IO.BigFile as bf
import numpy,os



class RSGQuery:
    def __init__(self,rsg_path:str) -> None:
        self.path = rsg_path
        RSG= mp.RSGRoot(rsg_path)
        self.halos = RSG.RKSHalos
        self.particles = RSG.RKSParticles

    def get_blobname(self,halo_id:int) -> str:
        """
        Gets blobname given as 'HaloID'.
        """
        data=bf.Column(self.path+os.sep+"RKSHalos/PP_HaloIDLinked").Read()
        data=data[numpy.argsort(data[:,0])]             # Sort and store in post-process?? That will filldle with blob wise.
        row = data[halo_id]
        if row[0]==halo_id:return "{:0X}".format(row[1]).rjust(6,'0')
        else:raise Exception("ERROR : row halo id not matching with given halo id.")

    def get_internal_halo_id(self,halo_id:int) -> int:
        """
        Gets 'InternalHaloID' given 'HaloID'.
        """
        data=bf.Column(self.path+os.sep+"RKSHalos/PP_HaloIDLinked").Read()
        data=data[numpy.argsort(data[:,0])]             # Sort and store in post-process?? That will filldle with blob wise.
        row = data[halo_id]
        if row[0]==halo_id:return row[2]
        else:raise Exception("ERROR : row halo id not matching with given halo id.")


    # def get_halo_id_of(self,internal_halo_id,blobname):
    #     if internal_halo_id<0:return None

    #     blob_halo_id = bf.Blob(os.path.join(self.halos.HaloID.path,blobname)).Read() 
    #     blob_inthalo_id = bf.Blob(os.path.join(self.halos.InternalHaloID.path,blobname)).Read() 
        
    #     halo_id = blob_halo_id[numpy.where(blob_inthalo_id==internal_halo_id)] 
    #     return halo_id[0]


    def get_massive_halos(self,number:int=10):
        virial_mass = self.halos.VirialMass()
        halo_ids = self.halos.HaloID()
        return numpy.array(halo_ids[numpy.argsort(virial_mass)[::-1]][:number])

    def get_child_halos_of(self,internal_halo_id,blobname,method="subof"):
        childs = []
        if method=="cochild":
            blob_ihid = bf.Blob(os.path.join(self.halos.InternalHaloID.path,blobname)).Read()
            blob_child = bf.Blob(os.path.join(self.halos.Child.path,blobname)).Read()
            blob_nextco = bf.Blob(os.path.join(self.halos.NextCochild.path,blobname)).Read()
            first_child = blob_child[blob_ihid==internal_halo_id][0]
            childs.append(first_child)
            while not childs[-1]==-1:
                next_child = blob_nextco[blob_ihid==childs[-1]][0]
                childs.append(next_child)
            return numpy.array(childs[:-1])
        
        if method=="subof":
            blob_subof = bf.Blob(os.path.join(self.halos.Sub_of.path,blobname)).Read()
            blob_ihid = bf.Blob(os.path.join(self.halos.InternalHaloID.path,blobname)).Read()
            childs = blob_ihid[blob_subof==internal_halo_id]
            return numpy.array(childs)


    def get_descendant_halos_of(self,internal_halo_id,blobname):
        descendants =[]
        descendants +=list(self.get_child_halos_of(internal_halo_id,blobname))
        for des in descendants:
            next_descendents = list(self.get_child_halos_of(des,blobname))
            if len(next_descendents) ==0: continue
            descendants +=next_descendents
        return numpy.array(descendants)
        
    
    def get_descendant_tree_of(self,internal_halo_id,blobname):
        def get_node_dict(ihid):
            childs = self.get_child_halos_of(ihid,blobname)
            if len(childs) == 0 : return None
            node_dict = {}
            for ch in childs:
                node_dict[ch]=get_node_dict(ch)
            return node_dict

        return {internal_halo_id:get_node_dict(internal_halo_id)}
        

    def get_parent_halo_of(self,internal_halo_id,blobname):
        blob_subof = bf.Blob(os.path.join(self.halos.Sub_of.path,blobname)).Read()
        blob_ihid = bf.Blob(os.path.join(self.halos.InternalHaloID.path,blobname)).Read()
        parent = blob_subof[blob_ihid==internal_halo_id]
        if len(parent)==0: return None
        if parent[0]==-1: return None
        return numpy.array(parent[0])

    def get_ancestor_track_of(self,internal_halo_id,blobname):
        blob_subof = bf.Blob(os.path.join(self.halos.Sub_of.path,blobname)).Read()

        # Method 1 : Slow but independent of ihid order
        # blob_ihid = bf.Blob(os.path.join(self.halos.InternalHaloID.path,blobname)).Read()
        # ancestors = [internal_halo_id]
        # while not ancestors[-1]==-1:
        #     ancestors+=list(blob_subof[blob_ihid==ancestors[-1]])

        # Method 1 : Fast but needs ihid to be order with zero based
        ancestors=[internal_halo_id]
        while not blob_subof[ancestors[-1]]==-1:
            ancestors+=[blob_subof[ancestors[-1]]]

        print(self.get_ancestor_origin(internal_halo_id,blobname))
        return numpy.array(ancestors)


    def get_ancestor_origin(self,internal_halo_id,blobname):
        blob_subof = bf.Blob(os.path.join(self.halos.Sub_of.path,blobname)).Read()

        # Using fast method of ancestor track with less memeory requirement
        prev_ancestor = internal_halo_id
        while not blob_subof[prev_ancestor]==-1:
            prev_ancestor=blob_subof[prev_ancestor]

        return prev_ancestor
    

    def check_if_valid_sub(self,ihids,blobname):
        hids = self.halos.HaloID(blobname)
        query_hids = hids[ihids]
        is_valid = (query_hids>=0)
        return is_valid






    def get_child_particle_rows(self,internal_halo_ids,blobname):
        blob_ihids,blob_pstart,blob_nump = bf.Blob(os.path.join(self.halos.PP_ParticleBlock.path,blobname)).Read().T
        pstart=[]
        nump=[]
        for i,blob_ihid in enumerate(blob_ihids):
            if blob_ihid not in internal_halo_ids: continue
            pstart.append(blob_pstart[i])
            nump.append(blob_nump[i])
        
        return numpy.column_stack((pstart,nump))
    
    def get_child_particle_positions(self,internal_halo_ids,blobname):
        rkspos = self.particles.Position(blobname)
        pstart,nump = self.get_child_particle_rows(internal_halo_ids,blobname).T
        pos = numpy.concatenate([rkspos[pstart[i]:pstart[i]+nump[i],:] for i in range(len(pstart))])
        return pos

    # def get_child_particle_types()

    def get_centre_position(self,internal_halo_id,blobname):
        cpos = self.halos.Position(blobname)
        return cpos[internal_halo_id]
    
    def get_virial_radius(self,internal_halo_id,blobname):
        vrad = self.halos.VirialRadius(blobname)
        return vrad[internal_halo_id]
    

    def get_position_offset(self,internal_halo_id,blobname):
        po = self.halos.PositionUncertainty(blobname)
        return po[internal_halo_id]
    
    def get_vmax_r(self,internal_halo_id,blobname):
        po = self.halos.vmax_r(blobname)
        return po[internal_halo_id]
    
    def get_peak_density_position(self,ihid,blobname):
        pass