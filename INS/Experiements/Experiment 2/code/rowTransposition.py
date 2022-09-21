def row_encrypt(text,key):
    incompleteReplacedString = '_'*(len(key)-(len(text)%len(key)))
    updatedString = text + incompleteReplacedString

    sortedKeyWord = sorted(key)
    
    matrix = []

    while(len(updatedString)!=0):
        matrix.append(updatedString[:len(key)])
        updatedString=updatedString[len(key):]

    key2 = list(key)

    encryptMatrix = []
    for i in matrix:
        encryptMatrix.append("")

    for i in range(len(sortedKeyWord)):
        index = key2.index(sortedKeyWord[i])
        for j in range(len(matrix)):
            letter = matrix[j][index:index+1]
            encryptMatrix[j] = encryptMatrix[j]+letter

    return "".join(encryptMatrix)

def row_decrypt(cipher,key):

    matrix = []
    while(len(cipher)!=0):
        matrix.append(cipher[:len(key)])
        cipher=cipher[len(key):]

    cipher = []
    for i in matrix:
        cipher.append("")

    key2 = list(key)
    sortedKeyWord = sorted(key)

    for i in range(len(key2)):
        index = sortedKeyWord.index(key2[i])
        for j in range(len(matrix)):
            letter = matrix[j][index:index+1]
            cipher[j] = cipher[j]+letter

    return ("".join(cipher)).replace("_","")

text = input("Enter word to be encrypted: ")
key = input("Enter key: ")
cipher = row_encrypt(text,key)
print("Encrypted Word is: ",cipher)
print("Decrypted Word is: ",row_decrypt(cipher,key))
