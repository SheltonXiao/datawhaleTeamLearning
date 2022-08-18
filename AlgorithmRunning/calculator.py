# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 17:09:33 2021

@author: asus
"""
ORDER_DICT = {
'+': {'+':-1, '-':-1, '*':-1, '/':-1, '√':-1, '(':1, ')':-1},
'-': {'+':-1, '-':-1, '*':-1, '/':-1, '√':-1, '(':1, ')':-1},
'*': {'+':1, '-':1, '*':-1, '/':-1, '√':-1, '(':1, ')':-1},
'/': {'+':1, '-':1, '*':-1, '/':-1, '√':-1, '(':1, ')':-1},
'√': {'+':1, '-':1, '*':1, '/':1, '√':-1, '(':1, ')':-1},
'(': {'+':1, '-':1, '*':1, '/':1, '√':1, '(':1, ')':0},
')': {'+':-1, '-':-1, '*':-1, '/':-1, '√':-1, '(':0, ')':-1}
    }

binary_op = {'+','-','*','/','(',')'}
unary_op = {'√'}

# file: calculator.py, 文件名必须是这个名
class Calculator(object):
    def __init__(self):
        self.stack_num = []
        self.stack_op = []
    
    # 系统会默认调用这个函数进行评测，你必须实验这个函数
    # 输入一个计算表达式，例如2+3*√4，返回的结果是8
    # 返回计算后的结构
    def solver(self, inputString):
        result = 0
        for i in range(len(inputString)):
            c = inputString[i]
            if 
        return 0
    
    def is_negative(self):
        #什么时候会是负的呢
        
    def convert(self, inputString):
        
        
