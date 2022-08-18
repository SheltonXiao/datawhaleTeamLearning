# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 14:19:54 2021

@author: asus
"""

#%%
import numpy as np

class Percolation(object):
    """Percolation
    Args:
        n(int): 构造矩阵的大小，构造成 (n, n)；0表示关闭，1表示打开
    """
    def __init__(self, n):
        self.n = n
        
        self.data = np.zeros((n,n))
        
        self.max_try = n*n
    
    # 判断系统中放个(row, col)是否是打开状态
    def is_open(self, row, col):
        return self.data[row,col] == 1

    # 打开(row, col)这个格子，状态从0变成1  
    def open(self, row, col):
        self.data[row,col] = 1
        self.lastpt = (row,col)
    
    # 返回打开的格子数
    def number_of_open_sites(self):
        return self.data.sum()
    
    # 返回当前系统的状态，是nxn的矩阵
    def get_current_status(self):
        return self.data

    # 可视化系统，将满足从上到下系统的格子，进行显示，
    # 你需要将满足从第一行就连通的格子的状态，从1变成2
    def show_percolates(self):
        show = np.zeros((self.n,self.n))
        
        # 第一层所有打开的格子可渗透
        show[0,:] = self.data[0,:]
        cu = np.where(show[0,:]==1)[0].tolist()
        lis = [(0,each) for each in cu]
        totlis = []
        
        totlis = self._sub_show_percolates(lis,totlis)
        
        #print(totlis)
        for (i,j) in totlis:
            show[i,j] = 1
            
        return show + self.data
            
    def _sub_show_percolates(self,lis,totlis):
        if len(lis) == 0:
            return totlis
        
        nlis = []
        for (i,j) in lis:
            newlis = [(max(i-1,0),j), (min(i+1,self.n-1), j), 
                      (i, max(j-1,0)), (i, min(j+1,self.n-1))]
            newlis = list(set(newlis))
            newlis = [each for each in newlis if self.data[each[0],each[1]]==1]
            
            nlis.extend(newlis)
        
        nlis = list(set(nlis)-set(totlis))
        totlis.extend(nlis)
        #print(nlis)
        totlis = self._sub_show_percolates(nlis,totlis)
        return totlis
    
    # 返回true or false，表示当前系统是否是渗透的
    # 以新添加点为起点进行检索
    def percolates(self):
        start = False
        end = False
        
        try:
            lis = [self.lastpt]
        except:
            return False
        
        totlis = lis.copy()
        start,end = self._sub_percolates(lis,start,end,totlis)
        return start and end
    
    def _sub_percolates(self,lis,start,end,totlis):
        if len(lis) == 0:
            return start,end
        
        nlis = []
        for (i,j) in lis:
            newlis = [(max(i-1,0),j), (min(i+1,self.n-1), j), 
                      (i, max(j-1,0)), (i, min(j+1,self.n-1))]
            newlis = list(set(newlis))
            newlis = [each for each in newlis if self.data[each[0],each[1]]==1]
            
            for each in newlis:
                if each[0] == 0:
                    start = True
                    newlis.remove(each)
                    #break
                if each[0] == self.n-1:
                    end = True
                    newlis.remove(each)
                    #break
            #newlis = [] if start or end else newlis
            nlis.extend(newlis)
            
        if start and end:
            return start,end
        
        nlis = list(set(nlis)-set(totlis))
        totlis.extend(nlis)
        #print(nlis)
        start,end = self._sub_percolates(nlis,start,end,totlis)
        return start,end
        
    
    # 运行模拟实验，每次打开一个格子，直到系统联通; 返回打开的格子个数
    def run(self):
        i = 0
        while i < self.max_try:
            [row,col] = np.random.randint(self.n,size = 2)
            if not self.is_open(row,col):
                self.open(row,col)
                i += 1
                if self.percolates():
                    break
        return i/self.max_try

#%%
class PercolationStats(object):
    def __init__(self, n, t):
        self.n = n 
        self.t = t
        self.record = np.zeros(t)

    # sample mean of percolation threshold
    # 渗透系统的阈值
    def mean(self):
        self.meanV = self.record.mean()
        return self.meanV

    # sample standard deviation of percolation threshold
    # T次实验渗透系统阈值对应的标准差
    def stddev(self):
        self.std = self.record.std()
        return self.std

    # low endpoint of 95% confidence interval
    # 95置信区间的下届
    def confidenceLow(self):
        self.lowcon = self.meanV - 1.96*self.std/(self.t**0.5)
        return self.lowcon

    # high endpoint of 95% confidence interval
    # 95置信区间的上届
    def confidenceHigh(self):
        self.highcon = self.meanV + 1.96*self.std/(self.t**0.5)
        return self.highcon
    
    # 系统会默认调用这个函数进行评测，这个函数必须实现
    # 进行t次模拟实验，需要返回5元组
    # <mean(渗透阈值), std(方差), low_conf(置信区间下界), high_conf(置信区间上界), precolation_status(T次实验中随机一个可视化的状态，需要将能够从上到下渗透的格子从1标记成2)>
    def run(self):
        for i in range(self.t):
            rand = Percolation(self.n)
            self.record[i] = rand.run()
        return (self.mean(), self.stddev(), 
                self.confidenceLow(), self.confidenceHigh(), 
                rand)

if __name__ == "__main__":
    n = 15
    t = 20
    #if len(sys.argv) == 3:
    #    n = int(sys.argv[1])
    #    t = int(sys.argv[2])
    percolation_stats = PercolationStats(n, t)
    percolation_stats.run()