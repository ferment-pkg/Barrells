import os
import subprocess
from index import Barrells
class ninja(Barrells):
    def __init__(self):
        self.url="https://github.com/ninja-build/ninja/archive/v1.10.2.tar.gz"
        self.description="Small build system for use with gyp or CMake"
        self.git=False
        self.homepage="https://ninja-build.org/"
    def install(self):
        os.chdir(self.cwd)
        subprocess.call(["python3","configure.py","--bootstrap", "--with-python=python3"], cwd=self.cwd)
        subprocess.call(["pip", "install", "meson"], cwd=self.cwd)
        os.symlink(f"{self.cwd}/ninja", "/usr/local/bin/ninja")
    def uninstall(self) -> bool:
        try:
            os.remove("/usr/local/bin/ninja")
        finally:
            return super().uninstall()