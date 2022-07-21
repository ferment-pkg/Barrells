# Created With Barrell Tool https://ferment.tk/create
import os
import subprocess

from index import Barrells


class pyenv(Barrells):
    def __init__(self):
        self.description = "Simple Python Version Management: pyenv"
        self.url = "https://github.com/pyenv/pyenv.git"
        self.git = True
        self.lib = False
        self.dependencies = ["automake"]

    def install(self):
        os.chdir(self.cwd)
        subprocess.call(["sh", "src/confugure"])
        subprocess.call(["make", "-C", "src"])
        self.SetPVar("PYENV_ROOT", self.cwd)
        self.EditPath("$PYENV_ROOT/bin")
        self.editRC("eval $(pyenv init -)")


