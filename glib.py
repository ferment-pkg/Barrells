# Created With Barrell Tool https://ferment.tk/create
import os
import subprocess
import sys
from index import Barrells
class glib(Barrells):
    def __init__(self):
        self.description = "Core application library for C"
        self.url = "https://gitlab.gnome.org/GNOME/glib.git"
        self.git = True
        self.lib = False
        self.dependencies = ["ninja"]
    
    def install(self):
        os.chdir(self.cwd)
        args=["--default-library=both", "-Diconv=auto", "-Dbsymbolic_functions=false", "-Ddtrace=false"]
        os.mkdir(f"{self.cwd}/build")
        os.chdir(f"{self.cwd}/build")
        subprocess.call(["meson", *args, ".."],stdout=sys.stdout, stderr=sys.stdout)
        subprocess.run(["ninja"],stdout=sys.stdout, stderr=sys.stdout)
        subprocess.run(["ninja", "install"],stdout=sys.stdout, stderr=sys.stdout)
        return super().install()
    def uninstall(self) -> bool:
        try:
            os.chdir(self.cwd)
            os.chdir("build")
            subprocess.call(["ninja", "uninstall"])
        finally:
            return super().uninstall()

