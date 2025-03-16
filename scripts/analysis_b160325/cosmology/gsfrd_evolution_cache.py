import galspy,numpy, os

PATH = "/mnt/home/student/cranit/NINJA/simulations/L250N2040/SNAPS"
root = galspy.NavigationRoot(PATH)

z=[]
sfrd=[]
sfrdhalo03=[]
def GetSFRD(snap_num):
    bsize   = root.PART(snap_num).Header.BoxSize()/1000
    sfr_gas = root.PART(snap_num).Gas.StarFormationRate()
    vol     = bsize**3
    _sfrd   = numpy.sum(sfr_gas)/vol
    _z      = root.PART(snap_num).Header.Redshift()
    z.append(_z)
    sfrd.append(_sfrd)
    sfrhalo   = root.PIG(snap_num).FOFGroups.StarFormationRate()
    _sfrdhalo03 = numpy.sum((sfrhalo[sfrhalo>0.3]))/vol
    sfrdhalo03.append(_sfrdhalo03)


# Get All PARTS
parts  = [cld for cld in os.listdir(PATH) 
          if os.path.isdir(PATH+os.sep+cld) and cld.startswith("PART_")]
tot = len(parts)
for i,part in enumerate(parts):
    print(i+1,'/',tot)
    sn = int(part.removeprefix("PART_"))
    Z = root.PART(sn).Header.Redshift()
    if Z>18:continue
    GetSFRD(sn)

z = numpy.array(z)
sfrd = numpy.array(sfrd)
sfrd03 = numpy.array(sfrdhalo03)

sort = numpy.argsort(z)
z,sfrd,sfrd03 = z[sort], sfrd[sort],sfrd03[sort]

numpy.savetxt("study/hpc_proposal/sfrd_L250N2040.txt",numpy.column_stack([z,sfrd,sfrd03]),
              fmt="%.08f",header="z sfrd sfrdhalo(>0.3) for L250N2040 in Mo/yr/(Mpc/h)^3")