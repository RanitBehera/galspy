import numpy
import pickle
import hoki
import hoki.load
import os
from galspec.bpass import BPASS



def cache(filepath,overwrite=False):
    # if os.path.isfile(filepath) and not overwrite:
    #     print("Using existing cache: \""+filepath +"\"")
    #     return
    
    print("Creating Cache ...")
    Z_foots=[1e-5,1e-4,1e-3,2e-3,3e-3,4e-3,6e-3,8e-3,1e-2,1.4e-2,2e-2,3e-2,4e-2]
    T_foots = numpy.arange(6,11.1,0.1)

    # Z_dict=dict(zip(Z_foots,range(len(Z_foots))))
    # T_dict=dict(zip(numpy.round(T_foots,1),range(len(T_foots))))

    spec_list=numpy.zeros((1+len(Z_foots)*len(T_foots),100000))
    
    for Zi,Z in enumerate(Z_foots):
        _BPASS = BPASS("CHABRIER_UPTO_300M","Binary",Z)
        table=_BPASS.Spectra.GetFlux().to_numpy()
        lam,aged_flux = table[:,0],table[:,1:].T
        for Ti,T in enumerate(T_foots):
            spec_index=1+(Zi*len(T_foots)+Ti)
            print(spec_index,"/",len(Z_foots)*len(T_foots))
        
            if spec_index==1:spec_list[0]=lam
            spec_list[spec_index]=aged_flux[Ti]

    print("Saving Pickle ...",flush=True)
    # Create folder if doesnot exist                #<----------
    with open(filepath,"wb") as fp: pickle.dump(spec_list,fp)

    print(f"Saved as \"{filepath}\"")   



cache("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM2/cache/specs.list")