# Created With Barrell Tool https://fermentpkg.tech/create
import os
import subprocess

from index import Barrells


class vde(Barrells):
    def __init__(self):
        self.description = "VDEv2: Virtual Distributed Ethernet."
        self.url = "https://github.com/virtualsquare/vde-2/archive/refs/tags/v2.3.3.tar.gz"
        self.git = False
        self.lib = True
        self.version="2.3.3"
        self.home = "https://github.com/virtualsquare/vde-2"
        self.dependencies = ["autoconf", "automake"]

    def install(self):
        os.chdir(self.cwd)
        subprocess.call(["sh", "./configure"])
        subprocess.call(["make", f"-j{os.cpu_count()}", "install"])

    def build(self):
        os.chdir(self.cwd)
        env = os.environ.copy()
        env["CC"] = "clang"
        env["CXX"] = "clang++"
        env["CFLAGS"] = "-arch arm64 -arch x86_64"
        env["CXXFLAGS"] = "-arch arm64 -arch x86_64"
        subprocess.call(
            ["sh", "./configure", "--prefix=/usr/local", "--disable-dependency-tracking"], env=env)
        subprocess.call(["make", f"-j{os.cpu_count()}"], env=env)
