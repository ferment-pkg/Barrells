import os
import subprocess
import sys

from index import Barrells, Prebuild


class bitgit(Barrells):
    def __init__(self):
        self.git=False
        self.url="https://github.com/chriswalz/bit/archive/v1.1.2.tar.gz"
        self.description="Bit is a modern Git CLI"
        self.homepage="https://github.com/chriswalz/bit"
        self.sha256="563ae6b0fa279cb8ea8f66b4b455c7cb74a9e65a0edbe694505b2c8fc719b2ff"
        self.license="Apache-2.0"
        self.version="1.1.2"
        self.dependencies=["go", "curl", "git"]
        self.binary="bit"
        self.prebuild=prebuild()
    def install(self):
        with open("/tmp/bitgit.log", "a") as sys.stdout:
            subprocess.run(["go", "build"], cwd=self.cwd, stdout=sys.stdout, stderr=sys.stdout)
            return True
    def build(self):
           with open("/tmp/bitgit.log", "a") as sys.stdout:
            subprocess.run(["go", "build", "-o", "x86-bitgit"], cwd=self.cwd, stdout=sys.stdout, stderr=sys.stdout)
            print("Building for arm64 now")
            os.environ["GOARCH"]="arm64"
            subprocess.run(["go", "build", "-o", "arm64-bitgit"], cwd=self.cwd, stdout=sys.stdout, stderr=sys.stdout)
            subprocess.call(["lipo", "-create", "-output","bit","x86-bitgit", "arm64-bitgit" ], cwd=self.cwd, stdout=sys.stdout, stderr=sys.stdout)
            os.chdir(self.cwd)
            os.remove("x86-bitgit")
            os.remove("arm64-bitgit")
    def uninstall(self) -> bool:
        try:
            os.remove("/usr/local/bin/bit")
        finally:
            return super().uninstall()
    def test(self):
        subprocess.run(["git", "init", "/tmp/testDir"])
        subprocess.run(["touch", "/tmp/testDir/test.txt"])
        subprocess.run(["/usr/local/bin/bit", "add", "test.txt"], cwd="/tmp/testDir/")
        output=subprocess.check_output(["/usr/local/bin/bit", "status"], cwd="/tmp/testDir/")
        if b"new file:   test.txt" in output:
            print("True")
            return True
        else:
            print("False")
            return False

#prebuild install here ->
class prebuild(Prebuild):
    def __init__(self):
        self.amd64="ferment://bitgit@bitgit.tar.gz"
        self.arm64="ferment://bitgit@bitgit.tar.gz"
    def install(self):
        os.chdir(self.cwd)
