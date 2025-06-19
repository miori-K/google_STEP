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

      
    def find_title(self,id):
        for key, value in self.titles.items():
            if key == id:
                return value
        return None
    
    def find_id(self,title):
        for key, value in self.titles.items():
            if value == title:
                return key
        return None
    
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
        start_key = self.find_id(start)  #startのidを探す
        goal_key = self.find_id(goal) #goalのidを探す
        queue = deque()
        visited = {}
        visited[start_key] = None
        queue.append(start_key)
        while queue: #キューがなくなるまでノードの子を検索していき、ゴールに辿り着いたら終わり
            node = queue.popleft()
            for child in self.links[node]:
                if child == goal_key:#goalが見つかった時
                    visited[child] = node
                    print("Found")
                    path = [] 
                    node = goal_key
                    while node is not None: #goalから辿った道を遡って記録
                        path.append(self.titles[node])
                        node = visited[node]
                    path.reverse()
                    print(path)
                    print(len(path)) 
                    return
                if not child in visited: #goalが見つからなかったらさらに子をキューに入れる
                    visited[child] = node
                    queue.append(child)
        print("Not Found")

    # Homework #2: Calculate the page ranks and print the most popular pages.
    #辞書を2つ用意して1つに古い値を記録して更新していく方法
    def find_most_popular_pages(self):
        point_count = {}
        prev_count = {}
        diff = 1
        for id in self.titles.keys(): #初期値を設定
            point_count[id] = 1
            prev_count[id] = 1
        
        while diff > 0.01:
            all_point = 0
            prev_all_point = len(point_count)*0.15
            for id in self.titles.keys():
                point_count[id] = prev_all_point/len(point_count) #全体を初期化

            for id in self.titles.keys():
                if self.links[id] != []: #繋がってる場合
                    for j in self.links[id]: 
                        point_count[j] += prev_count[id]*0.85/len(self.links[id])
                        all_point += prev_count[id]*0.15
                else: #繋がっていない場合
                    all_point += prev_count[id]

            prev_all_point = all_point    
            diff = 0
            for id in self.titles.keys(): #更新と差の計算
                diff += abs(point_count[id] - prev_count[id])
                prev_count[id] = point_count[id]
            #print(prev_count)
            #print(point_count)

        sorted_point = sorted(point_count.items(),key=lambda x:x[1], reverse = True)#pointでソートする
        print("find_most_popular_pages:")
        #print(sorted_point)
        print(sorted_point[:6])
        for id in range(6):
            print(self.find_title(sorted_point[id][0]))

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
    #wikipedia.find_shortest_path("A", "F")
    #wikipedia.find_shortest_path("C", "B")
    #wikipedia.find_shortest_path("渋谷", "パレートの法則")
    #wikipedia.find_shortest_path("渋谷", "9月22日")
    #wikipedia.find_shortest_path("渋谷", "小野妹子")
    # Homework #2
    wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    #wikipedia.find_longest_path("渋谷", "池袋")