import os

def completion():
    oc = {"-o":None}
    return {
        "-t":oc,
        "--template":oc,
        "-p":oc,
        "--post-process":oc
    }

def help():pass

def main(env:dict,args:list[str]):
    if len(args)<1:return

    # Template generation
    if any(a in args for a in ("-t","--template")):
        pass
    
    # Post-Process
    if any(a in args for a in ("-p","--post-process")):
        # Get Directory
        search_dir  = ""
        if "-o" in args:
            o_index = args.index("-o")
            if o_index<len(args)-1:
                search_dir=args[o_index+1]
                if not os.path.exists(search_dir):
                    print(f"Serach directory {search_dir} doesnot exist.")
                    search_dir = ""
                if not os.path.isdir(search_dir):
                    print(f"Serach directory {search_dir} is not a directory!")
                    search_dir = ""
            else:
                print("No search directory given:")
        
        
        if search_dir=="":
            with_pwd = input("Proceed with current directory? [Y/n] :")
            print(with_pwd)
            if with_pwd.lower() in ["y",""]:search_dir = env["PWD"]
            else:return

        # Get Snaps to work with
        snap_list=[]
        if os.path.basename(search_dir).startswith("RSG_"):snap_list.append(search_dir)
        else:
            childs = os.listdir(search_dir)
            for c in childs:
                full_dir = os.path.join(search_dir,c)
                if os.path.isdir(full_dir) and os.path.basename(c).startswith("RSG_"):
                    snap_list.append(full_dir)
        
        if len(snap_list)==0:
            print(f"No snapshot found.:{search_dir}")
        else:
            print(f"Found {len(snap_list)} snapshots.")
        
        # Post-Process
        for snap in snap_list:
            _Process_Headers(snap)
            
                    


                    

        
def _Process_Headers(snap_path:str):
    childs = [os.path.join(snap_path,child) for child in os.listdir(snap_path) if os.path.isdir(os.path.join(snap_path,child))]
    for child in childs:
        grands = [os.path.join(child,grand) for grand in os.listdir(child) if os.path.isdir(os.path.join(child,grand))]
        for grand in grands:
            headers = [os.path.join(grand,head) for head in os.listdir(grand) if head.startswith("header_")]
            nfile = len(headers)
            if nfile==0:continue

            dtype_list = []
            nmemb_list = []
            datalen_list = []
            
            for head in headers:
                with open(head) as h:
                    text = h.read()
                    lines = text.split("\n")
                    dtype = lines[0].split(":")[1].strip()
                    nmemb = int(lines[1].split(":")[1].strip())
                    datalen = lines[2].strip()
                    dtype_list.append(dtype)
                    nmemb_list.append(nmemb)
                    datalen_list.append(datalen)

            # Crosscheck
            check_dtype = all(el==dtype_list[0] for el in dtype_list)
            check_nmemb = all(el==nmemb_list[0] for el in nmemb_list)

            if not check_dtype:
                print(f"CROSSCHECK ERROR : All dtypes are not same for {grand}")
                continue
            if not check_nmemb:
                print(f"CROSSCHECK ERROR : All nmembs are not same for {grand}")
                continue
            
            datalen_list.sort()

            with open(os.path.join(grand,"header"),"w") as fp:
                fp.write(f"DTYPE: {dtype_list[0]}\n")
                fp.write(f"NMEMB: {nmemb_list[0]}\n")
                fp.write(f"NFILE: {nfile}\n")
                for dl in datalen_list:
                    fp.write(dl+"\n")


            datalen_list.sort()

            for head in headers:
                os.remove(head)

