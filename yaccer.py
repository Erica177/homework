# -*- coding: utf-8 -*-
"""
Created on Sun May 27 11:48:06 2018

@author: 帅老板
"""

"""
每个文法规则被描述为一个函数，这个函数的文档字符串描述了对应的上下文无关文法的规则。函数体用来实现规则的语义动作。
每个函数都会接受一个参数p，这个参数是一个序列，包含了组成这个规则的所有的语法符号,p[i]是规则中的第i个语法符号
'expression : expression PLUS expression'  
#    |             |      |        |  
#  p[0]          p[1]   p[2]     p[3]  
对于序列中的词法单元，p[i]的值就是该词法单元的值，也就是在词法分析器中赋值的p.value。
而对于非终结符的值则取决于该规则解析时p[0]中存放的值，这个值可以使任意类型，比如tuple、dict、类实例等
"""
import ply.yacc as yacc
import node
import lexer

tokens = lexer.tokens

#定义优先级和结合性
precedence = (
    ('left','OR'),
    ('left','AND'),
    ('nonassoc','LT','LE','GT','GE','EQ','NE')
)

def p_start(p):
  """
  start : command ';' start
        | epsilon
  """
  p[0] = p[1]
  
def p_command(p):
  """
  command : ddl
          | dml
          | exit
          | epsilon
  """
  p[0] = p[1]
  
#数据定义语言
def p_ddl(p):
  """
  ddl : createdatabase
      | createtable
      | usedatabase
      | droptable
      | dropdatabase
      | showtables
      | showdatabases
  """
  p[0] = p[1]

#数据操纵语言
def p_dml(p):
  """
  dml : query
      | insert
      | update
      | delete
  """
  p[0] = p[1]

def p_exit(p):
  " exit : EXIT "
  p[0] = node.ExitNode()
  
def p_epsilon(p):
  " epsilon : "
  p[0] = None

def p_createdatabase(p):
  " createdatabase : CREATE DATABASE ID "
  p[0] = node.CreateDatabaseNode(p[3])

def p_createtable(p):
  " createtable : CREATE TABLE ID '(' table_list ')' "
  p[0] = node.CreateTableNode(p[3],p[5])

def p_usedatabase(p):
  " usedatabase : USE ID "
  p[0] = node.UseDatabaseNode(p[2])

def p_droptable(p):
  "droptable : DROP TABLE ID "
  p[0] = node.DropTableNode(p[3])
  
def p_dropdatabase(p):
  " dropdatabase : DROP DATABASE ID "
  p[0] = node.DropDatabaseNode(p[3])

def p_showtables(p):
  " showtables : SHOW TABLES "
  p[0] = node.ShowTablesNode()
  
def p_showdatabase(p):
  " showdatabases : SHOW DATABASES"
  p[0] = node.ShowDatabasesNode()
  
def p_query(p):
  " query : SELECT select_list FROM from_list where_list "
  p[0] = node.QueryNode(p[2],p[4],p[5])
  
def p_insert(p):
  " insert : INSERT INTO into_list VALUES values_list "
  p[0] = node.InsertNode(p[3],p[5])
  
def p_update(p):
  " update : UPDATE ID SET set_list where_list "
  p[0] = node.UpdateNode(p[2],p[4],p[5])
  
def p_delete(p):
  " delete : DELETE FROM ID where_list "
  p[0] = node.DeleteNode(p[3],p[4])

#插入操作时 value 后跟的 value列表
def p_values_list(p):
  " values_list : '(' mvalue_list ')' "
  p[0] = p[2]

#被括号括起来的value值的每一个 value列表是由多个表项组成
def p_mvalue_list(p):
  """
  mvalue_list : value ',' mvalue_list
              | value
              | null_value ',' mvalue_list
              | null_value
  """
  if len(p)==2 :
    p[0] = [p[1]]
  else:
    p[0] = [p[1]] + p[3]

#value可以是字符串或数字
def p_value_string(p):
  "value : STRING "
  p[0] = node.Value('STRING',p[1])
  
def p_value_number(p):
  "value : NUMBER "
  p[0] = node.Value('NUMBER',p[1])

def p_null_value(p):
  "null_value : NULL"
  p[0] = node.Value("NULL",None)
  
