# -*- coding: utf-8 -*-
"""
Created on Sun May 27 10:34:21 2018

@author: 帅老板
"""

import ply.lex as lex

#定义保留关键字
reversed = (
    'CREATE','SELECT','FROM','WHERE','DROP','INSERT',
    'SET','VALUES','DELETE','INTO','SHOW','UPDATE',
    'TABLE','USE','DATABASE','DATABASES','TABLES',
    'AND','OR','NOT','INT','CHAR','NULL','EXIT'
    )
#定义标记
tokens = reversed + (
    'ID','NUMBER','STRING',
    'EQ','NE','LT','GT','LE','GE'
    )

#定义特殊符号
literals = ['(',')',',',';','.','+','-','*','/']
#定义可忽略字符
t_ignore = r' '#忽略空格
t_ignore_note = r'\/\/.*?$'#忽略单行注释
t_ignore_notes =  r'\/\*.*?\*\/'#忽略多行注释
#定义标记对应的描述符
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'='
t_NE = r'!='
#定义模式
"""
定义正则表达式以及根据正则表达式识别出记号后的操作
正则表达式作为函数的doc，参数t是LexToken类型，表示识别出的词法单元，具有属性：
                value：默认就是识别出的字符串序列。
                type：词法单元的类型，就是在tokens元组中的定义的。
                line：词法单元在源代码中的行号。
                lexpos：词法单元在该行的列号。
"""
def t_ID(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  if t.value.upper() in reversed:
    t.type = t.value.upper()
  else:
    t.type = 'ID'
  return t

def t_STRING(t):
  r'(\'|").*?(\'|")'
  t.value = t.value[1:-1]#去除括号
  return t

def t_NUMBER(t):
  r'\d+'
  t.value = int(t.value)
  return t

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)
    
def t_error(t):
  print("Lex Error [%s,%s]:Illegal word '%s'."%(t.lexer.lineno,t.lexer.lexpos,t.value[0]))
    
lexer = lex.lex()