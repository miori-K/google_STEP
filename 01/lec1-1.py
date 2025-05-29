import unittest

def binary_search(word,pair_dictionary):
    answer = []
    head = 0
    last = len(pair_dictionary) - 1
    while  head <= last:
        mid = (head + last) // 2
        if word < pair_dictionary[mid][0]:
            last = mid - 1
        elif word > pair_dictionary[mid][0]:
            head = mid + 1
        else:
            i = mid 
            while pair_dictionary[i][0] == word:
                answer.append(pair_dictionary[i][1])
                i -= 1
            j = mid + 1
            while pair_dictionary[j][0] == word:
                answer.append(pair_dictionary[j][1])
                j += 1
            return answer

def solution(input_word,dictonary):
    sorted_word = sorted(input_word)
    new_dictionary = []
    for word in dictionary:
        new_dictionary.append([sorted(word),word])
    new_dictionary.sort()
    anagram = binary_search(sorted_word,new_dictionary)
    return anagram

with open('words.txt', 'r') as f:
     dictionary = f.read().splitlines() 
input_word = input()
print(solution(input_word, dictionary))

class Test(unittest.TestCase):
    def test1(self):
        with open('words.txt', 'r') as f:
            dictionary = f.read().splitlines() 
        self.assertEqual(solution("cta",dictionary), ["act","cat"])
    def test2(self):
        with open('words.txt', 'r') as f:
            dictionary = f.read().splitlines() 
        self.assertEqual(solution("ojdiafsfd",dictionary),None)
    def test3(self):
        with open('words.txt', 'r') as f:
            dictionary = f.read().splitlines() 
        self.assertEqual(solution("lemweoc",dictionary),["welcome"])
    def test4(self):
        with open('words.txt', 'r') as f:
            dictionary = f.read().splitlines() 
        self.assertEqual(solution("",dictionary),None)

if __name__ == "__main__":
    unittest.main()