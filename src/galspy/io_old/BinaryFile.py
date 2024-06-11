import os,sys,numpy
from typing import Literal

class _BinaryFile:
    def __init__(self,path:str,dtype:numpy.dtype) -> None:
        self.path = path
        self.dtype = dtype

    def Read(self):
        with open (self.path, mode='rb') as file:
            return numpy.fromfile(file,self.dtype)
    


# Seperate from class to avoid accidental writes
# Further safe-keeping by using "xb" mode instead of "wb" mode for file opening
def _WriteHeader(path,variable:numpy.ndarray,nfile=1):
    # Get DTYPE
    dt = str(variable.dtype)
    bo = sys.byteorder
    dtype = ""

    if bo=="little":dtype+="<"
    elif bo=="big":dtype+=">"
    else:dtype+="="
    
    if "int" in dt:dtype+="i" + str(int(int(dt[3:])/8))
    elif "float" in dt:dtype+="f" + str(int(int(dt[5:])/8))

    # Write Header
    header = ""
    header += "DTYPE: " + dtype + "\n"
    header += "NMEMB: " + str((variable.shape)[1]) + "\n"
    header += "NFILE: " + str(nfile) +"\n"

    header += "000000: " + str((variable.shape)[0]) + " : 0 : 0\n"
    with open(path,"w") as f:f.write(header)


def WriteField(path:str,fieldname:str,variable,mode:Literal["Overwrite","Skip"]="Skip"):
    # Validation
    path = path.strip()
    fieldname = fieldname.strip()
    variable = numpy.array(variable)
    if (len(variable.shape)==1):variable=variable.reshape(len(variable),1)
    elif (len(variable.shape)==0):variable=variable.reshape(1,1)

    file_dir = os.path.join(path, fieldname)
    os.makedirs(file_dir,exist_ok=True)
    try:
        if mode=="Skip":
            with open(file_dir + os.sep + "000000",'xb') as f: variable.tofile(f)
        elif mode=="Overwrite":
            with open(file_dir + os.sep + "000000",'wb') as f: variable.tofile(f)
    except FileExistsError:
        print("Following file already exist. Skipping writing data.")
        print(file_dir + os.sep + "000000")
    _WriteHeader(file_dir + os.sep + "header",variable)

