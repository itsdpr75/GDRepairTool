import base64
import zlib
import os
import struct

def xor_decrypt(data: bytes, key: int) -> bytes:
    return bytes([byte ^ key for byte in data])

def decode_data(data: str) -> bytes:
    try:
        # Decodifica el Base64
        base64_decoded = base64.b64decode(data)
    except (base64.binascii.Error, ValueError) as e:
        raise ValueError(f"Base64 decoding error: {e}")
    
    # Aplica XOR
    xor_decoded = xor_decrypt(base64_decoded, 11)
    
    # Descomprime los datos
    try:
        return zlib.decompress(xor_decoded)
    except zlib.error as e:
        raise ValueError(f"Zlib decompression error: {e}")

def extract_levels(input_path: str, output_dir: str):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(input_path, 'rb') as file:
        data = file.read()
    
    # Asume que el archivo está en formato texto y lo decodifica
    try:
        data_str = data.decode('utf-8')
    except UnicodeDecodeError as e:
        print(f"Error decoding file as UTF-8: {e}")
        return
    
    try:
        decoded_data = decode_data(data_str)
    except ValueError as e:
        print(f"Error decoding data: {e}")
        return
    
    # Procesa los datos decodificados. El siguiente código es un ejemplo básico.
    # Dependiendo del formato real, es posible que necesites ajustar esto.
    
    # Ejemplo: Extraer niveles que están delimitados en el archivo
    offset = 0
    level_counter = 0
    
    while offset < len(decoded_data):
        # Leer tamaño del nivel (suponiendo que cada nivel tiene un tamaño prefijado o delimitador)
        if offset + 4 > len(decoded_data):
            break
        
        try:
            level_size = struct.unpack_from('<I', decoded_data, offset)[0]
            offset += 4
            
            if offset + level_size > len(decoded_data):
                break
            
            level_data = decoded_data[offset:offset + level_size]
            offset += level_size
            
            # Guardar nivel en formato .gmd
            level_path = os.path.join(output_dir, f'level_{level_counter}.gmd')
            with open(level_path, 'wb') as level_file:
                level_file.write(level_data)
            
            print(f"Level extracted and saved to {level_path}")
            level_counter += 1
        
        except (struct.error, IndexError) as e:
            print(f"Error processing level data: {e}")
            break

# Cambia las rutas a las ubicaciones correctas
input_file = '/storage/emulated/0/GDRepairTool/CCLocalLevels.dat'
output_directory = '/storage/emulated/0/GDRepairTool/extracted_levels'

extract_levels(input_file, output_directory)