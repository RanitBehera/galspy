import galspy.IO.MPGadget as mp
import galspy.IO.BigFile as bf
import numpy,os



class RockstarQuery:
    def __init__(self,rsg_path:str) -> None:
        self.path = rsg_path
        RSG= mp.RSGRoot(rsg_path)
        self.halos = RSG.RKSHalos
        self.particles = RSG.RKSParticles

    def get_blobname_of(self,halo_id:int) -> str:
        header = bf.Header(os.path.join(self.halos.path,"HaloID/header")).Read()
        del header["DTYPE"]        
        del header["NMEMB"]        
        del header["NFILE"]
        header = dict(sorted(header.items()))
        datalen = numpy.array([val for key,val in header.items()])
        datalen_cumsum = datalen.cumsum()
        for i,dl in enumerate(datalen_cumsum):
            if halo_id<dl:
                return ("{:X}".format(i)).upper().rjust(6,'0')
        
        print(f"Halo ID {halo_id} not in any blob.")
        return ""


    def get_internal_halo_id_of(self,halo_id:int):
        blobname = self.get_blobname_of(halo_id)
        internal_halo_id = self.halos.InternalHaloID()[halo_id]
        return internal_halo_id,blobname

    def get_halo_id_of(self,blobname,internal_halo_id):
        dt_halo_id = bf.Header(os.path.join(self.halos.path,"HaloID/header")).Read()["DTYPE"]
        dt_int_halo_id = bf.Header(os.path.join(self.halos.path,"InternalHaloID/header")).Read()["DTYPE"]

        blob_halo_id = bf.Blob(os.path.join(self.halos.HaloID.path,blobname),dt_halo_id).Read() 
        blob_inthalo_id = bf.Blob(os.path.join(self.halos.InternalHaloID.path,blobname),dt_int_halo_id).Read() 
        return blob_halo_id[numpy.where(blob_inthalo_id==internal_halo_id)]

    def get_massive_halos(self,number:int=10):
        virial_mass = self.halos.VirialMass()
        halo_ids = self.halos.HaloID()
        return numpy.array(halo_ids[numpy.argsort(virial_mass)[::-1]][:number])

    def _get_all_child_halos(self,hid):
        first_child = self.halos.Child()[hid]
        next_cochilds = self.halos.NextCochild()
        child_halos =[first_child]
        while not child_halos[-1] == -1:
            child_halos.append(next_cochilds[child_halos[-1]])
        print(child_halos)
        # return numpy.array(child_halos[:-1])

        
    def _get_all_descendant_halos(self,hid):
        first_child = self.halos.Child()[hid]
        next_cochilds = self.halos.NextCochild()
        child_halos =numpy.array([first_child])
        while not child_halos[-1] == -1:
            numpy.append(child_halos,next_cochilds[child_halos[-1]])
            numpy.concatenate((child_halos,self.get_all_descendant_halos(child_halos[-1])))
        # return numpy.array(child_halos[:-1])



    