from interpreter import log_and_embed_coordinates

def test_log_and_embed_coordinates():
    # Paths to the screenshot and template image
    screenshot_path = "screenshot_capture.png"
    template_path = "template_image.png"

    # Perform the log and embed operation
    macro = log_and_embed_coordinates(screenshot_path, template_path)

    # Print the resulting macro
    print("Generated Macro:", macro)

if __name__ == "__main__":
    test_log_and_embed_coordinates()