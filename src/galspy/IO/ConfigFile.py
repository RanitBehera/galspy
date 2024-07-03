import pathlib,ast


def ReadAsDictionary(filepath,sep_char='\n',comment_char='#'):
    # Check if file exists
    config_file = pathlib.Path(filepath)
    if not config_file.exists():
        raise FileExistsError(f'File "{filepath}" not found')

    # Read text file.
    with open(filepath) as cfg:text = cfg.read()

    # Split into lines.
    lines = text.split(sep_char)

    # Prepare empty dictionary.
    config_dict = {}

    # For each lines
    for line in lines:
        # Remove unwanted space
        line = line.strip()

        # Filter out blank lines and full comments.
        if line=='' or line.startswith(comment_char):continue

        # Filter out the inline comments
        line = line.split(comment_char)[0].strip()

        # Form key-value pair.
        tokens  = line.split("=")
        key,value     = tokens[0].strip(),tokens[1].strip()

        # Cast to appropiate types
        # - String
        if value.startswith('"') and value.endswith('"'):value = str(value[1:-1])
        # - Integer : Not implemented
        # - Float : Not implemented
        
        value = ast.literal_eval(value)

        # Fill the dictionary
        config_dict[key]=value
    
    return config_dict


def WriteFromDictionary(dict:dict,filepath:str,header:str="",header_char="#",overwrite=False):

    # Check if file exists
    config_file = pathlib.Path(filepath)
    if config_file.exists() and not overwrite:
        raise FileExistsError(f'File "{filepath}" already exists and overwrite is restricted')

    with open(filepath,'w') as f:
        # Header
        lines = header.split("\n")
        formatted_header =""
        for line in lines:
            if line=='':formatted_header +="\n"
            else: formatted_header+= '#' + line + '\n'
        
        f.write(formatted_header)

        # Dictionary
        for key,value in dict.items():
            if isinstance(value,str):value = "\""+value+"\""
            f.write(f'{key} = {str(value)}\n')

    



