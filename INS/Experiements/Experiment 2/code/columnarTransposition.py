def columnar_encrypt(text,key):
    # Adding _ to the difference place
    incompleteReplacedString = '_'*(len(key)-(len(text)%len(key)))
    updatedString = text + incompleteReplacedString
    sortedKeyWord = sorted(key)
    
    matrix = []

    while(len(updatedString)!=0):
        matrix.append(updatedString[:len(key)])
        updatedString=updatedString[len(key):]
    keyWord2 = list(key)

    cipher = ""
    for i in sortedKeyWord:
        index = keyWord2.index(i)
        for j in range(len(matrix)):
            cipher += matrix[j][index:index+1] 
            matrix[j] = matrix[j][:index]+matrix[j][index+1:]
        keyWord2.remove(i) 

    return cipher

def columnar_decrypt(cipher,key):
    sortedKeyWord = sorted(key)

    matrix = []
    noOfRows = len(cipher)//len(key)
    while(len(cipher)!=0):
        matrix.append(cipher[:noOfRows])
        cipher=cipher[noOfRows:]

    decryptedText=""
    newMatrix = []
    for i in key:
        index = sortedKeyWord.index(i)
        newMatrix.append(matrix[index])

    for i in range(noOfRows):
        for j in range(len(newMatrix)):
            decryptedText = decryptedText + newMatrix[j][i]

    return decryptedText.replace("_","")


text = input("Enter word to be encrypted: ").upper()
key = input("Enter key: ").upper()
cipher = columnar_encrypt(text,key)
print("Encrypted Word is: ",cipher)
print("Decrypted Word is: ",columnar_decrypt(cipher,key))