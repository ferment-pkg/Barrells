import os
import subprocess
import sys

from index import Barrells


class tldr(Barrells):
    def __init__(self):
        self.url="https://github.com/tldr-pages/tldr-c-client/archive/v1.4.3.tar.gz"
        self.git=False
        self.description= "Simplified and community-driven man pages"
        self.dependencies=["libzip", "pkg-config"]
        self.lib=True
    def install(self) -> bool:
        os.chdir(self.cwd)
        os.environ["PKG_CONFIG_PATH"]="/usr/local/lib/pkgconfig"
        subprocess.run(['make'])
        subprocess.run(['make','install'])
        return super().install()
    def uninstall(self) -> bool:
        try:
            os.remove("/usr/local/bin/tldr")
        finally:
            return super().uninstall()
    def build(self) -> bool:
        with open("/tmp/tldr.log", 'a') as sys.stdout:
            os.chdir(self.cwd)
            os.environ["PKG_CONFIG_PATH"]="/usr/local/lib/pkgconfig"
            subprocess.run(['make'], stdout=sys.stdout, stderr=sys.stdout)
