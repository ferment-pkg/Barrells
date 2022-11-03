# Created With Barrell Tool https://ferment.tk/create
import subprocess

from index import Barrells


class rust(Barrells):
    def __init__(self):
        self.description = "A language empowering everyone to build reliable and efficient software"
        self.url = "interactive:sh:https://sh.rustup.rs"
        self.git = False
        self.setup = True
        self.version="1.62"
        self.home = "https://www.rust-lang.org"
        self.dependencies = []


    def install(self) -> bool:
        self.EditPath("$HOME/.cargo/bin")
        return super().install()

    def uninstall(self) -> bool:
        subprocess.run(
            ["rustup", "self", "uninstall"],
            input=b"y\n",
            stdout=open("/tmp/uninstall.log", "a"),
            stderr=open("/tmp/uninstall.log", "a"),
        )
        return super().uninstall()
