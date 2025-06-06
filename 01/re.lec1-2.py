import sys
from collections import Counter

##早くなる方法(最初にスコアも計算した辞書を作って保存する方法）で課題2をやり直そうとしています！まだ途中です。

def abc_and_score(dict):
    ABC_dict = []
    for word in dict:
        ABC_score = [1,3,2,2,1,3,3,1,1,4,4,2,2,1,1,3,4,1,1,1,2,3,3,4,3,4]
        score = 0
        count = Counter(word)
        abc = [count.get(chr(i), 0) for i in range(ord('a'), ord('z')+1)]
        #ここまででABC辞書を作成
        for i in range(26):
            score += ABC_score[i]*abc[i]
        #ここまででスコアを計算
    ABC_dict.append[[word],[abc],[score]]
    return ABC_dict

def answer(sorted_dictionary,word):
    answer_list = []
    for i in sorted_dictionay:
        for j in range(26):
            if sorted_dictionary[i][1[j]] < word[1[j]]:
                append.answer_list[sorted_dictionary[i][0]]
                count += sorted_dictionary[i][2]

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
        ABC_dictionary = abc_and_score(dictionary)

    input_output(input_file, output_file, ABC_dictionary)