# Created With Barrell Tool https://ferment.tk/create
import os
import subprocess
import sys

from index import Barrells


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
            args=[f"--prefix=/usr/local/", "--enable-pc-files","--with-pkg-config-libdir=/usr/local/lib/pkgconfig", "--enable-sigwinch", "--enable-symlinks", "--enable-widec", "--with-shared",  "--with-cxx-shared","--with-gpm=no",  "--without-ada"]
            subprocess.run(["sh", "./configure", *args], stdout=sys.stdout, stderr=sys.stdout)
            subprocess.run(["make"], stdout=sys.stdout, stderr=sys.stdout)
            subprocess.run(["make", "install"], stdout=sys.stdout, stderr=sys.stdout)
            return super().install()
    def build(self):
        arm64args=["--host=x86_64-apple-darwin", "--build=arm-apple-darwin", "--with-build-cc"]
        args=[f"--prefix={self.cwd}", "--enable-pc-files","--with-pkg-config-libdir=/usr/local/lib/pkgconfig", "--enable-sigwinch", "--enable-symlinks", "--enable-widec", "--with-shared",  "--with-cxx-shared","--with-gpm=no",  "--without-ada"]


    def uninstall(self):
        try:
            os.chdir(self.cwd)
            subprocess.run(["make", "uninstall"])
        finally:
            return super().uninstall()

