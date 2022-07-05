import os
import subprocess
import sys

from index import Barrells


class smartmontools(Barrells):
    def __init__(self):
        self.url='https://downloads.sourceforge.net/project/smartmontools/smartmontools/7.3/smartmontools-7.3.tar.gz'
        self.git=False
        self.description="smartmontools is a set of utilities to monitor hard drives and other storage devices."
        self.dependencies=["autoconf", "automake"]
    def install(self) -> bool:
        os.chdir(self.cwd)
        args=["--disable-dependency-tracking", "--with-savestates", "--with-attributelog"]
        subprocess.call(["sh","configure", f"--prefix=/usr/local/", *args])
        subprocess.call(["make"])
        subprocess.call(["make","install"])
        return super().install()
    def build(self) -> bool:
        with open("/tmp/fermenter/smartmontools/build.log", "a") as sys.stdout:
            os.chdir(self.cwd)
            args=["--disable-dependency-tracking", "--with-savestates", "--with-attributelog"]
            subprocess.call(["sh","configure", f"--prefix=/usr/local/", *args], stdout=sys.stdout, stderr=sys.stderr)
            subprocess.call(["make"], stdout=sys.stdout, stderr=sys.stderr)
    def uninstall(self) -> bool:
        try:
            os.chdir(self.cwd)
            subprocess.call(["make","uninstall"])
        finally:
            return super().uninstall()
    def test(self) -> bool:
        try:
            subprocess.call(["smartctl", "--version"])
            subprocess.call(["smartd", "--version"])
            return super().test()
        except:
            return False
