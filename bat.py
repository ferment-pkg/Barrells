# Created With Barrell Tool https://ferment.tk/create
import subprocess

from index import Barrells


class bat(Barrells):
    def __init__(self):
        self.description = "Clone of cat(1) with syntax highlighting and Git integration"
        self.url = "https://github.com/sharkdp/bat/archive/v0.21.0.tar.gz"
        self.git = False
        self.lib = False
        self.version="0.21"
        self.home = "https://github.com/sharkdp/bat"
        self.dependencies = ["rust"]

    def install(self):
        subprocess.call(["cargo", "install","--locked", "bat"])
        return super().install()
    def uninstall(self) -> bool:
        subprocess.call(["cargo", "uninstall","--locked", "bat"])
        return super().uninstall()
