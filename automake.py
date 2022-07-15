import os
import subprocess
from time import sleep

from index import Barrells, Prebuild


class automake(Barrells):
    def __init__(self):
        self.url="https://ftp.gnu.org/gnu/automake/automake-1.14.tar.gz"
        self.git=False
        self.description="Automake -- Makefile generator"
        self.dependencies=["autoconf"]
    def install(self) -> bool:
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
    def test(self):
        subprocess.call(["automake","--version"])
    def uninstall(self) -> bool:
        try:
            os.chdir(self.cwd)
            subprocess.call(["make","uninstall"])
        finally:
            return super().uninstall()

