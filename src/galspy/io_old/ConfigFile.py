
class TextConfig:
    def __init__(self,path,sep_char='\n',comment_char='#') -> None:
        self.path   = path
        self.cmnt   = comment_char
        self.sep    = sep_char
    
    def GetAsDictionary(self):
        with open(self.path) as cfg:text = cfg.read()
        lines = text.split(self.sep)
        
        config_dict = {}
        for l in lines:
            if l=='':continue                       # Remove empty lines and comments
            l = l.strip()                           # Remove unwanted spaces
            if l.startswith(self.cmnt):continue     # Remove comments

            key,value = l.split('=')
            key,value = key.strip(),value.strip()

            config_dict[key]=value
        
        return config_dict


