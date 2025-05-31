from interpreter import match_template

def test_template_matching():
    # Paths to the screenshot and template image
    screenshot_path = "screenshot_capture.png"
    template_path = "template_image.png"

    # Perform template matching
    result = match_template(screenshot_path, template_path)

    if result:
        print(f"Template matched at coordinates: {result}")
    else:
        print("Template matching failed.")

if __name__ == "__main__":
    test_template_matching()