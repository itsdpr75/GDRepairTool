import base64
import zlib
import argparse

class Crypto:
    def __init__(self, key=11):
        self.key = key

    def xor(self, data):
        try:
            xor_data = ''.join(chr(b ^ self.key) for b in data)
            return xor_data
        except Exception as e:
            print(f"Error applying XOR: {e}")
            raise

    def decode(self, data):
        try:
            decoded = self.xor(data)
            print(f"Decoded (XOR Applied): {decoded[:1000]}...")  # Print the first 1000 characters for debugging
            
            # Check if the decoded string looks like base64 data
            try:
                decoded_base64 = base64.b64decode(decoded, validate=True)
            except Exception as e:
                print(f"Base64 decoding error: {e}")
                return None
            
            try:
                decompressed_data = zlib.decompress(decoded_base64).decode('utf-8')
                return decompressed_data
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