# Created With Barrell Tool https://fermentpkg.tech/create
import os
import subprocess

from index import Barrells, Prebuild, universalbinaryenv


class jq(Barrells):
    def __init__(self):
        self.description = "Lightweight and flexible command-line JSON processor"
        self.url = "https://github.com/stedolan/jq/releases/download/jq-1.6/jq-1.6.tar.gz"
        self.git = False
        self.lib = False
        self.home = "https://stedolan.github.io/jq/"
        self.dependencies = ["oniguruma", ":autoconf", ":automake"]
        self.version = "1.6"
        self.prebuild = prebuild()

    def install(self) -> bool:
        os.chdir(self.cwd)
        subprocess.call(["bash", "configure"])
        subprocess.call(["make", "install", f"-j{os.cpu_count()*1.5}"])
        return super().install()

    def uninstall(self) -> bool:
        os.chdir(self.cwd)
        watcher = open(".ferment_watcher", "r", encoding="utf-8")
        content = watcher.read()
        content = content.split("\n")
        for path in content:
            os.remove(path)
        return super().uninstall()

    def test(self):
        if subprocess.check_output(["command", "jq"]) > 0:
            print("False")
            return False
        print("True")
        return True

    def build(self):
        os.chdir(self.cwd)
        subprocess.call(
            ["make", f"-j{os.cpu_count()*1.5}"], env=universalbinaryenv())


class prebuild(Prebuild):
    def __init__(self):
        self.amd64 = "ferment://jq@jq.tar.gz"
        self.arm64 = "ferment://jq@jq.tar.gz"

    def install(self):
        os.chdir(self.cwd)
        subprocess.call(["make", "install"])
