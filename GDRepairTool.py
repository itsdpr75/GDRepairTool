import base64
import zlib
import argparse

class Crypto:
    def __init__(self, key=11):
        self.key = key

    def xor(self, data):
        return ''.join(chr(b ^ self.key) for b in data)

    def decode(self, data):
        try:
            decoded = self.xor(data)
            decoded = base64.b64decode(decoded)
            return zlib.decompress(decoded).decode('utf-8')
        except Exception as e:
            print(f"Error decoding data: {e}")
            return None

def repair_file(input_path, output_path):
    try:
        with open(input_path, 'rb') as file:
            save_data = file.read()
        
        crypto = Crypto()
        decoded_data = crypto.decode(save_data)
        
        if decoded_data:
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(decoded_data)
            print(f"File repaired and saved as '{output_path}'")
        else:
            print("Failed to repair the file.")
    except FileNotFoundError:
        print("Error! Could not open or find the save file")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Repair Geometry Dash save file")
    parser.add_argument('input', type=str, help="Path to the input CCLocalLevels.dat file")
    parser.add_argument('output', type=str, help="Path to save the repaired XML file")
    
    args = parser.parse_args()
    
    repair_file(args.input, args.output)

if __name__ == "__main__":
    main()