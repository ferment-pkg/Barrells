# Created With Barrells Tool https://ferment.tk/create
import os
import subprocess
import sys

from index import Barrells, Prebuild


class sdl2(Barrells):
    def __init__(self):
        self.description = "an image library"
        self.url = "https://libsdl.org/release/SDL2-2.0.22.tar.gz"
        self.git = False
        self.lib = True
        self.home = "https://libsdl.org"
        self.dependencies = ["autoconf", "automake"]
        self.prebuild = prebuild()
        self.args = ["--enable-hidapi"]
        self.version = "2.0.22"

    def install(self):
        import os
        os.chdir(self.cwd)
        import subprocess
        args = ["--prefix=/usr/local/", *self.args]
        env = os.environ.copy()
        env["CC"] = f"{self.cwd}/build-scripts/clang-fat.sh"
        env["CXX"] = f"{self.cwd}/build-scripts/clang++-fat.sh"
        subprocess.call(["sh", "configure", *args], env=env)
        subprocess.call(["make"])
        subprocess.call(["make", "install"])

    def build(self):
        with open(f"{self.cwd}/sdl2-build.log", "a") as sys.stdout:
            import os

            #
            os.chdir(self.cwd)
            import subprocess
            args = [f"--prefix={self.cwd}/built", *self.args]
            env = os.environ.copy()
            env["CC"] = f"{self.cwd}/build-scripts/clang-fat.sh"
            env["CXX"] = f"{self.cwd}/build-scripts/clang++-fat.sh"
            subprocess.run(["sh", "./configure", *args], env=env,
                           stdout=sys.stdout, stderr=sys.stdout)
            subprocess.run(
                ["make", f"-j{os.cpu_count()}"], stdout=sys.stdout, stderr=sys.stdout)
            subprocess.call(["make", "install"],
                            stdout=sys.stdout, stderr=sys.stdout)
            files = os.listdir(self.cwd)
            # remove built from dirs
            files.remove("built")
            for file in files:
                os.remove(file)
            os.rename("built", "build")

    def uninstall(self) -> bool:
        os.chdir(self.cwd)
        subprocess.call(["make", "uninstall"])
        return super().uninstall()

    def test(self):
        i = subprocess.call(["sdl2-config", "--version"])
        if i > 0:
            print("False")
            return False
        print("True")
        return True


class prebuild(Prebuild):
    def __init__(self):
        self.amd64 = "ferment://sdl2@sdl2.tar.gz"
        self.arm64 = "ferment://sdl2@sdl2.tar.gz"

    def install(self):
        os.chdir(self.cwd)
        os.symlink("build/*", "/usr/local/")
