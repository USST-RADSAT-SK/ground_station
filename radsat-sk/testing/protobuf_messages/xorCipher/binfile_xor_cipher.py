from os import urandom

"""
-This file contains three function:
    - genkey() : It is used to create an arbitrary key for testing purposes -- Uncomment it when you want to generate a key
    - xor_cipher(): It is used to cipher a binary file 
    - xor_decipher(): It is used to decipher a binary file
"""


#random key generating function for testing purposes
# def genkey(length):
#     """Generate key in bytes"""
#     return urandom(length)

# #Generate key and store it in a file
# key = genkey(10)
# try:
#         with open("encryption_key",'wb')as file:
#             file.write(key)
# except:
#     print("binary file key was not successfully created")




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

     #open key to use for cipher
    try:
        with open(key,"rb") as f:
            k = f.read()
    except:
        print("An error occured with opening the file")

    #perform cipher
    for i in binary_list:
        encrypted_binary.append(i ^k[0])
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

     #open key to use for cipher
    try:
        with open(key,"rb") as f:
            k = f.read()
    except:
        print("An error occured with opening the file")

    for i in binary_list:
        decrypted_binary.append(i ^k[0])
    return decrypted_binary

            #Quick test: Insert test bin files
# check1 = xor_cipher("output-onlinefiletools.bin","encryption_key")
# check2 = xor_decipher("encrypted_msg","encryption_key")
# print(check1)
# print(check2)
# for i in range(0,len(check1)):
#     if check1[i]!=check2[i]:
#         print("Encryption failed")
#         break
#     else:
#         continue
    
