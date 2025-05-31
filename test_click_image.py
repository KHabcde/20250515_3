from transpiler import parse_macro_line
from interpreter import execute_macro

def test_click_image():
    # Example macro line for clicking an image
    macro_line = "click image  screenshot_capture.png"  # Already uses two spaces

    # Parse the macro line
    parsed_macro = parse_macro_line(macro_line)
    print("Parsed Macro:", parsed_macro)

    # Execute the macro
    execute_macro(parsed_macro)

if __name__ == "__main__":
    test_click_image()
