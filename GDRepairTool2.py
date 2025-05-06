import base64
import zlib
import argparse

class Crypto:
    def __init__(self, key=11):
        self.key = key

    def xor(self, data):
        try:
            return ''.join(chr(b ^ self.key) for b in data)
        except Exception as e:
            print(f"Error applying XOR: {e}")
            raise

    def decode(self, data):
        try:
            decoded = self.xor(data)
            decoded = base64.b64decode(decoded, validate=True)
            return zlib.decompress(decoded).decode('utf-8')
        except base64.binascii.Error as e:
            print(f"Base64 decoding error: {e}")
            return None
        except zlib.error as e:
            print(f"Zlib decompression error: {e}")
            return None
        except Exception as e:
            print(f"General decoding error: {e}")
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
            print("Failed to repair the file. Check the input file and try again.")
    except FileNotFoundError:
        print("Error! Could not open or find the save file.")
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