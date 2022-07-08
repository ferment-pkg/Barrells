# Created With Barrells Tool https://ferment.tk/create
import os
import subprocess

from index import Barrells, Prebuild


class sdl2(Barrells):
    def __init__(self):
        self.description = "an image library"
        self.url = "https://libsdl.org/release/SDL2-2.0.22.tar.gz"
        self.git = False
        self.lib = True
        self.home = "https://libsdl.org"
        self.dependencies = ["autoconf", "automake"]
        self.prebuild=prebuild()

    def install(self):
        import os
        os.chdir(self.cwd)
        import subprocess
        args=["--prefix=/usr/local/"]
        subprocess.call(["sh", "configure"], env=[f"CC={self.cwd}/build-scripts/clang-fat.sh"])
        subprocess.call(["make"])
        subprocess.call(["make", "install"])
    def build(self):
        import os
        os.chdir(self.cwd)
        import subprocess
        args=["--prefix=/usr/local/"]
        subprocess.call(["sh", "configure", *args], env=[f"CC={self.cwd}/build-scripts/clang-fat.sh"])
        subprocess.call(["make"])
    def uninstall(self) -> bool:
        subprocess.call(["make", "uninstall"])
        return super().uninstall()
    def test(self):
        with open("/tmp/sdl.cpp", "a") as f:
            f.write("#include <SDL2/SDL.h>\n")
            f.write("int main(int argc, char* argv[]) {\n")
            f.write("    SDL_Init(SDL_INIT_VIDEO);\n")
            f.write("    SDL_Quit();\n")
            f.write("    return 0;\n")
            f.write("}\n")
            f.close()
        i=subprocess.call(["clang", "-o", "sdl", "/tmp/sdl.cpp"])
        if i > 0:
            print("False")
            return False
        print("True")
        return True
class prebuild(Prebuild):
    def __init__(self):
       self.amd64="ferment://sdl2@sdl2.tar.gz"
       self.arm64="ferment://sdl2@sdl2.tar.gz"
    def install(self):
        os.chdir(self.cwd)
        subprocess.call(["make", "install"])
