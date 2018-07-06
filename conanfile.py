#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class wxWidgetsConan(ConanFile):
    name = "wxwidgets"
    version = "3.1.1"
    description = "wxWidgets is a C++ library that lets developers create applications for Windows, Mac OS X, " \
                  "Linux and other platforms with a single code base."
    url = "https://github.com/bincrafters/conan-libname"
    homepage = "https://www.wxwidgets.org/"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "wxWidgets"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "fPIC": [True, False],
               "zlib": [None, "system", "zlib"],
               "png": [None, "system", "libpng"],
               "jpeg": [None, "system", "libjpeg", "libjpeg-turbo"],
               "tiff": [None, "system", "libtiff"],
               "expat": [None, "system", "expat"]}
    default_options = "shared=False",\
                      "fPIC=True",\
                      "zlib=zlib",\
                      "png=libpng",\
                      "jpeg=libjpeg",\
                      "tiff=libtiff",\
                      "expat=expat"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def requirements(self):
        if self.options.png == 'libpng':
            self.requires.add('libpng/1.6.34@bincrafters/stable')
        if self.options.jpeg == 'libjpeg':
            self.requires.add('libjpeg/9c@bincrafters/stable')
        elif self.options.jpeg == 'libjpeg-turbo':
            self.requires.add('libjpeg-turbo/1.5.2@bincrafters/stable')
        if self.options.tiff == 'libtiff':
            self.requires.add('libtiff/4.0.9@bincrafters/stable')
        if self.options.zlib == 'zlib':
            self.requires.add('zlib/1.2.11@conan/stable')
        if self.options.expat == 'expat':
            self.requires.add('expat/2.2.5@bincrafters/stable')

    def source(self):
        source_url = "https://github.com/wxWidgets/wxWidgets"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def configure_cmake(self):
        def option_value(option):
            return 'OFF' if option is None else 'sys'
        cmake = CMake(self)
        cmake.definitions['wxBUILD_SHARED'] = self.options.shared
        cmake.definitions['wxBUILD_SAMPLES'] = 'OFF'
        cmake.definitions['wxBUILD_TESTS'] = 'OFF'
        cmake.definitions['wxBUILD_DEMOS'] = 'OFF'
        cmake.definitions['wxBUILD_INSTALL'] = True

        if self.settings.compiler == 'Visual Studio':
            cmake.definitions['wxBUILD_USE_STATIC_RUNTIME'] = 'MT' in str(self.settings.compiler.runtime)
            cmake.definitions['wxBUILD_MSVC_MULTIPROC'] = True

        cmake.definitions['wxUSE_LIBPNG'] = option_value(self.options.png)
        cmake.definitions['wxUSE_LIBJPEG'] = option_value(self.options.jpeg)
        cmake.definitions['wxUSE_LIBTIFF'] = option_value(self.options.tiff)
        cmake.definitions['wxUSE_ZLIB'] = option_value(self.options.zlib)
        cmake.definitions['wxUSE_EXPAT'] = option_value(self.options.expat)
        if self.settings.os != 'Windows':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()
        # If the CMakeLists.txt has a proper install method, the steps below may be redundant
        # If so, you can just remove the lines below
        include_folder = os.path.join(self.source_subfolder, "include")
        self.copy(pattern="*", dst="include", src=include_folder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
