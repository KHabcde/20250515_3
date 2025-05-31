import win32gui
import difflib

def enum_window_titles():
    def callback(hwnd, titles):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                titles.append(title)

    titles = []
    win32gui.EnumWindows(callback, titles)
    return titles

if __name__ == "__main__":
    window_titles = enum_window_titles()
    print("Currently open window titles:")
    for title in window_titles:
        print(title)

    closest_match = difflib.get_close_matches(arg2, window_titles, n=1, cutoff=0.1)

    if closest_match:
        print(f"\nClosest match: {closest_match[0]}")
    else:
        print("\nNo close match found.")