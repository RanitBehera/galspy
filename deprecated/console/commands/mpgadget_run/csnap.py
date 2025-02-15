import numpy as np
import galterm.ansi as ANSI
import os

class SnapManager:
    TAG_PRIMARY = 0
    TAG_SECONDARY = 1
    def __init__(self,snapshot_path:str) -> None:
        self.snapshot_path = snapshot_path
        self.scale_factor=np.array([])
        self.tag=np.array([])

    def _recalculate(self):
        primary = self.scale_factor[self.tag==SnapManager.TAG_PRIMARY]

        # Tag seconary snapshots as primary if its also in primary
        for i in range(len(self.scale_factor)):
            ai=self.scale_factor[i]
            ti=self.tag[i]
            if (ai in primary) and (ti==SnapManager.TAG_SECONDARY):
                self.tag[i]=SnapManager.TAG_PRIMARY

        _,uind = np.unique(np.round(self.scale_factor,9),return_index=True)
        self.scale_factor = self.scale_factor[uind]
        self.tag = self.tag[uind]

        order = np.argsort(self.scale_factor)
        self.scale_factor=self.scale_factor[order]
        self.tag = self.tag[order]

    def AppendScales(self,scales,primary:bool):
        self.scale_factor = np.concatenate((self.scale_factor,scales))
        if primary:tag = SnapManager.TAG_PRIMARY
        else: tag = SnapManager.TAG_SECONDARY
        self.tag = np.concatenate((self.tag,tag*np.ones(len(scales))))
        self._recalculate()

    def AddRedshiftsLinear(self,z1,z2,number,primary:bool=True):
        reds = np.linspace(z1,z2,number)
        self.AppendScales(1/(reds+1),primary)

    def AddRedshiftsLogarithimic(self,z1,z2,number,primary:bool=True):
        reds = np.logspace(np.log10(z1),np.log10(z2),number)
        self.AppendScales(1/(reds+1),primary)

    def AddScalesLinear(self,a1,a2,number,primary:bool=True):
        scales = np.linspace(a1,a2,number)
        self.AppendScales(scales,primary)
    
    def AddScalesLogarithimic(self,a1,a2,number,primary:bool=True):
        scales = np.logspace(np.log10(a1),np.log10(a2),number)
        self.AppendScales(scales,primary)

    def AddRedshifts(self,redshifts:list,primary:bool=True):
        z=np.array(redshifts)
        self.AppendScales(1/(z+1),primary)

    def AddScale(self,a:list,primary:bool=True):
        self.AppendScales(a,primary)


    def AvailableSnaps(self):
        childs = os.listdir(self.snapshot_path)
        dirs = [c for c in childs if os.path.isdir(os.path.join(self.snapshot_path,c))]
        PART = [d for d in dirs if d.startswith("PART")]
        PIG = [d for d in dirs if d.startswith("PIG")]
        
        PART_NUM = [int(p[5:]) for p in PART]
        PIG_NUM = [int(p[4:]) for p in PIG]
        
        self.avail_part=PART_NUM
        self.avail_pig=PIG_NUM

    def GetSnapTxtScaleFactors(self):
        snapshots_txt_path =os.path.join(self.snapshot_path,"Snapshots.txt")
        if os.path.exists(snapshots_txt_path):
            N,a = np.loadtxt(snapshots_txt_path).T
        else:
            N,a=[-1],[-1]
        return np.int32(N),a
        # TODO:handle when no or single row in snap.txt
        # return np.array(N,dtype=np.int32),np.array(a)



    def DisplayTable(self):
        CW=10
        print("#".ljust(4),'|',
              "Expected".center(CW),'|',
              "Output".center(CW),'|',
              "Redshift".center(CW),'|',
              "Available".center(CW+4),'|',
              "Priority".center(CW),'|',
              "Action")
  
        for i in range(len(self.scale_factor)):
            a=self.scale_factor[i]
            z=(1/a)-1
            tag = self.tag[i]

            Nc,ac = self.GetSnapTxtScaleFactors()

            COLOR = ANSI.DIM if i>= len(Nc) else ""

            # Snap Number
            print(COLOR+str(i).ljust(4),'|',end=ANSI.RESET+" ")

            # Expected Scale
            print(COLOR+f"{np.round(a,5)}".ljust(CW),'|',end=ANSI.RESET+" ")

            # Output Scale
            if i<len(Nc):
                COLOROK = ANSI.FG_GREEN if np.round(a,5)==np.round(ac[i],5) else ANSI.FG_MAGENTA
                print(COLOROK+f"{np.round(ac[i],5)}".ljust(CW)+ANSI.RESET,'|',end=" ")
            else:
                print(COLOR+"-".center(CW),'|',end=ANSI.RESET + " ")
            
            # Redshift
            print(COLOR+str(np.round(z,5)).ljust(CW),'|',end=ANSI.RESET+" ")

            # PART and/or PIG
            self.AvailableSnaps()
            avail=[]
            if i in self.avail_part:avail.append("PART")
            if i in self.avail_pig:avail.append("PIG")
            print(" + ".join(avail).center(CW+4),'|',end=" ")

            # Priority
            if tag==SnapManager.TAG_PRIMARY:
                print(ANSI.BOLD+"P".center(CW)+ANSI.RESET,'|',end=" ")
            elif tag==SnapManager.TAG_SECONDARY:
                print(ANSI.DIM+"S".center(CW)+ANSI.RESET,'|',end=" ")

            # Action
            if tag==SnapManager.TAG_SECONDARY:
                if i in self.avail_part and i in self.avail_pig:
                    print(ANSI.FG_YELLOW+f"DELETE PART_{i:03}"+ANSI.RESET,end="")
                elif i in self.avail_pig:
                    # print(ANSI.DIM+f"DELETED PART_{i:03}"+ANSI.RESET,end="")
                    pass
                else:
                    # print(f"DELETE PART_{i:03}",end="")
                    pass
            
            # New Line
            if i==len(Nc)-1:print("\n"+"-"*8*CW,end="")
            print("")

    def OutputScales(self):
        print(','.join([str(np.round(a,9)) for a in self.scale_factor]))


def main(env:dict):
    # L150N2040
    sm = SnapManager("/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS")
    sm.AddRedshifts([90,50,20])
    sm.AddRedshiftsLinear(15,0,31)
    sm.AddScale([0.0829092])
    sm.AddScalesLogarithimic(1/(11+1),1/(4+1),51,False)
    sm.AddScale([0.178876],False)
    

    # # L250N2040
    # sm = SnapManager("/mnt/home/student/cranit/NINJA/simulations/L250N2040/SNAPS")
    # sm.AddRedshifts([90,50,20])
    # sm.AddRedshiftsLinear(15,0,31)
    # sm.AddScalesLogarithimic(1/(11+1),1/(4+1),51,False)
    
    
    sm.DisplayTable()
    # sm.OutputScales()

if __name__=="__main__":
    main({})