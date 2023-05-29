import PyInstaller.__main__

# Change to True when fully tested  # https://pyinstaller.org/en/stable/usage.html#cmdoption-D
BUILD_TO_FOLDER = True

PyInstaller.__main__.run(
    [
        "main.py",
        "--onedir" if BUILD_TO_FOLDER else "--onefile",
        "--icon=assets/images/image.ico",  # https://pyinstaller.org/en/stable/usage.html#cmdoption-i
        # '--noconfirm',  # Enable later - https://pyinstaller.org/en/stable/usage.html#cmdoption-y
        "--log-level=WARN",  # Disable later  # https://pyinstaller.org/en/stable/usage.html#cmdoption-log-level
        "--windowed",  # https://pyinstaller.org/en/stable/usage.html#cmdoption-w
    ]
)
