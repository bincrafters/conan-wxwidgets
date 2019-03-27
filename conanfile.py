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
    exports = ["LICENSE.md", "*.patch"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "fPIC": [True, False],
               "unicode": [True, False],
               "compatibility": ["2.8", "3.0", "3.1"],
               "zlib": [None, "system", "zlib"],
               "png": [None, "system", "libpng"],
               "jpeg": [None, "system", "libjpeg", "libjpeg-turbo", "mozjpeg"],
               "tiff": [None, "system", "libtiff"],
               "expat": [None, "system", "expat"],
               "secretstore": [True, False],
               "aui": [True, False],
               "opengl": [True, False],
               "html": [True, False],
               "mediactrl": [True, False],  # disabled by default as wxWidgets still uses deprecated GStreamer 0.10
               "propgrid": [True, False],
               "debugreport": [True, False],
               "ribbon": [True, False],
               "richtext": [True, False],
               "sockets": [True, False],
               "stc": [True, False],
               "webview": [True, False],
               "xml": [True, False],
               "xrc": [True, False],
               "cairo": [True, False]}
    default_options = "shared=False",\
                      "fPIC=True",\
                      "unicode=True",\
                      "compatibility=3.0",\
                      "zlib=zlib",\
                      "png=libpng",\
                      "jpeg=libjpeg",\
                      "tiff=libtiff",\
                      "expat=expat",\
                      "secretstore=True",\
                      "aui=True",\
                      "opengl=True",\
                      "html=True",\
                      "mediactrl=False",\
                      "propgrid=True",\
                      "debugreport=True",\
                      "ribbon=True",\
                      "richtext=True",\
                      "sockets=True",\
                      "stc=True",\
                      "webview=True",\
                      "xml=True",\
                      "xrc=True",\
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
                packages = ['libx11-dev%s' % arch_suffix,
                            'libgtk2.0-dev%s' % arch_suffix]
                # TODO : GTK3
                # packages.append('libgtk-3-dev%s' % arch_suffix)
                if self.options.secretstore:
                    packages.append('libsecret-1-dev%s' % arch_suffix)
                if self.options.opengl:
                    packages.extend(['mesa-common-dev%s' % arch_suffix,
                                     'libgl1-mesa-dev%s' % arch_suffix])
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
            self.requires.add('Expat/2.2.6@pix4d/stable')

    def source(self):
        source_url = "https://github.com/wxWidgets/wxWidgets"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = "wxWidgets-" + self.version
        os.rename(extracted_dir, self.source_subfolder)
        tools.patch(self.source_subfolder, "424f64f27d94f83ed946ebfcf9b9543c828f9f25.patch")

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

        # generic build options
        cmake.definitions['wxBUILD_SHARED'] = self.options.shared
        cmake.definitions['wxBUILD_SAMPLES'] = 'OFF'
        cmake.definitions['wxBUILD_TESTS'] = 'OFF'
        cmake.definitions['wxBUILD_DEMOS'] = 'OFF'
        cmake.definitions['wxBUILD_INSTALL'] = True
        cmake.definitions['wxBUILD_COMPATIBILITY'] = self.options.compatibility
        if self.settings.compiler == 'clang':
            cmake.definitions['wxBUILD_PRECOMP'] = 'OFF'

        # platform-specific options
        if self.settings.compiler == 'Visual Studio':
            cmake.definitions['wxBUILD_USE_STATIC_RUNTIME'] = 'MT' in str(self.settings.compiler.runtime)
            cmake.definitions['wxBUILD_MSVC_MULTIPROC'] = True
        if self.settings.os != 'Windows':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        if self.settings.os == 'Linux':
            # TODO : GTK3
            # cmake.definitions['wxBUILD_TOOLKIT'] = 'gtk3'
            cmake.definitions['wxUSE_CAIRO'] = self.options.cairo

        # 3rd-party libraries
        cmake.definitions['wxUSE_LIBPNG'] = option_value(self.options.png)
        cmake.definitions['wxUSE_LIBJPEG'] = option_value(self.options.jpeg)
        cmake.definitions['wxUSE_LIBTIFF'] = option_value(self.options.tiff)
        cmake.definitions['wxUSE_ZLIB'] = option_value(self.options.zlib)
        cmake.definitions['wxUSE_EXPAT'] = option_value(self.options.expat)

        # wxWidgets features
        cmake.definitions['wxUSE_UNICODE'] = self.options.unicode
        cmake.definitions['wxUSE_SECRETSTORE'] = self.options.secretstore

        # wxWidgets libraries
        cmake.definitions['wxUSE_AUI'] = self.options.aui
        cmake.definitions['wxUSE_OPENGL'] = self.options.opengl
        cmake.definitions['wxUSE_HTML'] = self.options.html
        cmake.definitions['wxUSE_MEDIACTRL'] = self.options.mediactrl
        cmake.definitions['wxUSE_PROPGRID'] = self.options.propgrid
        cmake.definitions['wxUSE_DEBUGREPORT'] = self.options.debugreport
        cmake.definitions['wxUSE_RIBBON'] = self.options.ribbon
        cmake.definitions['wxUSE_RICHTEXT'] = self.options.richtext
        cmake.definitions['wxUSE_SOCKETS'] = self.options.sockets
        cmake.definitions['wxUSE_STC'] = self.options.stc
        cmake.definitions['wxUSE_WEBVIEW'] = self.options.webview
        cmake.definitions['wxUSE_XML'] = self.options.xml
        cmake.definitions['wxUSE_XRC'] = self.options.xrc

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
        self.copy(pattern='*setup.h', dst=os.path.join('include', 'wx'), src=os.path.join(self.build_subfolder, 'lib'),
                  keep_path=False)

    def package_info(self):
        version_tokens = self.version.split('.')
        version_major = version_tokens[0]
        version_minor = version_tokens[1]
        unicode = 'u' if self.options.unicode else ''
        debug = 'd' if self.settings.build_type == 'Debug' else ''
        if self.settings.os == 'Linux':
            prefix = 'wx_'
            toolkit = 'gtk2'
            version = ''
            suffix = '-%s.%s' % (version_major, version_minor)
        elif self.settings.os == 'Macos':
            prefix = 'wx_'
            toolkit = 'osx_cocoa'
            version = ''
            suffix = '-%s.%s' % (version_major, version_minor)
        elif self.settings.os == 'Windows':
            prefix = 'wx'
            toolkit = 'msw'
            version = '%s%s' % (version_major, version_minor)
            suffix = ''

        def base_library_pattern(library):
            return '{prefix}base{version}{unicode}{debug}_%s{suffix}' % library

        def library_pattern(library):
            return '{prefix}{toolkit}{version}{unicode}{debug}_%s{suffix}' % library

        libs = ['{prefix}base{version}{unicode}{debug}{suffix}',
                library_pattern('core'),
                library_pattern('adv')]
        if self.options.sockets:
            libs.append(base_library_pattern('net'))
        if self.options.xml:
            libs.append(base_library_pattern('xml'))
        if self.options.aui:
            libs.append(library_pattern('aui'))
        if self.options.opengl:
            libs.append(library_pattern('gl'))
        if self.options.html:
            libs.append(library_pattern('html'))
        if self.options.mediactrl:
            libs.append(library_pattern('media'))
        if self.options.propgrid:
            libs.append(library_pattern('propgrid'))
        if self.options.debugreport:
            libs.append(library_pattern('qa'))
        if self.options.ribbon:
            libs.append(library_pattern('ribbon'))
        if self.options.richtext:
            libs.append(library_pattern('richtext'))
        if self.options.stc:
            if not self.options.shared:
                scintilla_suffix = '{debug}' if self.settings.os == "Windows" else '{suffix}'
                libs.append('wxscintilla' + scintilla_suffix)
            libs.append(library_pattern('stc'))
        if self.options.webview:
            libs.append(library_pattern('webview'))
        if self.options.xrc:
            libs.append(library_pattern('xrc'))
        for lib in reversed(libs):
            self.cpp_info.libs.append(lib.format(prefix=prefix,
                                                 toolkit=toolkit,
                                                 version=version,
                                                 unicode=unicode,
                                                 debug=debug,
                                                 suffix=suffix))

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
        elif self.settings.os == 'Macos':
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
        elif self.settings.os == 'Windows':
            # see cmake/init.cmake
            compiler_prefix = {'Visual Studio': 'vc',
                               'gcc': 'gcc',
                               'clang': 'clang'}.get(str(self.settings.compiler))

            arch_suffix = '_x64' if self.settings.compiler == 'Visual Studio' and self.settings.arch == 'x86_64' else ''
            # use the following code in next release:
            # arch_suffix = '_x64' if self.settings.arch == 'x86_64' else ''
            lib_suffix = '_dll' if self.options.shared else '_lib'
            libdir = '%s%s%s' % (compiler_prefix, arch_suffix, lib_suffix)
            libdir = os.path.join('lib', libdir)
            self.cpp_info.bindirs.append(libdir)
            self.cpp_info.libdirs.append(libdir)
            self.cpp_info.defines.append('__WXMSW__')
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
            # Link a few libraries that are needed when using gcc on windows
            if self.settings.compiler == 'gcc':
                self.cpp_info.libs.extend(['uxtheme',
                                           'version',
                                           'shlwapi',
                                           'oleacc'])
        if self.settings.compiler == 'Visual Studio':
            self.cpp_info.includedirs.append(os.path.join('include', 'msvc'))
