import json, random

def loadJson(filename):
    with open(filename,'r') as json_file:
        data = json.load(json_file)
    return data

def writeJson(dictionary, filename):
    with open(filename,'w') as json_out:
        json.dump(dictionary, json_out)

def loadTxtFile(dictionary_filename, answers_filename, output_json_filename):
    dictionary = {}
    with open(dictionary_filename,'r') as f:
        lines = f.read().splitlines()
    dictionary['dictionary'] = lines
    with open(answers_filename,'r') as f:
        lines = f.read().splitlines()
    dictionary['answers'] = lines
    writeJson(output_json_filename, 'userdata.json')

def getUserInput(answer, dictionary, unused_letters, wrong_positioned_letters, correct_positioned_letters):
    while True:
        guess = input("YOUR WORD: ").upper()
        if len(guess) != 5:
            print("Enter a 5 letter word.")
        else:
            if guess.lower() not in dictionary['dictionary']:
                print("Enter a valid word.")
            else:
                return wordCheck(guess, answer, unused_letters, wrong_positioned_letters, correct_positioned_letters)

def wordCheck(guess, word, unused_letters, wrong_positioned_letters, correct_positioned_letters):
    '''Checks if the guessed word is equal to word. returns 1 if win, 0 if wrong. Also handles printing of data.'''
    if guess == word:
        return 1,0,0,0
    else:
        guess = list(guess.strip(" "))
        word = list(word.upper().strip(" "))
        display_word = guess[:]
        # Correct Position, Correct Letter
        for i in range(0,5):
            if guess[i] == word[i]:
                if f"{guess[i]} at pos {i+1}" not in correct_positioned_letters:
                    correct_positioned_letters.append(f"{guess[i]} at pos {i+1}")
                guess[i] = '!'
                word[i] = '!'
        # Correct Letter, Incorrect Position
        for letter in word:
            if letter.isalpha():
                if letter in guess:
                    idx = guess.index(letter)
                    if f"{letter} not in pos {idx+1}" not in wrong_positioned_letters:
                        wrong_positioned_letters.append(f"{letter} not in pos {idx+1}")
                    guess[idx] = '*'
        # Remove Unwanted Characters
        for i in range(0,5):
            if guess[i].isalpha():
                if guess[i] in unused_letters:
                    unused_letters.remove(guess[i])
                guess[i] = '-'
        # print(f"Possible letters: {unused_letters}")
        print(f"Wrong Positions: {wrong_positioned_letters}")
        print(f"Correct Letters: {correct_positioned_letters}")
        print(display_word)
        print(guess)
        return 0, unused_letters, wrong_positioned_letters, correct_positioned_letters
        

def fetchWord(dictionary):
    # Optional: Remove ones answered already
    return random.choice(dictionary['answers'])

def checkWin(round, numGuess):
    if round:
        print("You Win!")
        return 10
    else:
        return numGuess + 1

def startGame():
    print("Welcome to WORDLE!")
    unused_letters = ["A","E","I","O","U","B","C","D","F","G","H","J","K","L","M","N","P","Q","R","S","T","V","W","X","Y","Z"]
    wrong_positioned_letters = []
    correct_positioned_letters = []
    dictionary = loadJson('userdata.json')
    numGuess = 0
    answer = fetchWord(dictionary)
    while numGuess < 6:
        round, unused_letters, wrong_positioned_letters, correct_positioned_letters = getUserInput(answer, dictionary, unused_letters, wrong_positioned_letters, correct_positioned_letters)
        numGuess = checkWin(round, numGuess)
    if numGuess == 6:
        print(f"The correct answer is: {answer}")

startGame()