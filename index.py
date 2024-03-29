import os
import subprocess
from typing import List, Optional
from urllib import request


class Barrells:
    def __init__(self):
        self.url: str
        """ currently supported protocols, http, https, sh(built into the program), interactive(built into the program and only works with sh)"""
        self.description: str
        self.homepage: str
        self.prebuild: Optional[Prebuild]
        self.version: str
        self.git: bool
        self.license: str
        self.mirror: Optional[list[str]]
        self.sha256: str
        self.supported_OS: list[str]
        self.dependencies: list[str]
        self.binary: str
        self.lib: bool
        self.setup: bool = False
        self.caveats: str
        # Provided by the cmd
        self.cwd: str
        self.arch: str

    def install(self) -> bool:
        print("True")
        return True

    def uninstall(self) -> bool:
        print("True")
        return True

    def build(self) -> bool:
        print("True")
        return True

    def update(self) -> bool:
        print("True")
        return True

    def test(self) -> bool:
        print("True")
        return True

    def download(self) -> bool:
        print("True")
        return True
    # Helper Functions DON'T EDIT

    def SetPVar(self, var: str, value: str) -> None:
        home = os.getenv("HOME")
        with open(f"{home}/.zshrc", "a") as f:
            f.write(f"export {var}={value}\n")

    def editRC(self, content: str):
        home = os.getenv("HOME")
        with open(f"{home}/.zshrc", "a") as f:
            f.write(f"{content}\n")

    def EditPath(self, path: str):
        home = os.getenv("HOME")
        with open(f"{home}/.zshrc", "a") as f:
            f.write(f"PATH=$PATH:{path}\n")

    def SetPkgConfigPath(self) -> None:
        os.environ["PKG_CONFIG_PATH"] = "/usr/local/lib/pkgconfig"

    def runcmdincwd(self, cmd):
        return subprocess.run(cmd, cwd=self.cwd)

    def removeTMPWaterMark(self, pkg: str) -> None:
        originalcontent = open("Makefile", "r+").read()
        while(f"/private/tmp/fermenter/{pkg}" in originalcontent):
            originalcontent = originalcontent.replace(
                f"/private/tmp/fermenter/{pkg}", self.cwd+f"/")
            originalcontent = originalcontent.replace(
                f"/tmp/fermenter/{pkg}", self.cwd+f"/")
            originalcontent = originalcontent.replace(
                "install: all install-bin install-hdrs install-lib install-data", "install: install-bin install-hdrs install-lib install-data")
            open("Makefile", "w").write(originalcontent)
            originalcontent = open("Makefile", "r+").read()
        builddir = os.listdir("build")
        # buildir should only contains files with the .d extention
        builddir = [x for x in builddir if x.endswith(".d")]
        for x in builddir:
            ogcontent = open(f"build/{x}", "r+").read()
            ogcontent = ogcontent.replace(
                f"/private/tmp/fermenter/{pkg}", self.cwd+f"/")
            open("build/"+x, "w").write(ogcontent)
            ogcontent = open(f"build/{x}", "r+").read()
        originalcontent = open("libtool", "r+").read()
        originalcontent = originalcontent.replace(
            f"/private/tmp/fermenter/{pkg}", self.cwd+f"/")
        originalcontent = originalcontent.replace(
            f"/tmp/fermenter/{pkg}", self.cwd+f"/")
        open("libtool", "w").write(originalcontent)


class Prebuild():
    def __init__(self):
        self.amd64: str
        self.arm64: str
        self.cwd: str

    def install(self):
        return bool

    def uninstall(self):
        return bool

    def removeTMPWaterMark(self, pkg: str, files: List[str] = None) -> None:
        originalcontent = open("Makefile", "r+").read()
        while(f"/private/tmp/fermenter/{pkg}" in originalcontent):
            originalcontent = originalcontent.replace(
                f"/private/tmp/fermenter/{pkg}", self.cwd+f"/")
            originalcontent = originalcontent.replace(
                f"/tmp/fermenter/{pkg}", self.cwd+f"/")
            open("Makefile", "w").write(originalcontent)
            originalcontent = open("Makefile", "r+").read()
        if os.path.isdir(f"{self.cwd}/build"):
            builddir = os.listdir("build")
            # buildir should only contains files with the .d extention
            builddir = [x for x in builddir if x.endswith(".d")]
            for x in builddir:
                ogcontent = open(f"build/{x}", "r+").read()
                ogcontent = ogcontent.replace(
                    f"/private/tmp/fermenter/{pkg}", self.cwd+f"/")
                open("build/"+x, "w").write(ogcontent)
                ogcontent = open(f"build/{x}", "r+").read()
            originalcontent = open("libtool", "r+").read()
            originalcontent = originalcontent.replace(
                f"/private/tmp/fermenter/{pkg}", self.cwd+f"/")
            originalcontent = originalcontent.replace(
                f"/tmp/fermenter/{pkg}", self.cwd+f"/")
            open("libtool", "w").write(originalcontent)
        for f in files:
            print(f)
            ogcontent = open(f, "r+").read()
            ogcontent = ogcontent.replace(
                f"/private/tmp/fermenter/{pkg}", self.cwd+f"/")
            ogcontent = ogcontent.replace(
                f"/tmp/fermenter/{pkg}", self.cwd+f"/")
            open(f, "w").write(ogcontent)


def patch(url, dst):
    # visit the url and download the patch
    request.urlretrieve(
        url, f"/tmp/{url.split('/')[-1]}")
    # apply the patch
    subprocess.run(
        ["patch", "-p1", dst, f"/tmp/{url.split('/')[-1]}"])


def universalbinaryenv():
    env = os.environ.copy()
    env["CC"] = "clang"
    env["CXX"] = "clang++"
    env["CFLAGS"] = "-arch arm64 -arch x86_64"
    env["CXXFLAGS"] = "-arch arm64 -arch x86_64"
    return env
