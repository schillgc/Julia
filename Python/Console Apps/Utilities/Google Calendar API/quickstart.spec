# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['quickstart.py', 'credentials.json'],
             pathex=['C:\\Users\\bschilling\\Google Drive\\Work\\Current\\Gavin Schilling Marketing\\Operations\\Programming\\Coding\\Development\\GitHub\\Languages\\Python\\Console Apps\\Utilities\\Google Calendar API'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
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
          name='quickstart',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
