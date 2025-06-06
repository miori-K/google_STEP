import sys
from collections import Counter

def ABCcount(word):
    count = Counter(word)
    return [count.get(chr(i), 0) for i in range(ord('a'), ord('z')+1)]

def score_count(words):#words = wordにして一個一個みていく
    ABC_score = [1,3,2,2,1,3,3,1,1,4,4,2,2,1,1,3,4,1,1,1,2,3,3,4,3,4]
    score = 0
    for word in words:
        count_word = ABCcount(word)
        for i in range(26):
            score += ABC_score[i]*count_word[i]
    return score

def answer(score_words_list):
    max_list = []
    max_score = 0
    for i in range(len(score_words_list)):
        if max_score == score_words_list[i][1]:
            max_list.append(score_words_list[i][0])
        elif max_score < score_words_list[i][1]:
            max_score = score_words_list[i][1]
            max_list = []
            max_list.append(score_words_list[i][0])
    return max_list,max_score

def check(input_word,ABC_dictinoary):#
    input_word_count = ABCcount(input_word)
    count_ABC_dictionary = []
    words = []
    for word in range(len(ABC_dictionary)): #change word = i にした方がわかりやすい
        count_ABC_dictionary = ABC_dictinoary[word][1]
        for i in range(26):
            if count_ABC_dictionary[i] > input_word_count[i]:
                break
        else:
            score = score_count(ABC_dictionary[word][0])
            words.append([ABC_dictionary[word][0],score])
    return input_word,words #input_wordは入力なので返さない

def input_output(input_filename, output_filename, ABC_dictionary):
    total_score = 0
    with open(input_filename, 'r') as f:
        words = f.read().splitlines()

    with open(output_filename, 'w') as out_file:
        for word in words:
            input_word, words_list = check(word, ABC_dictionary)#input_wordはwordのままで
            max_list, max_score = answer(words_list)
            out_file.write(f"{input_word}: {max_list}\n")
            out_file.write(f"score: {max_score}\n")
            total_score += max_score
        out_file.write(f"total_score:{total_score}\n")
    print(total_score)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open('words.txt', 'r') as f:
        dictionary = f.read().splitlines()
        ABC_dictionary = []
        for word in dictionary:
            ABC_dictionary.append([word,ABCcount(word)])

    input_output(input_file, output_file, ABC_dictionary)