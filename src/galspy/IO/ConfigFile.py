
class TextConfig:
    def __init__(self,path,sep_char='\n',comment_char='#') -> None:
        self.path   = path
        self.cmnt   = comment_char
        self.sep    = sep_char
    
    def ReadAsDictionary(self):
        # Read text file.
        with open(self.path) as cfg:text = cfg.read()

        # Split into lines.
        lines = text.split(self.sep)

        # Prepare empty dictionary.
        config_dict = {}

        # For each lines
        for line in lines:
            # Remove unwanted space
            line = line.strip()

            # Filter out blank lines and full comments.
            if line=='' or line.startswith(self.cmnt):continue

            # Filter out the inline comments
            line = line.split(self.cmnt)[0].strip()

            # Form key-value pair.
            tokens  = line.split("=")
            key,value     = tokens[0].strip(),tokens[1].strip()

            # Cast to appropiate types
            # - String
            if value.startswith('"') and value.endswith('"'):value = str(value[1:-1])
            # - Integer : Not implemented
            # - Float : Not implemented
            
            # Fill the dictionary
            config_dict[key]=value
        
        return config_dict


