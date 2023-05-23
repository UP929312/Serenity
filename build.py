import PyInstaller.__main__
PyInstaller.__main__.run([
    'main.py',
    '--onedir',  # Change to --onefile for single executable when fully tested
    '--icon="assets/images/image.ico'
])