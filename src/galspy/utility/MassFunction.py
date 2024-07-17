import numpy
from colossus.cosmology import cosmology
from colossus.lss import mass_function




# ===============================================
# --- BACK END
# ===============================================

def _mass_function_from_mass_list(Mass,VOLUME,LogBinStep):
    Mass = Mass[Mass!=0]
    
    # log10_Mass=numpy.log10(Mass)
    log_Mass=numpy.log(Mass)

    log_bin_start=numpy.floor(min(log_Mass))
    log_bin_end=numpy.ceil(max(log_Mass))

    BinCount=numpy.zeros(int((log_bin_end-log_bin_start)/LogBinStep))

    for lm in log_Mass:
        i=int((lm-log_bin_start)/LogBinStep)
        BinCount[i]+=1

    log_M=numpy.arange(log_bin_start,log_bin_end,LogBinStep)+(LogBinStep/2)
    dn_dlogM=BinCount/(VOLUME*LogBinStep)
    error=numpy.sqrt(BinCount)/(VOLUME*LogBinStep)

    return log_M,dn_dlogM,error


#https://bdiemer.bitbucket.io/colossus/lss_mass_function.html
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
    M = numpy.exp(log_M)
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
        cosmology,
        redshift,
        mass_range,
        output : Literal["dn/dlnM","(M2/rho0)*(dn/dm)"]
        ):
    model = user_to_colossus_model_name_map[model_name]
    q_out = user_to_colossus_qout_map[output]

    if model_name=="Comparat(z=0)":mdef = "vir"
    else:mdef="fof"


    return _mass_function_literature(cosmology, model,redshift,mass_range,q_out,mdef)