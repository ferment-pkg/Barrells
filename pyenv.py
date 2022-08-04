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

    def install(self):
        os.chdir(self.cwd)
        subprocess.call(["sh", "src/confugure"])
        subprocess.call(["make", "-C", "src"])
        self.editRC("#pyenv INIT - NO EDIT")
        self.SetPVar("PYENV_ROOT", self.cwd)
        self.EditPath("$PYENV_ROOT/bin")
        self.editRC("eval $(pyenv init -)")
        self.editRC("#pyenv EXIT - NO EDIT")
    def uninstall(self) -> bool:
        try:
            home=os.getenv("HOME")
            f=open(f"{home}/.zshrc", "r")
            f=f.read()
            content=f.split("\n")
            init:int
            exitHash:int
            for index in content:
                if content[index] =="#pyenv INIT - NO EDIT":
                    init=index
                    continue
                if content [index]=="#pyenv EXIT - NO EDIT":
                    exitHash=index
                    continue
            del content[init]
            del content[exitHash]
            f=open(f"{home}/.zshrc", "w")
            f.write(content)
        finally:
            return True
        self.editRC("eval $(pyenv init -")


