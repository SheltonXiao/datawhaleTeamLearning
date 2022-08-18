# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 11:23:06 2021

@author: asus
"""

import numpy as np

def BFS(queue, status, i = 0):
    #print(status)
    newqueue = []
    #if i == 5:
    #    return queue[0],i
    for each in queue:
        sta = each.to_string()
        if sta in status.keys():
            continue
        #标记状态
        status[sta] = each
        each.height = i
        if each.is_target():
            return each,i
        neighbors = each.neighbors()
        newqueue.extend(neighbors)
    i += 1
    end,endi = BFS(newqueue, status, i)
    return end,endi

def Astar(queue, status, i = 0):
    #newqueue = []
    score = dict()
    for each in queue:
        each.height = i
        if each.is_target():
            return each
        score[each] = each.get_score()
        
    score = dict(sorted(score.items(), key=lambda d:d[1]))
    #print(score)
    newqueue = []
    minscore = [each for each in score.values()]
    for prior in score.keys():
        if score[prior] > minscore[0]:
            break
        sta = prior.to_string()
        if sta in status.keys():
            continue
        status[sta] = prior
        #if prior.is_target():
            #prior.height = i+1
        #    return prior
        neighbors = prior.neighbors()
        newqueue.extend(neighbors)
    
    i += 1
    end = Astar(newqueue, status, i)
    return end

class Board(object):
    """
    data: NxN的二维数组，list or narray; 例如: np.array([[0,1,3],[4,2,5],[7,8,6]])
    """
    def __init__(self, data, use_func = "hamming"):
        if type(data) == list:
            data = np.array(data)
        self.board_data = data
        self.use_func = use_func
        self.prev = None
        self.size()

    # board size n
    def size(self):
        self.n = self.board_data.shape[0]
        return self.n
    
    # 从val值，得到其在八数码中的正确的问题。
    def get_xy_from_value(self, val):
        if val == 0:
            return self.n-1,self.n-1
        idx = (val) // self.n - 1
        idy = (val) % self.n
        return idx, idy

    # 当前状态到目标状态的海明距离
    def hamming(self):
        dist = 0
        for i in range(self.n):
            for j in range(self.n):
                if i==j==self.n-1:
                    break
                if (i)*self.n+j+1 == self.board_data[i][j]:
                    pass
                else:
                    dist += 1
        return dist

    # 当前状态到目标状态的曼哈顿距离
    def manhattan(self):
        dist = 0
        for i in range(self.n):
            for j in range(self.n):
                if self.board_data[i][j] == 0:
                    continue
                idx,idy = self.get_xy_from_value(self.board_data[i][j])
                dist += abs(idx-i) + abs(idy-j)
        return dist
    
    # 启发式的得分 source 
    def get_score(self):
        if self.use_func == 'hamming':
            return self.height + self.hamming()
        return self.height + self.manhattan()

    # 是否是目标状态
    def is_target(self):
        if self.use_func == 'hamming':
            return self.hamming() == 0
        return self.manhattan() == 0
    
    # 当前状态的所有邻居节点，return list<Board>
    def neighbors(self):
        all_neighbors = []
        [zeroi,zeroj] = np.argwhere(self.board_data == 0)[0]
        if zeroi < self.n - 1:
            newdata = self.board_data.copy()
            newdata[zeroi][zeroj], newdata[zeroi+1][zeroj] = newdata[zeroi+1][zeroj], newdata[zeroi][zeroj]
            new = Board(newdata)
            new.prev = self
            all_neighbors.append(new)

        if zeroj < self.n - 1:
            newdata = self.board_data.copy()
            newdata[zeroi][zeroj], newdata[zeroi][zeroj+1] = newdata[zeroi][zeroj+1], newdata[zeroi][zeroj]
            new = Board(newdata)
            new.prev = self
            all_neighbors.append(new)

        if zeroi > 0:
            newdata = self.board_data.copy()
            newdata[zeroi][zeroj], newdata[zeroi-1][zeroj] = newdata[zeroi-1][zeroj], newdata[zeroi][zeroj]
            new = Board(newdata)
            new.prev = self
            all_neighbors.append(new)

        if zeroj > 0:
            newdata = self.board_data.copy()
            newdata[zeroi][zeroj], newdata[zeroi][zeroj-1] = newdata[zeroi][zeroj-1], newdata[zeroi][zeroj]
            new = Board(newdata)
            new.prev = self
            all_neighbors.append(new)

        self.neighbor = all_neighbors
        return all_neighbors

    # 当前状态是否是最终状态 ?这个用来干啥的
    def is_solvable(self):
        return self.is_target()
    
    # 棋牌状态的string表示，例如return "1 2 3 4 5 6 7 8 0"
    def to_string(self):
        data = self.board_data.flatten()
        data = [str(each) for each in data]
        return "_".join(data)
    
    # 使用数值表示当前状态的唯一性，用于迭代过程中的判断
    def hash_code(self):
        hash_value = 0
        for i in range(self.n):
            for j in range(self.n):
                hash_value = hash_value * 10 + self.board_data[i][j]
        return hash_value
    
# 这里是解决八数码问题的函数，本次测试都是可解初始化状态，对验证当前状态会否可解不做要求
class Solver(object):
    """
    board：初始化棋盘状态。
    use_algo: 解决八数码问题的算法，bfs和astart，当前你也可以实现dfs
    
    """
    def __init__(self, board, use_algo="astar"):
        self.board = board
        self.ans_board = None
        self.use_algo = use_algo

    # 解决八数码问题，你必须实验这个函数，用来解决八数码问题
    def solver(self):
        if self.use_algo == "astar":
            ans_board = Astar([self.board], dict(), i = 0)
        else:
            ans_board,endi = BFS([self.board], dict(), i = 0)
        self.ans_board = ans_board
        return [ans_board]

    # 返回最短的路径
    def moves(self):
        return self.ans_board.height

    # 返回最优结果的路径，你必须返回这个结果
    def solution(self):
        ans_list = []
        last = self.ans_board
        ans_list.append(last.board_data)
        for i in range(self.ans_board.height):
            last = last.prev
            ans_list.append(last.board_data)
        ans_list.reverse()
        return ans_list