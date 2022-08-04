import os
import subprocess
import sys

from index import Barrells, Prebuild


class qemu(Barrells):
    def __init__(self):
        self.url="https://gitlab.com/qemu-project/qemu.git"
        self.git=True
        self.description="Emulator for x86 and PowerPC"
        self.homepage="https://www.qemu.org/"
        self.dependencies=["automake", "ninja", "glib", "pkg-config"]
        self.version="6.1"
        self.prebuild=prebuilt()
    def install(self):
        with open('/tmp/qemu.log', "a") as sys.stdout:
            os.chdir(self.cwd)
            subprocess.call(["git", "checkout", f"stable-{self.version}"])
            os.environ["PKG_CONFIG_PATH"]="/usr/local/lib/pkgconfig"
            args=["--disable-bsd-user", "--disable-guest-agent", "--enable-curses", "--enable-libssh", "--enable-slirp=system", "--enable-vde",  "--extra-cflags=-DNCURSES_WIDECHAR=1", "--disable-sdl", '--disable-gtk', '--enable-cocoa']
            os.mkdir("build")
            subprocess.call(["git", "submodule", "init"], stdout=sys.stdout, stderr=sys.stdout)
            subprocess.call(["git", "submodule", "update", "--recursive", f"--jobs={os.cpu_count()}"], stdout=sys.stdout, stderr=sys.stdout)
            subprocess.call(["git", "submodule", "status", "--recursive"],stdout=sys.stdout, stderr=sys.stdout)
            os.chdir("build")
            subprocess.call(["sh", "../configure", *args], stdout=sys.stdout, stderr=sys.stdout)
            subprocess.call(["make", f"-j{os.cpu_count()}"], stdout=sys.stdout, stderr=sys.stdout)
            subprocess.call(["make","V=1", "install"],  stdout=sys.stdout, stderr=sys.stdout)
            return super().install()
    def uninstall(self) -> bool:
        try:
            os.remove("/usr/local/share/qemu")
            bin=os.listdir("/usr/local/bin")
            for l in bin:
                if "qemu" in l:
                    os.remove(f"/usr/local/bin/{l}")
        finally:
            return super().uninstall()
    def test(self):
        l=subprocess.run(["qemu-system-x86_64", "-h"])
        if l.returncode != 0:
            return False
        return super().test()
    def build(self):
       with open('/tmp/qemu.log', "a") as sys.stdout:
            os.chdir(self.cwd)
            subprocess.call(["git", "checkout", f"stable-{self.version}"])
            os.environ["PKG_CONFIG_PATH"]="/usr/local/lib/pkgconfig"
            env=os.environ.copy()
            env["CC"]="clang"
            env["CXX"]="clang++"
            env["CFLAGS"]="-arch arm64 -arch x86_64"
            env["CXXFLAGS"]="-arch arm64 -arch x86_64"
            args=["--disable-bsd-user", "--disable-guest-agent", "--enable-libssh", "--enable-slirp=system", "--enable-vde",  "--extra-cflags=-DNCURSES_WIDECHAR=1", "--disable-sdl", '--disable-gtk', '--enable-cocoa',f"--prefix={self.cwd}/built"]
            os.mkdir("build")
            subprocess.call(["git", "submodule", "init"], stdout=sys.stdout, stderr=sys.stdout)
            subprocess.call(["git", "submodule", "update", "--recursive", f"--jobs={os.cpu_count()}"], stdout=sys.stdout, stderr=sys.stdout)
            subprocess.call(["git", "submodule", "status", "--recursive"],stdout=sys.stdout, stderr=sys.stdout)
            os.chdir("build")
            subprocess.call(["sh", "../configure", *args], stdout=sys.stdout, stderr=sys.stdout)
            subprocess.call(["make", f"-j{os.cpu_count()}"], stdout=sys.stdout, stderr=sys.stdout)
            subprocess.call(["make", "install"])
            #get all directories
            dirs=os.listdir(f"{self.cwd}")
            os.chdir(self.cwd)
            #remove each directory
            for d in dirs:
                if d !="built":
                    os.remove(f"{self.cwd}/{d}", recursive=True)



class prebuilt(Prebuild):
    def __init__(self):
        self.amd64="ferment://qemu@qemu.tar.gz"
        self.arm64="ferment://qemu@qemu.tar.gz"
    def install(self):
        with open("/tmp/qemu.log") as sys.stdout:
            os.chdir(self.cwd)
            os.link(f'{self.cwd}/built/*','/usr/local/')



