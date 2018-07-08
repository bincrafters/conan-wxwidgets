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
               "jpeg": [None, "system", "libjpeg", "libjpeg-turbo", "mozjpeg"],
               "tiff": [None, "system", "libtiff"],
               "expat": [None, "system", "expat"],
               "secretstore": [True, False],
               "opengl": [True, False],
               "webview": [True, False],
               "mediactrl": [True, False],  # disabled by default as wxWidgets still uses deprecated GStreamer 0.10
               "cairo": [True, False]}
    default_options = "shared=False",\
                      "fPIC=True",\
                      "zlib=zlib",\
                      "png=libpng",\
                      "jpeg=libjpeg",\
                      "tiff=libtiff",\
                      "expat=expat",\
                      "secretstore=True",\
                      "opengl=True",\
                      "webview=True",\
                      "mediactrl=False",\
                      "cairo=True"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC
        if self.settings.os != 'Linux':
            self.options.remove('cairo')

    def system_requirements(self):
        if self.settings.os == 'Linux' and tools.os_info.is_linux:
            if tools.os_info.with_apt:
                installer = tools.SystemPackageTool()
                if self.settings.arch == 'x86':
                    arch_suffix = ':i386'
                elif self.settings.arch == 'x86_64':
                    arch_suffix = ':amd64'
                packages = ['libx11-dev%s' % arch_suffix]
                packages.append('libgtk2.0-dev%s' % arch_suffix)
                # TODO : GTK3
                # packages.append('libgtk-3-dev%s' % arch_suffix)
                if self.options.secretstore:
                    packages.append('libsecret-1-dev%s' % arch_suffix)
                if self.options.opengl:
                    packages.append('mesa-common-dev%s' % arch_suffix)
                if self.options.webview:
                    packages.extend(['libsoup2.4-dev%s' % arch_suffix,
                                     'libwebkitgtk-dev%s' % arch_suffix])
                # TODO : GTK3
                #                    'libwebkitgtk-3.0-dev%s' % arch_suffix])
                if self.options.mediactrl:
                    packages.extend(['libgstreamer0.10-dev%s' % arch_suffix,
                                     'libgstreamer-plugins-base0.10-dev%s' % arch_suffix])
                if self.options.cairo:
                    packages.append('libcairo2-dev%s' % arch_suffix)
                for package in packages:
                    installer.install(package)

    def requirements(self):
        if self.options.png == 'libpng':
            self.requires.add('libpng/1.6.34@bincrafters/stable')
        if self.options.jpeg == 'libjpeg':
            self.requires.add('libjpeg/9c@bincrafters/stable')
        elif self.options.jpeg == 'libjpeg-turbo':
            self.requires.add('libjpeg-turbo/1.5.2@bincrafters/stable')
        elif self.options.jpeg == 'mozjpeg':
            self.requires.add('mozjpeg/3.3.1@bincrafters/stable')
        if self.options.tiff == 'libtiff':
            self.requires.add('libtiff/4.0.9@bincrafters/stable')
        if self.options.zlib == 'zlib':
            self.requires.add('zlib/1.2.11@conan/stable')
        if self.options.expat == 'expat':
            self.requires.add('expat/2.2.5@bincrafters/stable')

    def source(self):
        source_url = "https://github.com/wxWidgets/wxWidgets"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = "wxWidgets-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def add_libraries_from_pc(self, library):
        pkg_config = tools.PkgConfig(library)
        libs = [lib[2:] for lib in pkg_config.libs_only_l]  # cut -l prefix
        lib_paths = [lib[2:] for lib in pkg_config.libs_only_L]  # cut -L prefix
        self.cpp_info.libs.extend(libs)
        self.cpp_info.libdirs.extend(lib_paths)
        self.cpp_info.sharedlinkflags.extend(pkg_config.libs_only_other)
        self.cpp_info.exelinkflags.extend(pkg_config.libs_only_other)

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

        cmake.definitions['wxUSE_SECRETSTORE'] = self.options.secretstore
        cmake.definitions['wxUSE_OPENGL'] = self.options.opengl
        cmake.definitions['wxUSE_WEBVIEW'] = self.options.webview
        cmake.definitions['wxUSE_MEDIACTRL'] = self.options.mediactrl
        if self.settings.os != 'Windows':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        if self.settings.os == 'Linux':
            # TODO : GTK3
            # cmake.definitions['wxBUILD_TOOLKIT'] = 'gtk3'
            cmake.definitions['wxUSE_CAIRO'] = self.options.cairo
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()
        # copy setup.h
        self.copy(pattern='*setup.h', dst=os.path.join('include', 'wx'), src=os.path.join(self.build_subfolder, 'lib'), keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.defines.append('wxUSE_GUI=1')
        if self.settings.build_type == 'Debug':
            self.cpp_info.defines.append('__WXDEBUG__')
        if self.options.shared:
            self.cpp_info.defines.append('WXUSINGDLL')
        if self.settings.os == 'Linux':
            self.cpp_info.defines.append('__WXGTK__')
            self.add_libraries_from_pc('gtk+-2.0')
            self.add_libraries_from_pc('x11')
            self.cpp_info.libs.extend(['dl', 'pthread'])
        if self.settings.os == 'Macos':
            self.cpp_info.defines.extend(['__WXMAC__', '__WXOSX__', '__WXOSX_COCOA__'])
            for framework in ['Carbon',
                              'Cocoa',
                              'AudioToolbox',
                              'OpenGL',
                              'AVKit',
                              'AVFoundation',
                              'Foundation',
                              'IOKit',
                              'ApplicationServices',
                              'CoreText',
                              'CoreGraphics',
                              'CoreServices',
                              'CoreMedia',
                              'Security',
                              'ImageIO',
                              'System',
                              'WebKit']:
                self.cpp_info.exelinkflags.append('-framework %s' % framework)
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
        if self.settings.compiler == 'Visual Studio':
            self.cpp_info.defines.append('__WXMSW__')
            self.cpp_info.includedirs.append(os.path.join('include', 'msvc'))
            if self.settings.arch == 'x86_64':
                libdir = 'vx_x64_dll' if self.options.shared else 'vc_x64_lib'
                self.cpp_info.libdirs.append(os.path.join('lib', libdir))
            elif self.settings.arch == 'x86':
                libdir = 'vx_dll' if self.options.shared else 'vc_lib'
                self.cpp_info.libdirs.append(os.path.join('lib', libdir))
            # disable annoying auto-linking
            self.cpp_info.defines.extend(['wxNO_NET_LIB',
                                          'wxNO_XML_LIB',
                                          'wxNO_REGEX_LIB',
                                          'wxNO_ZLIB_LIB',
                                          'wxNO_JPEG_LIB',
                                          'wxNO_PNG_LIB',
                                          'wxNO_TIFF_LIB',
                                          'wxNO_ADV_LIB',
                                          'wxNO_HTML_LIB',
                                          'wxNO_GL_LIB',
                                          'wxNO_QA_LIB',
                                          'wxNO_XRC_LIB',
                                          'wxNO_AUI_LIB',
                                          'wxNO_PROPGRID_LIB',
                                          'wxNO_RIBBON_LIB',
                                          'wxNO_RICHTEXT_LIB',
                                          'wxNO_MEDIA_LIB',
                                          'wxNO_STC_LIB',
                                          'wxNO_WEBVIEW_LIB'])
            self.cpp_info.libs.extend(['kernel32',
                                       'user32',
                                       'gdi32',
                                       'comdlg32',
                                       'winspool',
                                       'shell32',
                                       'comctl32',
                                       'ole32',
                                       'oleaut32',
                                       'uuid',
                                       'wininet',
                                       'rpcrt4',
                                       'winmm',
                                       'advapi32',
                                       'wsock32'])
