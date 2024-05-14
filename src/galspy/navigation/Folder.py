import os

class _Folder:
    def __init__(self,path:str) -> None:
        self.path = path
        self.name = os.path.basename(self.path)
        self.parent_path = os.path.abspath(os.path.join(path, os.pardir))

    def Create(self):
        os.makedirs(self.path,exist_ok=True)
