import wave

def encode_aud_data():
    nameoffile = input("Enter name of the file (with extension): ")
    song = wave.open(nameoffile, mode='rb')

    nframes = song.getnframes()
    frames = song.readframes(nframes)
    frame_list = list(frames)
    frame_bytes = bytearray(frame_list)

    data = input("\nEnter the secret message: ")

    # Convert the message to binary
    result = []
    for c in data:
        bits = bin(ord(c))[2:].zfill(8)
        result.extend([int(b) for b in bits])

    # Prefix the binary data with its length (32-bit representation)
    length_bin = format(len(result), '032b')
    result = [int(b) for b in length_bin] + result

    # Embed the bits into the audio frames
    j = 0
    for i in range(len(result)):
        frame_bytes[j] = (frame_bytes[j] & 254) | result[i]
        j += 1

    frame_modified = bytes(frame_bytes)

    stegofile = input("\nEnter name of the stego file (with extension): ")
    with wave.open(stegofile, 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)
    print("\nEncoded the data successfully in the audio file.")
    song.close()

def decode_aud_data():
    nameoffile = input("Enter name of the file to be decoded: ")
    song = wave.open(nameoffile, mode='rb')

    nframes = song.getnframes()
    frames = song.readframes(nframes)
    frame_list = list(frames)
    frame_bytes = bytearray(frame_list)

    # Extract the length of the encoded data (32-bit representation)
    length_bin = ''
    for i in range(32):
        res = bin(frame_bytes[i])[2:].zfill(8)
        length_bin += res[-1]

    length = int(length_bin, 2)

    # Extract the encoded data
    extracted = ''
    for i in range(32, 32 + length):
        res = bin(frame_bytes[i])[2:].zfill(8)
        extracted += res[-1]

    all_bytes = [extracted[i: i + 8] for i in range(0, len(extracted), 8)]
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))

    print("The Encoded data was: ", decoded_data)

def aud_steg():
    while True:
        print("\n\t\tAUDIO STEGANOGRAPHY OPERATIONS")
        print("1. Encode the Text message")
        print("2. Decode the Text message")
        print("3. Exit")
        choice1 = int(input("Enter the Choice: "))
        if choice1 == 1:
            encode_aud_data()
        elif choice1 == 2:
            decode_aud_data()
        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")

# Run the steganography operations
aud_steg()
