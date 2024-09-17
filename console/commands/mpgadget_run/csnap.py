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


    def AvailableSnaps(self):
        childs = os.listdir(self.snapshot_path)
        dirs = [c for c in childs if os.path.isdir(os.path.join(self.snapshot_path,c))]
        PART = [d for d in dirs if d.startswith("PART")]
        PIG = [d for d in dirs if d.startswith("PIG")]
        
        PART_NUM = [int(p[5:]) for p in PART]
        PIG_NUM = [int(p[4:]) for p in PIG]
        
        self.avail_part=PART_NUM
        self.avail_pig=PIG_NUM

    def GetSnapScaleFactor(self):
        snapshots_txt_path =os.path.join(self.snapshot_path,"Snapshots.txt")
        N,a = np.loadtxt(snapshots_txt_path).T
        return np.int32(N),a



    def DisplayTable(self):
        CW=16
        print("#".ljust(8),'|',
              "Scale Factor".center(CW),'|',
              "Redshift".center(CW),'|',
              "Status".center(CW),'|',
              "Type".center(CW),'|',
              "Action")
  
        for i in range(len(self.scale_factor)):
            a=self.scale_factor[i]
            z=(1/a)-1
            tag = self.tag[i]

            Nc,ac = self.GetSnapScaleFactor()

            COLOR_PRE_i = ANSI.FG_MAGENTA
            COLOR_PRE_a = ANSI.FG_MAGENTA
            if i<len(Nc):
                if i==Nc[i]: COLOR_PRE_i=ANSI.FG_GREEN
                if np.round(a,5)==np.round(ac[i],5): COLOR_PRE_a=ANSI.FG_GREEN

            if i<len(Nc):        
                print(COLOR_PRE_i+str(i).ljust(8)+ANSI.RESET,'|',end=" ")
                print(COLOR_PRE_a+f"{np.round(a,5)}({np.round(ac[i],5)})".ljust(CW)+ANSI.RESET,'|',end=" ")
            else:
                print(str(i).ljust(8)+ANSI.RESET,'|',end=" ")
                print(str(np.round(a,5)).ljust(CW)+ANSI.RESET,'|',end=" ")

            print(str(np.round(z,5)).ljust(CW),'|',end=" ")

            # STATUS
            self.AvailableSnaps()
            status=[]
            if i in self.avail_part:status.append("PART")
            if i in self.avail_pig:status.append("PIG")
            print(" + ".join(status).center(CW),'|',end=" ")

            
            if tag==SnapManager.TAG_PRIMARY:
                print("PRIMARY".center(CW),'|',end=" ")
                print("")
            else:
                print("SECONDARY".center(CW),'|',end=" ")
                if i in self.avail_part:
                    print(ANSI.FG_YELLOW+f"DELETE PART_{i:03}"+ANSI.RESET)
                else:
                    print(f"DELETE PART_{i:03}")

    def OutputScales(self):
        print(','.join([str(np.round(a,9)) for a in self.scale_factor]))


def main(env:dict):
    sm = SnapManager("/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS")
    sm.AddRedshifts([90,50,20])
    sm.AddRedshiftsLinear(15,0,31)
    sm.AddRedshifts([11.06139])
    sm.AddScalesLogarithimic(1/(11+1),1/(4+1),51,False)

    sm.DisplayTable()
    # sm.OutputScales()

if __name__=="__main__":
    main({})