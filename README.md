[![Download](https://api.bintray.com/packages/bincrafters/public-conan/wxwidgets%3Abincrafters/images/download.svg) ](https://bintray.com/bincrafters/public-conan/wxwidgets%3Abincrafters/_latestVersion)
[![Build Status Travis](https://travis-ci.com/bincrafters/conan-wxwidgets.svg?branch=stable%2F3.1.2)](https://travis-ci.com/bincrafters/conan-wxwidgets)
[![Build Status AppVeyor](https://ci.appveyor.com/api/projects/status/github/bincrafters/conan-wxwidgets?branch=stable%2F3.1.2&svg=true)](https://ci.appveyor.com/project/bincrafters/conan-wxwidgets)

## Conan package recipe for [*wxwidgets*](https://www.wxwidgets.org/)

wxWidgets is a C++ library that lets developers create applications for Windows, Mac OS X, Linux and other platforms with a single code base.

The packages generated with this **conanfile** can be found on [Bintray](https://bintray.com/bincrafters/public-conan/wxwidgets%3Abincrafters).


## Issues

If you wish to report an issue or make a request for a package, please do so here:

[Issues Tracker](https://github.com/bincrafters/community/issues)


## For Users

### Basic setup

    $ conan install wxwidgets/3.1.2@bincrafters/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    wxwidgets/3.1.2@bincrafters/stable

    [generators]
    cmake

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..

Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git.


## Build and package

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from "build_requires" and "requires" , and then running the build() method.

    $ conan create . bincrafters/stable


### Available Options
| Option        | Default | Possible Values  |
| ------------- |:----------------- |:------------:|
| shared      | False |  [True, False] |
| fPIC      | True |  [True, False] |
| unicode      | True |  [True, False] |
| compatibility      | 3.0 |  ['2.8', '3.0', '3.1'] |
| zlib      | zlib |  ["off", "sys", 'zlib'] |
| png      | libpng |  ["off", "sys", 'libpng'] |
| jpeg      | libjpeg |  ["off", "sys", 'libjpeg', 'libjpeg-turbo', 'mozjpeg'] |
| tiff      | libtiff |  ["off", "sys", 'libtiff'] |
| expat      | expat |  ["off", "sys", 'expat'] |
| secretstore      | True |  [True, False] |
| aui      | True |  [True, False] |
| opengl      | True |  [True, False] |
| html      | True |  [True, False] |
| mediactrl      | False |  [True, False] |
| propgrid      | True |  [True, False] |
| debugreport      | True |  [True, False] |
| ribbon      | True |  [True, False] |
| richtext      | True |  [True, False] |
| sockets      | True |  [True, False] |
| stc      | True |  [True, False] |
| webview      | True |  [True, False] |
| xml      | True |  [True, False] |
| xrc      | True |  [True, False] |
| cairo      | True |  [True, False] |


## Add Remote

    $ conan remote add bincrafters "https://api.bintray.com/conan/bincrafters/public-conan"


## Conan Recipe License

NOTE: The conan recipe license applies only to the files of this recipe, which can be used to build and package wxwidgets.
It does *not* in any way apply or is related to the actual software being packaged.

[MIT](https://github.com/bincrafters/conan-wxwidgets/blob/stable/3.1.2/LICENSE.md)
