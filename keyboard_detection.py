import msvcrt
def check_if_pressing_v() -> bool:
  if msvcrt.kbhit():
    key = msvcrt.getch()
    if key == b"v":
       return True
    return False
  return False

if __name__ == "__main__":
    while True:
        is_pressing_v = check_if_pressing_v()
        if is_pressing_v:
            print("Pressing V!")