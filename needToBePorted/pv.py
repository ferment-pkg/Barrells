# Created With Barrell Tool https://ferment.tk/create
from index import Barrells


class pv(Barrells):
    def __init__(self):
        self.description = "Monitor data's progress through a pipe"
        self.url = "https://github.com/icetee/pv/archive/refs/tags/v1.6.6.tar.gz"
        self.git = False
        self.lib = False
        self.version="1.6.6"
        self.home = "https://www.ivarch.com/programs/pv.shtml"
        self.dependencies = ["automake", "pkg-config"]

    def install(self):
        import subprocess

        args = ["--prefix=/usr/local/", "--disable-nls"]
        import os

        os.chdir(self.cwd)
        subprocess.call(["sh", "./configure", *args])
        subprocess.call(["make"])
        subprocess.call(["make", "install"])
    def build(self):
        import subprocess
        args = ["--prefix=/usr/local/", "--disable-nls"]
        import os
        os.chdir(self.cwd)
        subprocess.call(["sh", "./configure", *args])
        subprocess.call(["make"])
    def uninstall(self):
        import os

        os.chdir(self.cwd)
        import subprocess

        subprocess.call(["make", "uninstall"])
