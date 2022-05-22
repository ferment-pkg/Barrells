        with open("/tmp/glib-build.log", "a") as sys.stdout:
            os.chdir(self.cwd)
            args=["--default-library=both", "-Diconv=auto", "-Dbsymbolic_functions=false", "-Ddtrace=false"]
            os.mkdir(f"{self.cwd}/build")
            os.chdir(f"{self.cwd}/build")
            subprocess.call(["meson", *args, ".."],stdout=sys.stdout, stderr=sys.stdout)
            subprocess.run(["ninja"],stdout=sys.stdout, stderr=sys.stdout)
            subprocess.run(["ninja", "install"],stdout=sys.stdout, stderr=sys.stdout)
            return super().install()
