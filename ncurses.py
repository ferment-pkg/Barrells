# Created With Barrell Tool https://ferment.tk/create
import subprocess
from index import Barrells
import os
import sys
class ncurses(Barrells):
    def __init__(self):
        self.description = "Ncurses"
        self.url = "https://ftp.gnu.org/pub/gnu/ncurses/ncurses-6.1.tar.gz"
        self.git = False
        self.lib = True
        self.dependencies = ["pkg-config"]
    
    def install(self):
        with open("/tmp/ncurses.log", "a") as sys.stdout:
            os.chdir(self.cwd)
            args=[f"--prefix={self.cwd}/built", "--enable-pc-files","--with-pkg-config-libdir=/usr/local/lib/pkgconfig", "--enable-sigwinch", "--enable-symlinks", "--enable-widec", "--with-shared",  "--with-cxx-shared","--with-gpm=no",  "--without-ada"]
            subprocess.run(["sh", "./configure", *args], stdout=sys.stdout, stderr=sys.stdout)
            subprocess.run(["make"], stdout=sys.stdout, stderr=sys.stdout)
            subprocess.run(["make", "install"], stdout=sys.stdout, stderr=sys.stdout)
            syms=os.listdir(self.cwd+"/built/bin")
            for sym in syms:
                os.symlink(self.cwd+"/built/bin/"+sym, f"/usr/local/bin/{sym}")
            os.symlink(f"{self.cwd}/built/include/ncursesw", "/usr/local/include/ncurses")
            syms=os.listdir(self.cwd+"/built/lib")
            for sym in syms:
                if(os.path.isdir(sym)):
                    continue
                os.symlink(self.cwd+"/built/lib/"+sym, f"/usr/local/lib/{sym}")
            syms=os.listdir(self.cwd+"/built/lib/pkgconfig")
            for sym in syms:
                os.symlink(self.cwd+"/built/lib/pkgconfig/"+sym, f"/usr/local/lib/pkgconfig/{sym}")
            return super().install()
    def uninstall(self):
        try:
            binsym=os.listdir(f"{self.cwd}/built/bin")
            libsyms=os.listdir(self.cwd+"/built/lib")
            pkgsyms=os.listdir(self.cwd+"/built/lib/pkgconfig")
            os.remove("/usr/local/include/ncursesw")
            for sym in binsym:
                os.remove(f"/usr/local/bin/{sym}")
            for sym in libsyms:
                os.remove(f"/usr/local/lib/{sym}")
            for sym in pkgsyms:
                os.remove(f"/usr/local/lib/pkgconfig/{sym}")
        finally:
            return super().uninstall()
    
