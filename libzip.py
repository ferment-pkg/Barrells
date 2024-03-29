import os
import subprocess

from index import Barrells, Prebuild, universalbinaryenv


class libzip(Barrells):
    def __init__(self):
        self.url = "https://libzip.org/download/libzip-1.9.2.tar.gz"
        self.git = False
        self.description = "A C library for reading, c, and modifying zip archives"
        self.dependencies = ["cmake"]
        self.lib = True
        self.version = "1.9.2"
        self.dualarch = True
        self.prebuild = prebuild()

    def install(self):
        args = [
            "-DENABLE_GNUTLS=OFF",
            "-DENABLE_MBEDTLS=OFF",
            "-DENABLE_OPENSSL=OFF",
            "-DBUILD_REGRESS=OFF",
            "-DBUILD_EXAMPLES=OFF",
            f"-DCMAKE_INSTALL_PREFIX={self.cwd}/built"
        ]
        subprocess.call(
            ["cmake", ".", "-DCMAKE_BUILD_TYPE=release", " ".join(args)], cwd=self.cwd
        )
        subprocess.call(
            ["make", f"DESTDIR={self.cwd}/built", "install", f"-j{os.cpu_count()}"], cwd=self.cwd)
        for directory in ["bin", "share", "lib", "include"]:
            os.rename(f"{self.cwd}/built/usr/local/{directory}",
                      f"{self.cwd}/built/{directory}")
        os.chdir(f"{self.cwd}/built")
        os.remove("usr")
        subprocess.call(["cp", "-rS", f"{self.cwd}/built/*", "/usr/local/"])

    def build(self):
        os.chdir(self.cwd)
        with open("libzip-build.log", "a") as stdout:
            args = [
                "-DENABLE_GNUTLS=OFF",
                "-DENABLE_MBEDTLS=OFF",
                "-DENABLE_OPENSSL=OFF",
                "-DBUILD_REGRESS=OFF",
                "-DBUILD_EXAMPLES=OFF",
                f"-DCMAKE_INSTALL_PREFIX={self.cwd}/built"
            ]
            os.mkdir("build")
            os.chdir("build")
            subprocess.call(
                ["cmake", "..", "-DCMAKE_BUILD_TYPE=release", " ".join(args)],  stdout=stdout, stderr=stdout
            )
            subprocess.call(["make", f"-j{os.cpu_count()}"],
                            stdout=stdout, stderr=stdout)
            subprocess.call(["make", f"DESTDIR={self.cwd}/built", "install"],
                            stdout=stdout, stderr=stdout)
            os.chdir(f"{self.cwd}/built")
            for directory in ["bin", "share", "lib", "include"]:
                os.rename(f"{self.cwd}/built/usr/local/{directory}",
                          f"{self.cwd}/built/{directory}")
            os.remove("usr")
            stdout.write(os.listdir(self.cwd+"/built"))

    def uninstall(self) -> bool:
        os.chdir(self.cwd)
        os.remove("built")
        return super().uninstall()

    def test(self) -> bool:
        os.chdir("/tmp")
        test = open("ziptest.c", "w")
        test.write(
            "#include <zip.h>\nint main(){zip_t *z=zip_open(\"test.zip\",0,NULL);zip_close(z);return 0;}")
        test.close()
        out = subprocess.call(["gcc", "-I/usr/local/include/", "-L/usr/local/lib/",
                               "-o", "ziptest", "ziptest.c"], env=universalbinaryenv())
        if out > 0:
            print("False")
            return False
        print("True")
        return True


class prebuild(Prebuild):
    def __init__(self):
        self.amd64 = "ferment://libzip-amd64@libzip.tar.gz"
        self.arm64 = "ferment://libzip-arm64@libzip.tar.gz"

    def install(self):
        subprocess.call(["cp", "-Rs", f"{self.cwd}/built/*", "/usr/local/"])
