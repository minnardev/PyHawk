"""
🦅 PyHawk Code Formatter
Formats Hawk source code with consistent indentation, clean block structure,
and normalized whitespace.
"""

import re


def format_code(source: str, indent_size: int = 4) -> str:
    lines = source.splitlines()
    indent_unit = " " * indent_size
    formatted_lines = []
    
    current_indent = 0
    blank_line_count = 0

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Handle blank lines
        if not line:
            blank_line_count += 1
            # Allow at most 1 blank line between code blocks
            if blank_line_count <= 1 and formatted_lines:
                formatted_lines.append("")
            i += 1
            continue

        blank_line_count = 0

        # Optional: join standalone 'else' or 'else {' with preceding line if it ended with '}'
        if (line.startswith("else ") or line.startswith("else{") or line == "else") and formatted_lines:
            prev_line = formatted_lines[-1]
            if prev_line.endswith("}"):
                # Merge into "} else ..."
                formatted_lines[-1] = prev_line + " " + line
                # Recalculate opening/closing braces on this merged line
                # Since the previous '}' already decremented current_indent,
                # we just need to see if 'else {' opens a new brace:
                opens = line.count("{") + line.count("[")
                closes = line.count("}") + line.count("]")
                current_indent += (opens - closes)
                i += 1
                continue

        # Count braces and brackets on the current line (ignoring strings and comments)
        clean_line = _strip_strings_and_comments(line)
        opens = clean_line.count("{") + clean_line.count("[")
        closes = clean_line.count("}") + clean_line.count("]")

        # Check if line starts with closing brace or bracket
        starts_with_close = line.startswith("}") or line.startswith("]")
        if line.startswith("else") and not starts_with_close:
            # Standalone else on newline takes outer indent
            line_indent = max(0, current_indent - 1)
        elif starts_with_close:
            line_indent = max(0, current_indent - 1)
        else:
            line_indent = current_indent

        # Format line with proper indentation
        formatted_lines.append(f"{indent_unit * line_indent}{line}")

        # Update indent level for following lines
        current_indent = max(0, current_indent + (opens - closes))
        i += 1

    # Ensure single trailing newline
    result = "\n".join(formatted_lines).strip()
    return result + "\n" if result else ""


def _strip_strings_and_comments(line: str) -> str:
    """Removes string literals and comments so braces inside them don't affect indentation."""
    # Remove strings
    no_strings = re.sub(r'"([^"\\]|\\.)*"', '""', line)
    # Remove comments # or //
    no_comments = re.sub(r'(#|//).*$', '', no_strings)
    return no_comments
