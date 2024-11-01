import galspy,numpy, os

PATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
root = galspy.NavigationRoot(PATH)

sfrd=[]
sfrd03=[]
z=[]
def GetSFRD(snap_num):
    sfr_gas = root.PART(snap_num).Gas.StarFormationRate()
    bsize   = root.PART(snap_num).Header.BoxSize()/1000
    vol     = bsize**3
    _sfrd   = numpy.sum(sfr_gas)/vol
    _sfrd03   = numpy.sum(sfr_gas[sfr_gas>0.3])/vol
    _z      = root.PART(snap_num).Header.Redshift()
    z.append(_z)
    sfrd.append(_sfrd)
    sfrd03.append(_sfrd03)

# Get All PARTS
parts  = [cld for cld in os.listdir(PATH) 
          if os.path.isdir(PATH+os.sep+cld) and cld.startswith("PART_")]
tot = len(parts)
for i,part in enumerate(parts):
    print(i+1,'/',tot)
    sn = int(part.removeprefix("PART_"))
    GetSFRD(sn)

sfrd = numpy.array(sfrd)
z = numpy.array(z)

sort = numpy.argsort(z)
z,sfrd = z[sort], sfrd[sort]

numpy.savetxt("study/hpc_proposal/sfrd_L150N2040.txt",numpy.column_stack([z,sfrd,sfrd03]),
              fmt="%.08f",header="z sfrd sfrd(>0.3) for L150N2040 in Mo/yr/(Mpc/h)^3")