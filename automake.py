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
        self.prebuild=prebuild()
    def install(self) -> bool:
        os.chdir(self.cwd)
        os.environ["PERL"]="/usr/bin/perl"
        subprocess.run(["sh","./configure", f"--prefix=/usr/local"], timeout=1200)
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
    def build(self):
        with open(f"{self.cwd}/automake-build.log", "a") as stdout:
            os.chdir(self.cwd)
            env=os.environ.copy()
            env["CC"]="clang"
            env["CXX"]="clang++"
            env["CFLAGS"]="-arch arm64 -arch x86_64"
            env["CXXFLAGS"]="-arch arm64 -arch x86_64"
            env["PERL"]="/usr/bin/perl"
            subprocess.call(["sh","configure", "--prefix=/usr/local/"], env=env, stdout=stdout, stderr=stdout)
            subprocess.call(["make", f"-j{os.cpu_count()}"], env=env, stdout=stdout, stderr=stdout)

class prebuild(Prebuild):
    def __init__(self):
        self.amd64="ferment://automake@automake.tar.gz"
        self.arm64="ferment://automake@automake.tar.gz"
    def install(self):
        os.chdir(self.cwd)
        self.removeTMPWaterMark("automake")
        subprocess.call(["make", "install", f"-j{os.cpu_count()}"])
