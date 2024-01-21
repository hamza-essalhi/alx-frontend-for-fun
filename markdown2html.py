import sys
import os

def convert_markdown_to_html(markdown_file, output_file):
    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    with open(markdown_file, 'r') as md_file, open(output_file, 'w') as html_file:
        html_file.write(md_file.read())

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py <markdown_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        convert_markdown_to_html(markdown_file, output_file)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)

