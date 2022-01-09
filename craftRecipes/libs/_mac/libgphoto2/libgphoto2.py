# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['2.5.27']:
            self.targets[ver] = 'https://downloads.sourceforge.net/project/gphoto/libgphoto/' + ver + '/libgphoto2-' + ver +  '.tar.bz2'
            self.archiveNames[ver] = "libgphoto2-%s.tar.gz" % ver
            self.targetInstSrc[ver] = 'libgphoto2-' + ver
        self.description = 'Gphoto2 digital camera library'
        self.defaultTarget = '2.5.27'

    def setDependencies(self):
        self.buildDependencies["libs/gettext"] = None
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/_mac/libusb-compat"] = None
        #gd and libexif might be needed too

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def fixLibraryFolder(self, folder):
        root = str(CraftCore.standardDirs.craftRoot())
        craftLibDir = os.path.join(root,  'lib')
        for library in utils.filterDirectoryContent(str(folder)):
            for path in utils.getLibraryDeps(str(library)):
                if path.startswith(craftLibDir):
                    utils.system(["install_name_tool", "-change", path, os.path.join("@rpath", os.path.basename(path)), library])
            if library.endswith(".dylib"):
                utils.system(["install_name_tool", "-id", os.path.join("@rpath", os.path.basename(path)), library])
            utils.system(["install_name_tool", "-add_rpath", craftLibDir, library])

    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )
        prefix = str(self.shell.toNativePath(CraftCore.standardDirs.craftRoot()))
       	self.subinfo.options.configure.autoreconf = False
       	self.subinfo.options.useShadowBuild = False
        self.subinfo.options.configure.args += " --disable-dependency-tracking" \
        " --disable-silent-rules" \
        " --prefix=" + prefix

    def install(self):
        ret = AutoToolsPackageBase.install(self)
        if OsUtils.isMac():
            self.fixLibraryFolder(os.path.join(self.imageDir(), "lib"))
            self.fixLibraryFolder(os.path.join(self.imageDir(), "lib", "libgphoto2", "2.5.27"))
            self.fixLibraryFolder(os.path.join(self.imageDir(), "lib", "libgphoto2_port", "0.12.0"))
        return ret



