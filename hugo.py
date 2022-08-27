# Created With Barrell Tool https://fermentpkg.tech/create
import os
import subprocess

from index import Barrells, Prebuild


class hugo(Barrells):
    def __init__(self):
        self.description = "A static site generator"
        self.url = "https://github.com/gohugoio/hugo/archive/refs/tags/v0.101.0.tar.gz"
        self.git = False
        self.lib = False
        self.home = "https://gohugo.io"
        self.dependencies = ["go"]
        self.binary = "hugo"
        self.version = "0.101.0"

    def install(self):
        os.chdir(self.cwd)
        subprocess.call(["go", "build", "-o", "hugo"])
        return super().install()

    def uninstall(self) -> bool:
        os.chdir(self.cwd)
        os.remove("hugo")
        return super().uninstall()

    def build(self):
        os.chdir(self.cwd)
        with open("hugo-build.log", "a") as stdout:
            env = os.environ.copy()
            env["GOARCH"] = "amd64"
            subprocess.call(["go", "build", "-o", "hugo-amd64"],
                            stdout=stdout, stderr=stdout, env=env)
            env["GOARCH"] = "arm64"
            subprocess.call(["go", "build", "-o", "hugo-arm64"],
                            stdout=stdout, stderr=stdout, env=env)
            subprocess.call(["lipo", "-create", "-output", "hugo",
                            "hugo-amd64", "hugo-arm64"], stdout=stdout, stderr=stdout)
            contents = os.listdir()
            # remove hugo from contents
            contents.remove("hugo")
            # move contents to bin
            stdout.write(contents)
            for item in contents:
                os.remove(item)
        return super().build()

    def test(self):
        out = subprocess.call("which", "hugo")
        if out > 0:
            print("False")
            return False
        print("True")
        return True


class prebuild(Prebuild):
    def __init__(self):
        self.amd64 = "ferment://hugo@hugo.tar.gz"
        self.arm64 = "ferment://hugo@hugo.tar.gz"

    def install(self):
        os.chdir(self.cwd)
        return super().install()
