#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input


def distance(city1, city2): #　2つの都市間の距離を計算する関数
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def search_dist(city1,city2,dist):
    return dist[city1][city2]

def solve(cities): 
    N = len(cities) #　N=都市の数

    dist = [[0] * N for i in range(N)] #　全ての都市間の初期値をゼロに設定
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    # dist = [[AAの距離、ABの距離、ACの距離],[BAの距離、BBの距離、BCの距離],[CAの距離、CBの距離、CCの距離]]のようになる

    current_city = 0
    unvisited_cities = set(range(1, N)) #　すべての都市をunvisitedにする
    tour = [current_city] #　訪れた順番に記録

    while unvisited_cities: #　すべての都市に訪れるまで
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    tour.append(tour[0])

    return tour,dist

def opt_2(tour,dist):
    pair_list = [] 

    for i in range(len(tour) - 1): # 2つずつ取り出したリストを作る
        pair_list.append([tour[i], tour[i + 1]])
        
    for i in range(len(pair_list) - 2): # クロスしているところがあれば変える
        for j in range(i+2,len(pair_list)):
              if (search_dist(pair_list[i][0],pair_list[i][1],dist)+search_dist(pair_list[j][0],pair_list[j][1],dist))>(search_dist(pair_list[i][0],pair_list[j][0],dist)+search_dist(pair_list[i][1],pair_list[j][1],dist)):
                x = pair_list[i][1]
                pair_list[i][1] = pair_list[i+1][0] = pair_list[j][0]
                pair_list[i+1][1] = pair_list[j][0] = x
    
    answer = []
    for k in range(len(pair_list)):
        answer.append(pair_list[k][0])
    answer.append(0)

    return answer

if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour,dist = solve(read_input(sys.argv[1]))
    print_tour(opt_2(tour,dist))