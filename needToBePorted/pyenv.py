# Created With Barrell Tool https://ferment.tk/create
import os
import subprocess

from index import Barrells


class pyenv(Barrells):
    def __init__(self):
        self.description = "Simple Python Version Management: pyenv"
        self.url = "https://github.com/pyenv/pyenv.git"
        self.git = True
        self.version="2.3.2"
        self.lib = False
        self.dependencies = ["automake"]
        self.caveats="Run source ~/.zshrc to start using pyenv"

    def install(self):
        os.chdir(self.cwd)
        subprocess.call(["sh", "src/confugure"])
        subprocess.call(["make", "-C", "src"])
        self.editRC("#pyenv INIT - NO EDIT")
        self.SetPVar("PYENV_ROOT", self.cwd)
        self.EditPath("$PYENV_ROOT/bin")
        self.editRC('eval "$(pyenv init -)"')
        self.editRC("#pyenv EXIT - NO EDIT")
    def uninstall(self) -> bool:
        home=os.getenv("HOME")
        f=open(f"{home}/.zshrc", "r")
        f=f.read()
        content=f.split("\n")
        start=0
        endHash=0
        for index in range(len(content)):
            if content[index]=="#pyenv INIT - NO EDIT":
                start=index
            if content[index]=="#pyenv EXIT - NO EDIT":
                endHash=index
        if start==0 and endHash==0:
            return super().uninstall()
        #remove
        del content[start:endHash+1]
        f=open(f"{home}/.zshrc", "w")
        f.write("\n".join(content))
        return super().uninstall()


