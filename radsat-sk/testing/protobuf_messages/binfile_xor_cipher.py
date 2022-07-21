from os import urandom

"""
-This file contains three function:
    - genkey() : It is used to create an arbitrary key for testing purposes
    - xor_cipher(): It is used to cipher a binary file 
    - xor_decipher(): It is used to decipher a binary file
"""


#random key generating function for testing purposes
def genkey(length):
    """Generate key in bytes"""
    return urandom(length)

#Generate key and store it in a file
key = genkey(10)
try:
        with open("encryption_key",'wb')as file:
            file.write(key)
except:
    print("binary file key was not successfully created")




def xor_cipher(file, key):
    """
    Takes in a binary file, and a encryption key and produces an XOR ciphered text
    * Encryption is done byte by byte
    """

    
    encrypted_binary = [] #list to store the encrypted message 

    #open binary message to be encrypted
    try:
        with open(file,"rb") as f:
            binary_list = list(f.read())
    except:
        print("An error occured with opening the file")

    #perform cipher
    for i in binary_list:
        encrypted_binary.append(i ^key[0])
    #create file to store cipher in the same directory
    try:
        with open("encrypted_msg",'wb')as file:
            file.write(bytes(encrypted_binary))
            
            return binary_list #for testing purposes only
    except:
        print("an error occured with storing the encrypted messaged")



def xor_decipher(file,key):
    decrypted_binary = []
    with open(file,"rb") as f:
        binary_list = list(f.read())

    for i in binary_list:
        decrypted_binary.append(i ^key[0])
    return decrypted_binary

            #Quick test: Insert test bin files
# check1 = xor_cipher("output-onlinefiletools.bin",key)
# check2 = xor_decipher("encrypted_msg",key)

# for i in range(0,len(check1)):
#     if check1[i]!=check2[i]:
#         print("Encryption failed")
#         break
#     else:
#         continue
    
