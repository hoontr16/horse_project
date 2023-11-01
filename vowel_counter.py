vowels = "AaEeIiOoUu"
def vowelcheck(word, vowels):
    """ a function to check how many vowels are in a single word
    Args:
        word(str): the word which is having its vowels counted
        vowels(str): a string of characters that are considered vowels
    """
    count = [each for each in word if each in vowels]
    print(len(count))
    print(count)
while True:
    word = input()
    strings = word.split()
    if len(strings) == 1:
        break
    else:
        print('only one word')
vowelcheck(word, vowels)
