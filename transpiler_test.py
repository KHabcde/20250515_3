from transpiler import natural_to_macro

def test_natural_to_macro():
    # Example natural language command
    natural_command = "「template_image.png」の位置をクリックして"
    
    # Convert to macro syntax
    macro_syntax = natural_to_macro(natural_command)
    
    # Print the result
    print("Natural Command:", natural_command)
    print("Macro Syntax:", macro_syntax)

if __name__ == "__main__":
    test_natural_to_macro()
