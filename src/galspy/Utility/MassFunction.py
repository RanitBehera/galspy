import numpy
from colossus.cosmology import cosmology
from colossus.lss import mass_function
from galspy.MPGadget import _PIG



# ===============================================
# --- BACK END
# ===============================================

def _mass_function_from_mass_list(Mass,VOLUME,bins):
    Mass = Mass[Mass!=0]
    # log10_Mass=numpy.log10(Mass)
    # Will exponent on e in front-end to get back mass, So no confilict with log10
    log_Mass=numpy.log(Mass)
    
    bin_count,bin_edges = numpy.histogram(Mass,bins=bins)
    bin_center = (bin_edges[1:]+bin_edges[:-1])/2
    bin_span = numpy.diff(bin_edges)
    bin_phi = bin_count / (bin_span * VOLUME)
    error=numpy.sqrt(bin_count)
    return bin_center,bin_phi,error



#https://bdiemer.bitbucket.io/colossus/lss_mass_function.html
# massFunction() takes input masses in M_solar/h. Reference: function documentation or doc string.
# It returns in in (Mpc/h)^3. Reference: Colossus Documantation basics  
def _mass_function_literature(sim_cosmology, model_name, redshift,mass_range,q_out,mdef="fof"):
    cosmology.setCosmology("my_cosmo",sim_cosmology)
    mass_func = mass_function.massFunction(mass_range, redshift, mdef = mdef, model = model_name, q_out = 'dndlnM')
    return mass_range,mass_func




# ===============================================
# --- FRONT END
# ===============================================
from typing import Literal

def MassFunction(mass_list,
                 box_size,
                 LogBinStep=0.5):
    
    volume = (box_size)**3
    log_M, dn_dlogM,error = _mass_function_from_mass_list(mass_list,volume,LogBinStep)
    M = numpy.exp(log_M)        # <-- Here taking e instead of 10, same as in backend
    return M,dn_dlogM,error


# -----------------------------------------------
user_to_colossus_model_name_map =  { 
                "Press-Schechter" : "press74",
                "Seith-Tormen"    : "sheth99",
                "Comparat(z=0)"   : "comparat17"
            }
user_to_colossus_qout_map =  { 
                "dn/dlnM" : "dndlnM",
                "(M2/rho0)*(dn/dm)"    : "M2dndM",
            }
LMF_OPTIONS = Literal["Press-Schechter","Seith-Tormen","Comparat(z=0)"]

def MassFunctionLiterature(
        model_name : LMF_OPTIONS,
        cosmology:dict,
        redshift,
        mass_range,
        output : Literal["dn/dlnM","(M2/rho0)*(dn/dm)"]
        ):
    model = user_to_colossus_model_name_map[model_name]
    q_out = user_to_colossus_qout_map[output]

    if model_name=="Comparat(z=0)":mdef = "vir"
    else:mdef="fof"


    return _mass_function_literature(cosmology, model,redshift,mass_range,q_out,mdef)


def CosmologyDict(isflat:bool,H0:float,Om0:float,Ob0:float,sig8:float,ns:float):
    return {'flat': isflat,'H0': H0,'Om0': Om0,'Ob0': Ob0,'sigma8': sig8,'ns': ns}

