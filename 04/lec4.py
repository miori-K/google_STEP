#python lec4.py pages_small.txt links_small.txt
#python lec4.py pages_small2.txt links_small2.txt
#python lec4.py pages_medium.txt links_medium.txt
#python lec4.py pages_large.txt links_large.txt

from os import link
import sys
import collections
from collections import deque

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}
        self.pages = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title #titlesのidのところにtitleを収納
                self.links[id] = []
        print("Finished reading %s" % pages_file)
        #print(self.titles)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        #print(self.links)
        print()


    # Example: Find the longest titles.
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()

    # Example: Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_shortest_path(self, start, goal):
        start_key = next(k for k, v in self.titles.items() if v == start) #startのidを探す
        goal_key = next(k for k, v in self.titles.items() if v == goal) #goalのidを探す
        queue = deque()
        visited = {}
        visited[start_key] = None
        queue.append(start_key)
        while queue: #キューがなくなるまでノードの子を検索していき、ゴールに辿り着いたら終わり
            node = queue.popleft()
            for child in self.links[node]:
                if child == goal_key:
                    visited[child] = node
                    print("Found")
                    path = [] #道順を記録する用
                    node = goal_key
                    while node is not None: #goalから辿った道を遡る
                        path.append(self.titles[node])
                        node = visited[node]
                    path.reverse()
                    print(path)
                    print(len(path))
                    return
                if not child in visited:
                    visited[child] = node
                    queue.append(child)
        print("Not Found")

    # Homework #2: Calculate the page ranks and print the most popular pages.
    #辞書を二つ用意して一つに古い値を記録して更新していく方法
    def find_most_popular_pages(self):
        point_count = {}
        prev_count = {}
        for id in self.titles.keys():
            point_count[id] = 1
            prev_count[id] = 1
        
        for i in range(10):
            for id in self.titles.keys():
                point_count[id] -=prev_count[id]
                if self.links[id] == []:
                    for j in point_count.keys():
                        point_count[j] += prev_count[id]/len(point_count)
                for j in point_count.keys(): #ここが重い？
                    point_count[j] += prev_count[id]*0.15/len(point_count)
                    if j in self.links[id]:
                        point_count[j] += prev_count[id]*0.85/len(self.links[id])

            for id in self.titles.keys(): #ここが重い？
                prev_count[id] = point_count[id]
            #print(prev_count)
            #print(point_count)

        sorted_point = sorted(point_count.items(), key=lambda x:x[1])#pointでソートする
        print("find_most_popular_pages:")
        #print(sorted_point)
        print(sorted_point[len(self.titles)-1])#ソートした最後の一番大きものを取り出す
        print(next(v for k, v in self.titles.items() if k == sorted_point[len(self.titles)-1][0]))

    #軽くしてみる
    def find_most_popular_pages2(self):
        point_count = {}
        prev_count = {}
        for id in self.titles.keys():
            point_count[id] = 1
            prev_count[id] = 1
        
        for i in range(5):
            for id in self.titles.keys():
                point_count[id] -=prev_count[id]
                if self.links[id] == []:
                    for j in point_count.keys():
                        point_count[j] += prev_count[id]/len(point_count)
                for j in point_count.keys(): #ここが重い？
                    point_count[j] += prev_count[id]*0.15/len(point_count)
                    if j in self.links[id]:
                        point_count[j] += prev_count[id]*0.85/len(self.links[id])
            
            for id in self.titles.keys():
                prev_count[id] -=point_count[id]
                if self.links[id] == []:
                    for j in prev_count.keys():
                        prev_count[j] += point_count[id]/len(prev_count)
                for j in prev_count.keys(): #ここが重い？
                    prev_count[j] += point_count[id]*0.15/len(prev_count)
                    if j in self.links[id]:
                        prev_count[j] += point_count[id]*0.85/len(self.links[id])
            #print(prev_count)
            #print(point_count)

        sorted_point = sorted(point_count.items(), key=lambda x:x[1])#pointでソートする
        print("find_most_popular_pages:")
        #print(sorted_point)
        print(sorted_point[len(self.titles)-1])#ソートした最後の一番大きものを取り出す
        print(next(v for k, v in self.titles.items() if k == sorted_point[len(self.titles)-1][0]))

    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_longest_path(self, start, goal):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


    # Helper function for Homework #3:
    # Please use this function to check if the found path is well formed.
    # 'path': An array of page IDs that stores the found path.
    #     path[0] is the start page. path[-1] is the goal page.
    #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
    #     page to the goal page.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def assert_path(self, path, start, goal):
        assert(start != goal)
        assert(len(path) >= 2)
        assert(self.titles[path[0]] == start)
        assert(self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert(path[i + 1] in self.links[path[i]])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # Example
    #wikipedia.find_longest_titles()
    # Example
    #wikipedia.find_most_linked_pages()
    # Homework #1
    wikipedia.find_shortest_path("A", "F")
    #wikipedia.find_shortest_path("C", "M")
    #wikipedia.find_shortest_path("渋谷", "パレートの法則")
    #wikipedia.find_shortest_path("渋谷", "9月22日")
    #wikipedia.find_shortest_path("渋谷", "小野妹子")
    # Homework #2
    wikipedia.find_most_popular_pages()
    wikipedia.find_most_popular_pages2()
    # Homework #3 (optional)
    #wikipedia.find_longest_path("渋谷", "池袋")