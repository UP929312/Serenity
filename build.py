import PyInstaller.__main__

PyInstaller.__main__.run(
    [
        "main.py",
        "--onedir",  # Change to --onefile for single executable when fully tested  # https://pyinstaller.org/en/stable/usage.html#cmdoption-D
        "--icon=assets/images/image.ico",  # https://pyinstaller.org/en/stable/usage.html#cmdoption-i
        # '--noconfirm',  # Enable later - https://pyinstaller.org/en/stable/usage.html#cmdoption-y
        "--log-level=WARN",  # Disable later  # https://pyinstaller.org/en/stable/usage.html#cmdoption-log-level
        "--windowed",  # https://pyinstaller.org/en/stable/usage.html#cmdoption-w
    ]
)
