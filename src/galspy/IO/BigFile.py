import numpy, struct, os, sys
from typing import Literal
from multiprocessing import Pool


def Get_DTYPE(variable):
    variable = numpy.array(variable)
    dt = str(variable.dtype)
    bo = sys.byteorder
    dtype = ""
    if bo=="little":dtype+="<"
    elif bo=="big":dtype+=">"
    else:dtype+="="
    if "int" in dt:dtype+="i" + str(int(int(dt[3:])/8))
    elif "float" in dt:dtype+="f" + str(int(int(dt[5:])/8))
    return dtype




class Attribute:
    def __init__(self,path:str) -> None:
        self.path = path

    def Read(self,plain_text:bool=False):
        with open(self.path) as f: attr_v2=f.read()
        if plain_text:return attr_v2
        struct_dtype_map={'i4':'i','i8':'q','u4':'I','u8':'Q','f4':'f','f8':'d','S1':'c',}
        attr_v2_dict={}
        for line in attr_v2.split("\n"):
            if line=="":continue
            chunks      = line.split(" ")
            key         = chunks[0]
            endianess   = chunks[1][0]
            dtype       = chunks[1][1:]
            length      = int(chunks[2])
            fmt = endianess + struct_dtype_map[dtype]*length
            val = list(struct.unpack(fmt,bytes.fromhex(chunks[3])))
            if dtype=='S1':val=b''.join(val)#.decode("utf-8")
            if length==1:val=val[0]
            attr_v2_dict[key]= val
        return attr_v2_dict



class Header:
    def __init__(self,path:str) -> None:
        self.path = path

    def Read(self,plain_text:bool=False):
        with open(self.path) as f:header=f.read()
        if plain_text:return header
        lines = header.split("\n")
        header_dict={}
        header_dict["DTYPE"] = lines[0].split(" ")[1]
        header_dict["NMEMB"] = int(lines[1].split(":")[1])
        header_dict["NFILE"] = int(lines[2].split(":")[1])
        for i in range(3,len(lines)):
            if lines[i]=="":continue
            filename,rowlen,_,_=lines[i].split(":")
            header_dict[filename] = int(rowlen.strip())
        return header_dict
    

    def Write(self,data_column):
        filenames = [("{:X}".format(i)).upper().rjust(6,'0') for i in range(len(data_column))]
        
        # Per Blob
        pb_datalen = numpy.zeros(len(data_column),dtype=int)
        pb_nmemb   = numpy.zeros(len(data_column),dtype=int)
        for i,blob in enumerate(data_column):
            blob = numpy.array(blob)
            
            # These logic corrects shape representation (4,)->(4,1)
            if (len(blob.shape)==1):blob=blob.reshape(len(blob),1)
            elif (len(blob.shape)==0):blob=blob.reshape(1,1)

            pb_nmemb[i]     = blob.shape[-1] 
            pb_datalen[i]   = len(blob)
        
        if not all([nm==pb_nmemb[0] for nm in pb_nmemb]):
            print("WARNING : NMEMB in all blob are not same.\nNMEMB of first blob will be used in header.")

        header = ""
        header += f"DTYPE: {Get_DTYPE(data_column[0])}\n"
        header += f"NMEMB: {str(pb_nmemb[0])}\n"
        header += f"NFILE: {str(len(data_column))}\n"

        for i,fn in enumerate(filenames):
            header+= f"{filenames[i]}: {pb_datalen[i]} : :\n"

        with open(self.path,"w") as f:f.write(header)      
        


# -----------------------------------------------------
class Blob:
    def __init__(self,path:str) -> None:
        self.path   = path

    def Read(self):
        parent_dir  = os.path.abspath(os.path.join(self.path, os.pardir))
        blobname    = os.path.basename(self.path)
        header_path = os.path.join(parent_dir,"header")
        header      = Header(header_path).Read()
        dtype  = header["DTYPE"]
        nmemb  = header["NMEMB"]
        rowlen = header[blobname]
        with open(self.path,mode="rb") as file:
            blob_data = numpy.fromfile(file,dtype=dtype)
        if nmemb>1: blob_data = blob_data.reshape(rowlen,nmemb)
        return blob_data
            
        
    def Write(self,variable,mode:Literal["Overwrite","Skip"]="Skip"):
        # parent_dir  = os.path.abspath(os.path.join(self.path, os.pardir))
        # os.makedirs(parent_dir,exist_ok=True)

        variable = numpy.array(variable)

        try:
            if mode=="Skip":
                with open(self.path,'xb') as file: variable.tofile(file)
            elif mode=="Overwrite":
                with open(self.path,'wb') as file: variable.tofile(file)
        except FileExistsError:
            print("Following file already exist. Skipping writing data.")
            print(self.path)
        



# -----------------------------------------------------
class Column:
    def __init__(self,path:str) -> None:
        self.path = path
    
    def Read(self,blobnames:list[str]=None):
        if blobnames==None:
            nfile = Header(os.path.join(self.path,"header")).Read()["NFILE"]
            blobnames = [("{:X}".format(i)).upper().rjust(6,'0') for i in range(nfile)]
        
        column = numpy.concatenate([Blob(os.path.join(self.path,fn)).Read() for fn in blobnames])
        return column


    def Write(self,data_column:list[numpy.ndarray]|list[list],mode:Literal["Overwrite","Skip"]="Skip"):
        os.makedirs(self.path,exist_ok=True)

        filenames = [("{:X}".format(i)).upper().rjust(6,'0') for i in range(len(data_column))]
        
        for i,data_blob in enumerate(data_column):
            filepath = os.path.join(self.path,filenames[i])
            Blob(filepath).Write(data_blob,mode)

        # Headers
        head_path = os.path.join(self.path,"header") 
        if os.path.exists(head_path) and mode=="Skip":return
        Header(head_path).Write(data_column)      

            





    
