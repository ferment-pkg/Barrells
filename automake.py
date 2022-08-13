import os
import subprocess
from time import sleep

from index import Barrells, Prebuild


class automake(Barrells):
    def __init__(self):
        self.url="https://ftp.gnu.org/gnu/automake/automake-1.14.tar.gz"
        self.git=False
        self.version="1.14"
        self.description="Automake -- Makefile generator"
        self.dependencies=["autoconf"]
    def install(self):
        with open(f"{self.cwd}/automake-build.log", "a") as f:
            os.chdir(self.cwd)
            env=os.environ.copy()
            env["CC"]="clang"
            env["CXX"]="clang++"
            subprocess.call(["sh","./configure", f"--prefix=/usr/local"], stdout=f, stderr=f, env=env)
            sleep(1)
            subprocess.call(["make"], stdout=f, stderr=f)
            subprocess.call(["make","install"],stdout=f, stderr=f)
            super().install()
    def test(self)->bool:
        st=subprocess.check_call(["which","automake"])
        if st > 0:
            print("False")
            return False
        print("True")
        return True
    def uninstall(self) -> bool:
        try:
            os.chdir(self.cwd)
            subprocess.call(["make","uninstall"])
        finally:
            return super().uninstall()

