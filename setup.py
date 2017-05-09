from distutils.core import setup, Extension
import os
import subprocess
import re

scorep_config = "/opt/scorep/TRY_READEX_online_access_call_tree_extensions_r11730_mpich_gcc6.2.0/bin/scorep-config"

ldflage =   subprocess.run([scorep_config,"--nocompiler", "--user", "--ldflags"], stdout=subprocess.PIPE).stdout
libs =      subprocess.run([scorep_config,"--nocompiler", "--user", "--libs"], stdout=subprocess.PIPE).stdout
cflags =    subprocess.run([scorep_config,"--nocompiler", "--user", "--cflags"], stdout=subprocess.PIPE).stdout
 
scorep_adapter_init = subprocess.run([scorep_config,"--nocompiler", "--user", "--adapter-init"], stdout=subprocess.PIPE).stdout
 
libs        = libs.decode("utf-8")
ldflage     = ldflage.decode("utf-8")
cflags      = cflags.decode("utf-8")

scorep_adapter_init = scorep_adapter_init.decode("utf-8")


lib_dir = re.findall("-L[/.\w]*",ldflage)
lib     = re.findall("-l[/.\w]*",libs)
include = re.findall("-I[/.\w]*",cflags)
macro   = re.findall("-D[/.\w]*",cflags)

remove_flag = lambda x: x[2:]

lib_dir = list(map(remove_flag, lib_dir))
lib     = list(map(remove_flag, lib))
include = list(map(remove_flag, include))
macro   = list(map(remove_flag, macro))

macro   = list(map(lambda x: tuple([x,1]), macro))
    

with open("./scorep_init.c","w") as f:
    f.write(scorep_adapter_init)

module1 = Extension('scorep',
                    include_dirs = include,
                    libraries = lib,
                    library_dirs = lib_dir,
                    define_macros = macro,
                    sources = ['scorep.c',"scorep_init.c"])

setup (name = 'scorep',
       version = '0.1',
       description = 'This is a scorep demo package',
       author = 'Andreas Gocht',
       author_email = 'andreas.gocht@tu-dresden.de',
       url = '',
       long_description = '''
This is really just a scorep demo package.
''',
       ext_modules = [module1])
