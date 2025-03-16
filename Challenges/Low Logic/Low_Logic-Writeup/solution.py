"""Module for parsing input.csv"""
import csv


def read_csv(file_path):
    """Read the CSV file and return the rows of binary inputs."""
    inputs = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            inputs.append({
                'in0': int(row['in0']),
                'in1': int(row['in1']),
                'in2': int(row['in2']),
                'in3': int(row['in3'])
            })
    return inputs


def test_logic_functions(inputs):
    """Test different logic functions on the input data."""
    logic_functions = {
        'in0': lambda row: row['in0'],
        'in1': lambda row: row['in1'],
        'in2': lambda row: row['in2'],
        'in3': lambda row: row['in3'],
        'in0 AND in1': lambda row: row['in0'] & row['in1'],
        'in0 OR in1': lambda row: row['in0'] | row['in1'],
        'in2 AND in3': lambda row: row['in2'] & row['in3'],
        'in2 OR in3': lambda row: row['in2'] | row['in3'],
        'in0 XOR in1': lambda row: row['in0'] ^ row['in1'],
        'in2 XOR in3': lambda row: row['in2'] ^ row['in3'],
        'ALL AND': lambda row: row['in0'] & row['in1'] & row['in2'] & row['in3'],
        'ALL OR': lambda row: row['in0'] | row['in1'] | row['in2'] | row['in3'],
        'ALL XOR': lambda row: row['in0'] ^ row['in1'] ^ row['in2'] ^ row['in3'],
        '(in0 AND in1) OR (in2 AND in3)': lambda row:
            (row['in0'] & row['in1']) | (row['in2'] & row['in3']),
        '(in0 OR in1) AND (in2 OR in3)': lambda row:
            (row['in0'] | row['in1']) & (row['in2'] | row['in3']),
        'MAJORITY': lambda row:
            1 if (row['in0'] + row['in1'] +
                  row['in2'] + row['in3']) >= 2 else 0,
    }

    results = {}
    for name, func in logic_functions.items():
        binary_string = ''.join(str(func(row)) for row in inputs)
        results[name] = binary_string

    return results


def binary_to_ascii(binary_string):
    """Convert a binary string to ASCII text."""
    # Pad the binary string if needed to ensure it's a multiple of 8
    padded_binary = binary_string + '0' * \
        (8 - len(binary_string) %
         8) if len(binary_string) % 8 != 0 else binary_string

    # Convert to bytes and then to ASCII
    ascii_text = ''
    for i in range(0, len(padded_binary), 8):
        byte = padded_binary[i:i+8]
        char_code = int(byte, 2)
        if 32 <= char_code <= 126:  # Printable ASCII range
            ascii_text += chr(char_code)
        else:
            ascii_text += '.'  # Replace non-printable with dot

    return ascii_text


def main():
    # For the actual file, you can use:
    input_data = read_csv('..\hw_lowlogic\input.csv')

    # Test various logic functions
    logic_results = test_logic_functions(input_data)

    # Check each result for readable ASCII
    # print("Testing logic functions for readable output:")
    # for name, binary in logic_results.items():
    #     ascii_text = binary_to_ascii(binary)
    #     if any(flag_marker in ascii_text for flag_marker in ['HTB{', 'Flag', 'flag']):
    #         print(f"\nPOTENTIAL FLAG FOUND in {name}:")
    #         print(f"ASCII: {ascii_text}")
    #     elif any(c.isalpha() for c in ascii_text):
    #         print(f"\n{name}:")
    #         print(f"ASCII Preview: {ascii_text[:20]}...")

    # Specifically check the suspected function
    target_function = '(in0 AND in1) OR (in2 AND in3)'
    if target_function in logic_results:
        binary = logic_results[target_function]
        ascii_text = binary_to_ascii(binary)
        # print(f"\nTarget function '{target_function}':")
        # print(f"Binary: {binary}")
        # print(f"ASCII: {ascii_text}")
        print(ascii_text)


if __name__ == "__main__":
    main()
