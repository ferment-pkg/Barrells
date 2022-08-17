import os
import subprocess

from index import Barrells, Prebuild


class ninja(Barrells):
    def __init__(self):
        self.url = "https://github.com/ninja-build/ninja/archive/v1.10.2.tar.gz"
        self.description = "Small build system for use with gyp or CMake"
        self.git = False
        self.version = "1.10.2"
        self.homepage = "https://ninja-build.org/"
        self.prebuild = prebuild()
        self.caveats = "You may need to allow ninja to run in System Preferences > Security & Privacy"

    def install(self):
        os.chdir(self.cwd)
        subprocess.call(["python3", "configure.py", "--bootstrap",
                        "--with-python=python3"], cwd=self.cwd)
        subprocess.call(["pip", "install", "meson"], cwd=self.cwd)
        os.symlink(f"{self.cwd}/ninja", "/usr/local/bin/ninja")

    def uninstall(self) -> bool:
        try:
            os.remove("/usr/local/bin/ninja")
        finally:
            return super().uninstall()


class prebuild(Prebuild):
    def __init__(self):
        self.amd64 = "https://github.com/ferment-pkg/Barrells/releases/download/zip/ninja.tar.gz"
        self.arm64 = "https://github.com/ferment-pkg/Barrells/releases/download/zip/ninja.tar.gz"

    def install(self):
        os.chdir(self.cwd)
        subprocess.call(["pip", "install", "meson"], cwd=self.cwd)
        os.symlink(f"{self.cwd}/ninja", "/usr/local/bin/ninja")
        return super().install()
