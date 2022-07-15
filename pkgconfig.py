#Credit: Kareku Sato - https://noknow.info/it/os/install_pkg_config_from_source?lang=en
import os
import subprocess

from index import Barrells, Prebuild


class pkgconfig(Barrells):
    def __init__(self):
        self.url="https://pkgconfig.freedesktop.org/releases/pkg-config-0.29.2.tar.gz"
        self.git=False
        self.description="Manage compile and link flags for libraries"
        self.dependencies=["autoconf", "automake", "libtool"]
        self.prebuild=prebuild()
    def install(self):
        os.chdir(self.cwd)
        args=["--disable-debug", f"--prefix=/usr/local/","--disable-host-tool", "--with-internal-glib"]
        env=os.environ.copy()
        env["CC"]="clang"
        env["CXX"]="clang++"
        env["CFLAGS"]="-arch arm64 -arch x86_64"
        env["CXXFLAGS"]="-arch arm64 -arch x86_64"
        subprocess.call(["sh","configure", *args], env=env)
        subprocess.call(["make", f"-j{os.cpu_count()}"], env=env)
        subprocess.call(["make","install", f"-j{os.cpu_count()}"], env=env)
        os.mkdir("/usr/local/lib/pkgconfig")
    def build(self):
        with open(f"{self.cwd}/pkgconfig-build.log", "a") as stdout:
            os.chdir(self.cwd)
            args=["--disable-debug", f"--prefix=/usr/local/","--disable-host-tool", "--with-internal-glib"]
            env=os.environ.copy()
            env["CC"]="clang"
            env["CXX"]="clang++"
            env["CFLAGS"]="-arch arm64 -arch x86_64"
            env["CXXFLAGS"]="-arch arm64 -arch x86_64"
            env["INSTALL"]="install -p"
            subprocess.call(["sh","configure", *args], env=env, stdout=stdout, stderr=stdout)
            subprocess.call(["make", f"-j{os.cpu_count()}"], env=env, stdout=stdout, stderr=stdout)

    def test(self):
        e=subprocess.call(["pkg-config", "--version"])
        if e > 0:
            print('false')
            return False
        print('true')
        return True

    def uninstall(self) -> bool:
        try:
            os.chdir(self.cwd)
            subprocess.call(["make", "uninstall"])
        finally:
            return super().uninstall()
class prebuild(Prebuild):
    def __init__(self):
        self.amd64="ferment://pkgconfig@pkgconfig.tar.gz"
        self.arm64="ferment://pkgconfig@pkgconfig.tar.gz"
    def install(self):
        os.chdir(self.cwd)
        self.removeTMPWaterMark("pkgconfig", ["glib/Makefile"])
        subprocess.call(["make", "install", f"-j{os.cpu_count()}"])
