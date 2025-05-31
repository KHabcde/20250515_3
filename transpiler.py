from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY が設定されていません")

client = OpenAI(api_key=api_key)

def natural_to_macro(text: str) -> str:
    """
    Converts natural language text to macro syntax using OpenAI's ChatGPT API and appends the result to macro_syntax.txt.

    Args:
        text (str): The natural language command.

    Returns:
        str: The converted macro syntax.
    """
    try:
        # Load the prompt template from an external file
        with open("prompt_template.txt", "r", encoding="utf-8") as file:
            prompt_template = file.read()

        # Format the template with the input text
        prompt = f"""
        以下の自然言語指示を、対応するマクロ構文に変換してください。
        自然言語指示: "{text}"
        マクロ構文のみを出力してください。
        出力には余計な記号や装飾を含めないでください。
        
        # 自然言語の例:
        # 「(100,200)をクリックして。」
        # マクロ構文の例:
        # click  100 200

        # 自然言語の例:
        # 画像ファイル「template_image.png」をクリックして。
        # マクロ構文の例:
        # click  image  template_image.png
        
        # 自然言語の例:
        # アプリ「Google Chrome」上のキーワード「green」をクリックして。
        # マクロ構文の例:
        # click  keyword green  Google Chrome
        
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        if not response.choices or not response.choices[0].message.content.strip():
            raise ValueError("Empty response from the API.")

        macro_syntax = response.choices[0].message.content.strip()

        # Ensure two spaces between command and arguments in macro_syntax
        parts = macro_syntax.split(maxsplit=1)
        if len(parts) == 2:
            command, arguments = parts
            arguments_parts = arguments.split(maxsplit=1)
            if len(arguments_parts) == 2:
                macro_syntax = f"{command}  {arguments_parts[0]} {arguments_parts[1]}"

        # Append the macro syntax to macro_syntax.txt
        with open("macro_syntax.txt", "a", encoding="utf-8") as output_file:
            output_file.write(macro_syntax + "\n")

        return macro_syntax
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return "Error: Empty response from the API."
    except Exception as e:
        print(f"Error during API call: {e}")
        return "Error: API call failed."


def parse_macro_line(line: str) -> dict:
    """
    Parses a macro line into its components.

    Args:
        line (str): A single line of macro syntax.

    Returns:
        dict: A dictionary with keys 'cmd', 'arg', 'ext1', 'ext2', 'ext3'.
    """
    parts = line.split('  ')  # Split by two spaces
    keys = ['cmd', 'arg1', 'arg2', 'ext1', 'ext2']  # Adjusted keys to support multiple arguments
    parsed = {key: parts[i] if i < len(parts) else None for i, key in enumerate(keys)}
    return parsed
