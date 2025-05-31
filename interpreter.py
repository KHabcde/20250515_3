import pyautogui
import cv2
import numpy as np
try:
    from pywinauto import Application
except ImportError:
    print("pywinauto is not installed. Some functionalities will be unavailable.")

def execute_macro(parsed_macro: dict):

    """
    Executes a parsed macro command using PyAutoGUI.

    Args:
        parsed_macro (dict): A dictionary containing the parsed macro components.
    """
    cmd = parsed_macro.get('cmd')
    arg1_1 = parsed_macro.get('arg1_1')
    arg1_2 = parsed_macro.get('arg1_2')
    arg2 = parsed_macro.get('arg2')

    if cmd == 'click':
        # Example: click x y (x and y are combined in arg1)
        if arg1_1 and arg1_2 and arg1_1.isdigit() and arg1_2.isdigit():
            try:
                x, y = int(arg1_1), int(arg1_2)
                pyautogui.click(x, y)
            except ValueError:
                print("Error parsing coordinates for 'click' command.")
        elif arg1_1 == 'image' and arg1_2:
            capture_screenshot("screenshot_capture.png")
            result = log_and_embed_coordinates("screenshot_capture.png", str(arg1_2))
            _, x, y = result.split()
            x, y = int(x), int(y)
            pyautogui.click(x, y)
        elif arg1_1 == 'keyword' and arg1_2 and arg2:
            # Example: click keyword keyword_text
            capture_screenshot("screenshot_capture.png")
            try:
                from pywinauto import Application
                from window_title import enum_window_titles
                import difflib
                import sys
                from io import StringIO

                # Get all currently open window titles
                window_titles = enum_window_titles()
                print("Currently open window titles:")
                for title in window_titles:
                    print(title)

                # Find the closest match to arg2
                closest_match = difflib.get_close_matches(arg2, window_titles, n=1, cutoff=0.1)

                if not closest_match:
                    print(f"No close match found for application title: {arg2}")
                    return

                matched_title = closest_match[0]
                print(f"Closest match for application title: {matched_title}")

                # Connect to the application by its matched title
                app = Application().connect(title_re=matched_title)
                print(f"Connected to application: {matched_title}")

                # Get the main window of the application
                main_window = app.w
                indow(title_re=matched_title)
                
                print(f"Main window found: {main_window.window_text()}")

                with open("chrome_ui_info.txt", "w", encoding="utf-8") as file:
                    original_stdout = sys.stdout
                    sys.stdout = StringIO()
                    try:
                        main_window.print_control_identifiers()
                        file.write(sys.stdout.getvalue())
                    finally:
                        sys.stdout = original_stdout
            except Exception as e:
                print(f"Error interacting with application '{arg2}': {e}")
        else:
            print(f"Invalid arguments for 'click' command: arg1='{arg1_1}', arg2='{arg1_2}'")
    else:
        print(f"Command '{cmd}' is not implemented.")

def capture_screenshot(filename: str):
    """
    Captures a screenshot of the current screen and saves it to the specified file.

    Args:
        filename (str): The name of the file to save the screenshot.
    """
    try:
        pyautogui.screenshot(filename)
        print(f"Screenshot saved as {filename}")
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        

def log_and_embed_coordinates(image_path: str, template_path: str):
    """
    Matches a template image within a larger image, logs the coordinates, and embeds them into a macro.

    Args:
        image_path (str): Path to the larger image (e.g., screenshot).
        template_path (str): Path to the template image to match.

    Returns:
        str: A macro string with embedded coordinates, or an error message if no match is found.
    """
    coordinates = match_template(image_path, template_path)
    if coordinates:
        x, y = coordinates
        print(f"Matched coordinates: ({x}, {y})")
        return f"click {x} {y}"
    else:
        print("No match found to embed coordinates.")
        return "Error: No match found."

def match_template(image_path: str, template_path: str) -> tuple:
    """
    Matches a template image within a larger image and returns the coordinates of the match.

    Args:
        image_path (str): Path to the larger image (e.g., screenshot).
        template_path (str): Path to the template image to match.

    Returns:
        tuple: (x, y) coordinates of the center of the matched region, or None if no match is found.
    """
    try:
        # Load the images
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

        if image is None or template is None:
            print("Error: One or both images could not be loaded.")
            return None

        # Perform template matching
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Define a threshold for a good match
        threshold = 0.8
        if max_val >= threshold:
            template_height, template_width = template.shape
            center_x = max_loc[0] + template_width // 2
            center_y = max_loc[1] + template_height // 2
            return (center_x, center_y)
        else:
            print("No match found with sufficient confidence.")
            return None
    except Exception as e:
        print(f"Error during template matching: {e}")
        return None