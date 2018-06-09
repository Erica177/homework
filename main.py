# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 22:05:54 2018

@author: 帅老板
"""
from lexer import lexer as lex
from yaccer import yaccer as yacc
from process import process

if __name__ == '__main__':
    while True:
        cmd = input("User@Cmd: ~$ ")
        res = yacc.parse(cmd,lexer=lex)
        #print(type(result))
        if not res:continue
        process(res)