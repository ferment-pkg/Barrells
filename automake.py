import os
import subprocess
from time import sleep
from index import Barrells
class automake(Barrells):
    def __init__(self):
        self.url="https://ftp.gnu.org/gnu/automake/automake-1.14.tar.gz"
        self.git=False
        self.description="Automake -- Makefile generator"
        self.dependencies=["autoconf"]
    def install(self) -> bool:
        os.chdir(self.cwd)
        os.environ["PERL"]="/usr/bin/perl"
        subprocess.run(["sh","./configure", f"--prefix=/usr/local"], timeout=1200)
        subprocess.call(["make"])
        subprocess.call(["make"])
        #wait a second for the make to finish
        sleep(1)
        subprocess.call(["make","install"], timeout=120)
        super().install()
    def uninstall(self) -> bool:
        try:
            os.chdir(self.cwd)
            subprocess.call(["make","uninstall"])
        finally:
            return super().uninstall()
