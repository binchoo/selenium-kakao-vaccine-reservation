# -*- mode: python ; coding: utf-8 -*-


block_cipher = None
from os.path import join, dirname, abspath, split
from os import sep
import glob
import seleniumwire

pkg_dir = split(seleniumwire.__file__)[0]
pkg_data = []
pkg_data.extend((file, dirname(file).split("site-packages")[1]) for file in glob.iglob(join(pkg_dir,"**{}*".format(sep)), recursive=True))

a = Analysis(['..\qtmain.py'],
             pathex=['F:\\repositories\\corona-virus-vaccine-reservation'],
             binaries=[],
             datas=pkg_data,
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='qtmain',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
