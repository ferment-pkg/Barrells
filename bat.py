# Created With Barrell Tool https://ferment.tk/create
import os
import subprocess

from index import Barrells, Prebuild


class bat(Barrells):
    def __init__(self):
        self.description = "Clone of cat(1) with syntax highlighting and Git integration"
        self.url = "https://github.com/sharkdp/bat/archive/v0.21.0.tar.gz"
        self.git = False
        self.lib = False
        self.version = "0.21"
        self.home = "https://github.com/sharkdp/bat"
        self.dependencies = ["rustc:rust"]
        self.prebuild = prebuild()

    def install(self):
        subprocess.call(["cargo", "install", "--locked", "bat"])
        return super().install()

    def uninstall(self) -> bool:
        os.chdir(self.cwd)
        if "PREBUILD" in os.listdir():
            os.remove("bat")
        else:
            subprocess.call(["cargo", "uninstall", "--locked", "bat"])
        return super().uninstall()

    def build(self):
        os.chdir(self.cwd)
        subprocess.call(
            ["cargo", "build", "--target=aarch64-apple-darwin", "bat"])
        subprocess.call(
            ["cargo", "build", "--target=x86_64-apple-darwin", "bat"])
        # link with lipo
        subprocess.call(["lipo", "-create", "-output", "bat",
                        "target/aarch64-apple-darwin/release/bat", "target/x86_64-apple-darwin/release/bat"])

        contents = os.listdir()
        # remove bat from contents
        contents.remove("bat")
        # move contents to bin
        for item in contents:
            os.remove(item)
        # make empty file called PREBUILD
        open("PREBUILD", "w").close()
        return super().build()

    def test(self):
        out = subprocess.call("bat", "-V")
        if out > 0:
            print("False")
            return False
        print("True")
        return True


class prebuild(Prebuild):
    def __init__(self):
        self.amd64 = "ferment://bat@bat.tar.gz"
        self.arm64 = "ferment://bat@bat.tar.gz"

    def install(self):
        os.chdir(self.cwd)
        os.symlink("bat", "/usr/local/bin/bat")
