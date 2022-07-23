import os
import subprocess

from index import Barrells


class go(Barrells):
    def __init__(self):
        self.url="https://go.dev/dl/go1.18.3.src.tar.gz"
        self.version="1.18.3"
        self.git=False
        self.description="Open source programming language to build simple/reliable/efficient software"
        self.license="BSD-3-Clause"
    def install(self) -> bool:
       subprocess.call(["sh", "all.bash"], cwd=self.cwd+"/src")
       self.EditPath(self.cwd+"/bin")
       return super().install()
