import os
import subprocess

from index import Barrells, Prebuild


class autoconf(Barrells):
    def __init__(self):
        self.url="http://ftp.gnu.org/gnu/autoconf/autoconf-2.69.tar.gz"
        self.git=False
        self.version="2.69"
        self.description="Autoconf -- system configuration part of autotools"
        self.prebuild=prebuild()
    def install(self) -> bool:
        os.chdir(self.cwd)
        subprocess.call(["sh","configure", f"--prefix=/usr/local/"])
        subprocess.call(["make"])
        subprocess.call(["make","install"])
        return super().install()
    def uninstall(self) -> bool:
        os.chdir(self.cwd)
        subprocess.call(["make","uninstall"])
        return super().uninstall()
    def build(self)->bool:
        with open(f"{self.cwd}/autoconf-build.log", "a") as stdout:
            os.chdir(self.cwd)
            env=os.environ.copy()
            env["CC"]="clang"
            env["CXX"]="clang++"
            env["CFLAGS"]="-arch arm64 -arch x86_64"
            env["CXXFLAGS"]="-arch arm64 -arch x86_64"
            subprocess.call(["sh","configure", "--prefix=/usr/local/"], env=env, stdout=stdout, stderr=stdout)
            subprocess.call(["make", f"-j{os.cpu_count()}"], env=env, stdout=stdout, stderr=stdout)
class prebuild(Prebuild):
    def __init__(self):
        self.amd64="ferment://autoconf@autoconf.tar.gz"
        self.arm64="ferment://autoconf@autoconf.tar.gz"
    def install(self):
        os.chdir(self.cwd)
        self.removeTMPWaterMark("autoconf")
        subprocess.call(["make", "install", f"-j{os.cpu_count()}"])
