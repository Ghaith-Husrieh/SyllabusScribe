import re


def extract_list(text):
    lines = text.split('\n')
    extracted_lines = [line for line in lines if re.match(r'^\d', line)]
    result_text = '\n'.join(extracted_lines)
    return result_text
