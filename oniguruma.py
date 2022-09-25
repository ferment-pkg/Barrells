import os
import subprocess

from index import Barrells, Prebuild, universalbinaryenv


class oniguruma(Barrells):
    def __init__(self):
        self.url = "https://github.com/kkos/oniguruma/releases/download/v6.9.8/onig-6.9.8.tar.gz"
        self.git = False
        self.version = "6.9.8"
        self.description = "Oniguruma is a modern and flexible regular expressions library."
        self.dependencies = ["autoconf", "automake", "libtool"]
        self.lib = True

    def install(self) -> bool:
        os.chdir(self.cwd)
        subprocess.run(["autoreconf", "-vfi"])
        subprocess.run(
            ["sh", "./configure"])
        subprocess.call(["make"])
        subprocess.call(["make", "install"])

        return super().install()

    def uninstall(self) -> bool:
        os.chdir(self.cwd)
        watcher = open(".ferment_watcher", "r", encoding='utf-8')
        content = watcher.read()
        watcher.close()
        content = content.split("\n")
        for line in content:
            os.remove(line)

    def build(self) -> bool:
        os.chdir(self.cwd)
        subprocess.run(["autoreconf", "-vfi"])
        subprocess.run(
            ["sh", "./configure"])
        subprocess.call(
            ["make", f"-j{os.cpu_count()}"],  env=universalbinaryenv())

        return super().build()

    def test(self):
        os.chdir(self.cwd)
        if subprocess.check_output(["make", "check"]) != 0:
            print("False")
            return False
        print("True")
        return True


class prebuild(Prebuild):
    def __init__(self):
        self.amd64 = "ferment://oniguruma@oniguruma.tar.gz"
        self.arm64 = "ferment://oniguruma@oniguruma.tar.gz"

    def install(self):
        os.chdir(self.cwd)
        subprocess.call(["make", "install"])
