# Structure Of FPKGS

## File name
`{{pkg_name}}.fpkg`

## Structure
Similar to shell scripts but with a couple of differences.

```bash
pkgname={{package_name}}
alias="array","of","aliases"
version="string"
desc="A normal string"
#only valid arches
arch="amd64","arm64", "universal"
source="an","array","of","http/git","sources"
# dependencies 
# Array's don't need to be quoted unless it has spaces
dependencies=sdl2,htop
#Dbuilds are dev-dependencies or dependencies that are only needed for building
Dbuild=automake,autoconf
license=MIT,Apache

build(){
    ./build.sh
    #use identations and architechtures to run a line of code exclusicely on one ARCH
    arm64:
        cp build arm64
    amd64:
        cp build amd64
}

test(){
    #$variables store data like strings or number
    #@ variables store outputs of a command
    $var="hello world"
    @output="command -v"
    # match is a built in command, the bottom should return false
    match $output == "v1"
}
install(){
    ln -s * /
}
```
## Built In Commands

| Command | Description | Arguments
| --- | --- | ---|
| `match` | Matches two strings or numbers (TEST SECTION ONLY) | "item1" "operator" "item2"
| `fileman` | Edit or write to a file | "`append`, `write`" "content"
## Supported Compilers or Buildtools (For Universal Builds)
Compilers: `clang`, `clang++`
Buildtools: `cmake`, `autotools`

## Important Commands
### Universal Envs for Clang
If universal is set as an arc any other set archs will be ignored, the fermenter(package builder) will add the following envs to the build script
```bash
CC = "clang"

CXX = "clang++"

CFLAGS = "-arch arm64 -arch x86_64"

CXXFLAGS = "-arch arm64 -arch x86_64"
```
These flags will allow for universal binaries to be built, make sure that your package can work as a universal binary.