#执行创建表操作时 后面跟的列声明的列表 可以是单个列 也可以是多个列
def p_table_list(p):
  """
  table_list : attrtype ',' table_list
             | attrtype
  """
  if len(p)==2 :
    p[0] = [p[1]]
  else:
    p[0] = [p[1]] + p[3]

#每个列的声明是 ID+type 或者 ID+type+长度声明
def p_attrtype(p):
  """
  attrtype : ID type
           | ID type '(' NUMBER ')'
  """
  if len(p)==3:
    p[0] = node.AttrType(p[1],p[2])
  else:
    p[0] = node.AttrType(p[1],p[2],p[4])

#每个列名的type是INT或者CHAR类型
def p_type(p):
  """
  type : INT
       | CHAR
  """
  p[0] = p[1].upper()

#SELECT关键字后面跟的要选择的列名 可以是多个列名 也可以是 *
def p_select_list(p):
  """
  select_list : relaattr_list
              | '*'
  """
  p[0] = p[1]

#多个列名表可以是一个 也可以是多个
def p_relaattr_list(p):
  """
  relaattr_list : relaattr ',' relaattr_list
                | relaattr
  """
  if len(p)==2:
    p[0] = [p[1]]
  else:
    p[0] = [p[1]] + p[3]

#每个列名可以是单独的列名形式 也可以是 表名.列名 的形式
def p_relaattr(p):
  """
  relaattr : ID '.' ID
           | ID
  """
  if len(p)==2:
    p[0] = node.RelaAttr(p[1])
  else:
    p[0] = node.RelaAttr(p[3],p[1])

#FROM后面跟的表名 可以是单个表 也可以是多个表
def p_from_list(p):
  """
  from_list : ID ',' from_list
            | ID
  """
  if len(p)==2:
    p[0] = [p[1]]
  else:
    p[0] = [p[1]] + p[3]

#WHERE后面跟的可以是多条条件指令 也可以没有WHERE条件
def p_where_list(p):
  """
  where_list : WHERE mcond_list
             | epsilon
  """
  if len(p)==3:
    p[0] = p[2]
  else:
    p[0] = p[1]

#WHERE后的指令可以是多个条件与 或 或者单个条件
def p_mcond_list(p):
  """
  mcond_list : mcond_list AND mcond_list
             | mcond_list OR mcond_list
             | '(' mcond_list ')'
             | condition
  """
  if len(p)==2:
    p[0] = p[1]
  elif p[1] =='(':
    p[0] = p[2]
  else:
    p[0] = node.Cond(p[1],p[2],p[3])
    
#每个条件可以是 列与列的比较 也可以是 列与操作数的比较 也可以是
def p_condition(p):
  """
  condition : relaattr op relaattr_or_value
           | relaattr EQ null_value
           | relaattr NE null_value
  """
  p[0] = node.Cond(p[1],p[2],p[3])

#列值或者操作数
def p_relaattr_or_value(p):
  """
  relaattr_or_value : relaattr
                    | value
  """
  p[0] = p[1]

#操作符
def p_op(p):
  """
  op : LT
     | LE
     | GT
     | GE
     | EQ
     | NE
  """
  p[0] = p[1]

#set后面可以跟一个赋值语句 也可以跟多个赋值语句
def p_set_list(p):
  """
  set_list : relaattr EQ value ',' set_list
           | relaattr EQ value
  """
  if len(p) > 4:
    p[0] = [(p[1],p[3])] + p[5]
  else:
    p[0] = [(p[1],p[3])]

#into后面跟 表名（列名1，列名2、、、、），或省略列名只写表名
def p_into_list(p):
  """
  into_list : ID '(' colm_list ')'
            | ID
  """
  if len(p) > 2:
    p[0] = node.IntoNode(p[1],p[3])
  else:
    p[0] = node.IntoNode(p[1])

#单个列名 或多个列名
def p_colm_list(p):
  """
  colm_list : ID ',' colm_list
            | ID
  """
  if len(p) > 2:
    p[0] = [p[1]] + p[3]
  else:
    p[0] = [p[1]]

def p_error(p):
    if not p:
        print("Syntax Error! Maybe Missing ';' at the end of the command!")
    else:
        print("Syntax Error at token '%s'(%s)"%(p.value,p.type))

yaccer = yacc.yacc()