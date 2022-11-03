# Created With Barrell Tool https://fermentpkg.tech/create
from index import Barrells


class libtool(Barrells):
    def __init__(self):
        self.description = "GNU Libtool is a generic library support script."
        self.url = "https://ftpmirror.gnu.org/libtool/libtool-2.4.6.tar.gz"
        self.git = False
        self.lib = False
        self.home = "https://www.gnu.org/software/libtool/"
        self.dependencies = ["autoconf", "automake"]
        self.version = "2.4.6"

    def install(self):
        print("Not implemented")
