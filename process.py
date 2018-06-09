# -*- coding: utf-8 -*-
"""
Created on Mon May 28 22:21:18 2018

@author: 帅老板
"""

import node
import os
import itertools

"系统目录，sys.dat存储所有创建的数据库的名称 所有数据库以文件夹分开方式存储"
sys_path = "F:\\bianyi\\src\\"
"工作目录 当前数据库所处目录 db.dat存放当前数据库的表格信息 各个表格以.txt的形式存储"
work_path = ""

def start(Node):
  if Node.command_node == None:
    pass
  elif Node.command_node.type != node.NodeType.start_type:
    process(Node.command_node)
  else:
    start(Node.command_node)
  if Node.start_node == None:
    pass
  elif Node.start_node.type != node.NodeType.start_type:
    process(Node.start_node)
  else:
    start(Node.start_node)
    
def create_database(Node):
  "Node class - CreateDatabaseNode"
  try:
    os.mkdir(sys_path+Node.database_name)
  except FileExistsError:
    print("Error:Database "+Node.database_name+" has existed")
  else:
    f = open(sys_path+"sys.dat",mode="a+")
    f_ = open(sys_path+Node.database_name+"\\db.dat",mode="w")
    f_.close()
    f.write(Node.database_name+"\n")
    f.close()
    print("\nOp Result : create database successfully")
    
def create_table(Node):
  "Node class - CreateTableNode"
  tb_name = Node.table_name
  tb_attr_list = Node.attr_list
  if os.path.exists(work_path+tb_name+".txt"):
    raise RuntimeError("Error: Table "+tb_name+" exists!")
  f = open(work_path+"db.dat",mode='a+')
  i = 1
  for attr in tb_attr_list:
    f.write(tb_name + " " +str(i)+" "+attr.__str__()+"\n")
    i += 1
  f.close()
  f = open(work_path+tb_name+".txt",mode='w')
  f.close()
  print("\nOp Result : create table successfully")
  
def show_databases():
  database_name = os.listdir(sys_path)
  if len(database_name) == 1:
    print("\nThere are no databases now!")
  else:
    database_name.remove("sys.dat")
    count = 1
    print("\nDatabase Name:\n------------------------------------------------------------------")
    for i in database_name:
      print(str(count)+"th\t|\t"+i)
      count += 1
    print("------------------------------------------------------------------")
    
def show_tables():
    f = open(work_path + "db.dat",'r')
    table_name = []
    for line in f:
      if line.split()[0] not in table_name:
        table_name += [line.split()[0]]
    if len(table_name) == 0:
      print("\nThere are no tables now!")
    else:
      count = 1
      print("\nTable Name:\n------------------------------------------------------------------")
      for i in table_name:
        print(str(count)+"th\t|\t"+i)
        count += 1
      print("------------------------------------------------------------------")

def use_database(Node):
  "Node class - UseDatabaseNode"
  if Node.database_name in os.listdir(sys_path):
    global work_path
    work_path = sys_path + Node.database_name +"\\"#改变工作路径
    print("\nNow using database : "+Node.database_name)
  else:
    print("\nError: Database "+Node.database_name+" not exists")
  
def drop_database(Node):
  "Node class - DropDatabaseNode"
  try:
    flag = False
    with open(sys_path+"sys.dat",mode='r') as f:
      with open(sys_path+"sys_copy.dat",mode='w') as f_:
        for line in f:
          if Node.database_name in line:
            flag = True
            os.remove(sys_path+Node.database_name+"\\sys.dat")
            os.rmdir(sys_path+Node.database_name)
          else:
            f_.write(line)
    os.remove(sys_path+"sys.dat")
    os.rename(sys_path+"sys_copy.dat",sys_path+"sys.dat")
    if not flag:
      print("\nError:Database "+Node.database_name+" doesn't exist")
    else:
      print("\nOp Result : drop database successfully")
  except OSError:
    print("\nError: Cannot drop the database:"+Node.database_name+"\n")
    
def drop_table(Node):
  "Node class - DropTableNode"
  if Node.table_name+".txt" in os.listdir(work_path):
    os.remove(work_path + Node.table_name+".txt")
    with open(work_path+"db.dat",'r') as f:# f - 当前数据库表格文件
      with open(work_path+"db_copy.dat",'w') as f_:
        for line in f:
          if line.split()[0] != Node.table_name:
            f_.write(line)
          else:
            continue
    os.remove(work_path+"db.dat")
    os.rename(work_path+"db_copy.dat",work_path+"db.dat")
    print("\nOp Result : drop table successfully")
  else:
    print("\nError: "+Node.table_name+" doesn't exist!")
    
def insert(Node):
  "Node class - 1.InsertNode 2.IntoNode 3.Value"
  table_name = Node.into_lists.table_name
  colum_lists = Node.into_lists.colum_lists
  value_lists = Node.value_lists
  col_num = -1
  f1 = open(work_path+"db.dat",'r')
  for line in f1:
    if table_name == line.split()[0]:
      col_num = int(line.split()[1])#表的列数
  if col_num == -1:
    raise RuntimeError("Table "+table_name+" doesn't exist")
  f2 = open(work_path+table_name+".txt",'a')
  if colum_lists == 'all':
    for line in value_lists:
      f2.write(line.__str__()+" ")
    f2.write("\n")
  else:
    for line in value_lists:
      f2.write(line.__str__()+" ")
      col_num -= len(value_lists)
      for i in range(col_num):
        f2.write("NULL ")
    f2.write("\n")
  print("\nOp Result : Insert successfully")

def delete(Node):
  
  "Node class - DeleteNode"
  table_name = Node.table_name
  where_lists = Node.where_lists
  col_list = []
  with open(work_path+"db.dat",'r') as f:
    for line in f:
      if table_name == line.split()[0]:
        col_list =col_list + [[line.split()[2]]+[line.split()[3]]]
    #print(colum_lists)
  with open(work_path+table_name+".txt",'r') as f:
    with open(work_path+table_name+"_copy.txt",'w') as f_new:
      for line in f:
        line_dic = create_dict(col_list,line)
        #print(line_dic)
        if not find_where(line_dic,where_lists):
          f_new.write(line)
        else:  continue
  os.remove(work_path+table_name+".txt")
  os.rename(work_path+table_name+"_copy.txt",work_path+table_name+".txt")
  print("\nOp Result : delete successfully")
  
def update(Node):
  "Node class - UpdateNode"
  table_name = Node.table_name
  set_list = Node.set_lists#[(列名，值)，(列名，值)]
  where_list = Node.where_lists
  col_list = []
  with open(work_path+"db.dat",'r') as f:
    for line in f:
      if table_name == line.split()[0]:
        col_list += [[line.split()[2]] + [line.split()[3]]]  ##[[sname char][sage int]] 的形式
  with open(work_path+table_name+".txt",'r') as f:
    with open(work_path+table_name+"_copy.txt",'w') as f_:
      for line in f:
        line_dict = create_dict(col_list,line)
        if find_where(line_dict,where_list):
          new_line = line.split()
          for st in set_list:
            for c in col_list:
              #print(st[0].attr_name)
              if st[0].attr_name == c[0]:
                num = col_list.index(c)#找到要更新的值在第几列
                #print(num)
                new_line[num] = str(st[1].value)#更新
                break
          for s in new_line:
            f_.write(s+" ")
          f_.write("\n")
        else:
          f_.write(line)
  os.remove(work_path+table_name+".txt")
  os.rename(work_path+table_name+"_copy.txt",work_path+table_name+".txt")
  print("\nOp Result : update successfully")

def select(Node):
  select_lists = Node.select_lists
  from_lists = Node.from_lists
  where_lists = Node.where_lists
  col_list = []
  #单表
  if len(from_lists) == 1:
    table_name = from_lists[0]
    with open(work_path+"db.dat",'r') as f:
      for line in f:
        if table_name == line.split()[0]:
          col_list += [[line.split()[2]]+[line.split()[3]]]
    print("\nQuery Result:\n------------------------------------------------------------------")
    if isinstance(select_lists[0],str): #Condition * （select all lines）
      assert (select_lists[0] == "*")
      for cc in col_list:
        print(cc[0] + "\t|\t", end='')
      print("------------------------------------------------------------------")
      print('')
      if not where_lists == None: # where_lists exist:
        with open(work_path + table_name + ".txt", 'r') as f:
          for line in f:
            line_dict = create_dict(col_list, line)
            if find_where(line_dict, where_lists):
              for i in line.split():
                print(i + "\t|\t", end='')
              print('')
      else:
        with open(work_path+table_name+".txt",'r') as f:
          for line in f:
            line_split = line.split()
            for s in line_split:
              print(s + "\t|\t",end='')
            print('')
      print("------------------------------------------------------------------")
    else:
      assert (select_lists[i].type == node.NodeType.relation_attr for i in select_lists)
      show_colum_num = []
      for rr in select_lists:
        print(rr.attr_name+"\t|\t",end='')
        for c in col_list:
          if rr.attr_name == c[0]:
            show_colum_num = show_colum_num + [col_list.index(c)]
            break
      print("------------------------------------------------------------------")
      print('')
      if not where_lists == None:
        with open(work_path + table_name + ".txt",'r') as f:
          for line in f:
            line_dict = create_dict(col_list,line)
            if find_where(line_dict,where_lists):
              for num in show_colum_num:
                print(line.split()[num]+"\t|\t",end='')
              print('')
      else:
        with open(work_path + table_name + ".txt",'r') as f:
          for line in f:
            line_dict = create_dict(col_list,line)
            for num in show_colum_num:
              print(line.split()[num]+"\t|\t",end='')
            print('')
      print("------------------------------------------------------------------")
  #多表
  else:
    table_name = from_lists
    with open(work_path+"db.dat",'r') as f:
      for tb in table_name:
        tb = tb.upper()
        f.seek(0)
        for line in f:
          if tb == line.split()[0]:#表名
            temp_str = line.split()[2]#列名
            col_list += [[temp_str] + [line.split()[3]] + [tb]]  ##[[sname char tb][tb.sage int tb]]
          else:
            continue
    for it in col_list:
      for it_t in col_list:
        if (it[0] == it_t[0] or (len(it_t[0].split(".")) == 2 and it[0] == it_t[0].split(".")[1])) and it[2] != it_t[2]:
          it[0] = it[2]+"."+it[0]
          it_t[0] = it_t[2]+"."+it_t[0]
    dikaer(table_name)
    print("\nQuery Result:\n------------------------------------------------------------------")
    if isinstance(select_lists[0],str): # select * 
      assert (select_lists[0] == "*")
      for cc in col_list:
        print(cc[0] + "\t|\t", end='')
      print("------------------------------------------------------------------")
      print('')
      if not where_lists == None:
        with open(work_path +"dikaer.txt",'r') as f:
          for line in f:
            line_dict = create_dict(col_list,line)
            if find_where(line_dict,where_lists):
              for s in line.split():
                print(s + "\t|\t", end='')
              print('')
      else:
        with open(work_path +"dikaer.txt",'r') as f:
          for line in f:
            for s in line.split():
              print(s + "\t|\t", end='')
            print('')
      os.remove(work_path +"dikaer.txt")
      print("------------------------------------------------------------------")
    else:# select col
      assert (select_lists[i].type == node.NodeType.relation_attr for i in select_lists)
      show_colum_num = []
      for rr in select_lists:
        if rr.table_name == None:
          print(rr.attr_name + "\t\t|\t", end='')
          for c in col_list:
            if rr.attr_name == c[0]:
              show_colum_num = show_colum_num + [col_list.index(c)]
              break
        else:
          print(rr.table_name+"."+rr.attr_name + "\t|\t", end='')
          for c in col_list:
            if rr.table_name == c[2] and rr.attr_name == c[0]:
              show_colum_num = show_colum_num + [col_list.index(c)]
              break
      print("------------------------------------------------------------------")
      print('')
      if not where_lists == None:
        with open(work_path+"dikaer.txt",'r') as f:
          for line in f:
            line_dict = create_dict(col_list,line)
            if find_where(line_dict,where_lists):
              for num in show_colum_num:
                print(line.split()[num]+"\t\t|\t",end='')
              print('')
      else:
        with open(work_path+"dikaer.txt",'r') as f:
          for line in f:
            for num in show_colum_num:
              print(line.split()[num]+"\t\t|\t",end='')
            print('')
      os.remove(work_path +"dikaer.txt")
      print("------------------------------------------------------------------")
      
def _exit():
  os._exit(0)
  
def process(res):
  if res.type == node.NodeType.start_type:
    start(res)
  elif res.type == node.NodeType.create_database:
    create_database(res)
  elif res.type == node.NodeType.show_databases:
    show_databases()
  elif res.type == node.NodeType.drop_database:
    drop_database(res)
  elif res.type == node.NodeType.use_database:
    use_database(res)
  elif res.type == node.NodeType.create_table:
    create_table(res)
  elif res.type == node.NodeType.show_tables:
    show_tables()
  elif res.type == node.NodeType.drop_table:
    drop_table(res)
  elif res.type == node.NodeType.insert:
    insert(res)
  elif res.type == node.NodeType.delete:
    delete(res)
  elif res.type == node.NodeType.exit:
    _exit()
  elif res.type == node.NodeType.update:
    update(res)
  elif res.type == node.NodeType.select:
    select(res)
  else: raise RuntimeError('Res Node Type Error')
    
def get_value(line_dict,Node):
  #print(Node)
  if Node.type == node.NodeType.relation_attr:
    if Node.table_name == None:
      return line_dict[Node.attr_name]
    else:
      return line_dict[Node.table_name+"."+Node.attr_name]
  else:
    #print(Node.value_type)
    if Node.value_type == "NUMBER":
      return int(Node.value)
    elif Node.value_type == "STRING":
      return str(Node.value)
    elif Node.value_type == "NULL":
      return None
    else:
      raise RuntimeError("Error!! Value type error!")

def create_dict(col_list,line):# col_list[[列1名,列1type],[列2名,列2type]...] line_list[列1值,列2值....]
  "构造当前表的每一行的字典{'列1':值1,'列2':值2}"
  line_list = line.split()
  #print(line_list)
  dict = {}#dict {'列1':值1,'列2':值2}
  i = 0
  if len(col_list[0]) == 2:
      for c in col_list:
        if line_list[i] == "NULL":
            dict[c[0]] = None
            i = i+1
            continue
        if c[1] == "INT":
            dict[c[0]] = int(line_list[i])
            i = i+1
        elif c[1] == "CHAR":
            dict[c[0]] = str(line_list[i])
            i = i+1
        else:
            raise RuntimeError("Error!! line_list type error!")
  else:
    for c in col_list:
      if line_list[i] == "NULL":
        dict[c[2]+'.'+c[0]] = None
        i = i+1
        continue
      if c[1] == "INT":
        dict[c[2]+'.'+c[0]] = int(line_list[i])
        i = i+1
      elif c[1] == "CHAR":
        dict[c[2]+'.'+c[0]] = str(line_list[i])
        i = i+1
      else:
        raise RuntimeError("Error!! line_list type error!")
  return dict
  
def find_where(line_dict,Node):
  assert(Node.type == node.NodeType.condition)
  where_list = Node
  L_cond = where_list.L_cond
  R_cond = where_list.R_cond
  op = where_list.op
  if op == "AND":
    return find_where(line_dict,L_cond) and find_where(line_dict,R_cond)
  elif op == "OR":
    return  find_where(line_dict,L_cond) or find_where(line_dict,R_cond)
  elif op == "=":
    return get_value(line_dict, L_cond) == get_value(line_dict, R_cond)
  elif op == "!=":
    return get_value(line_dict, L_cond) != get_value(line_dict, R_cond)
  elif op == ">":
    return get_value(line_dict, L_cond) > get_value(line_dict, R_cond)
  elif op == "<":
    return get_value(line_dict, L_cond) < get_value(line_dict, R_cond)
  elif op == ">=":
    return  get_value(line_dict,L_cond) >= get_value(line_dict,R_cond)
  elif op == "<=":
    return get_value(line_dict, L_cond) <= get_value(line_dict, R_cond)
  else:
    raise RuntimeError("Error!! op type error!!")
  
def dikaer(tables):
  all_tb_list = []
  for tb in tables:
    with open(work_path+tb.upper()+".txt","r") as f:
      tb_list = []
      for line in f:
        tb_list = tb_list + [line.split()]
      all_tb_list = all_tb_list + [tb_list] #[ [ [t1.r1] [t1.r2] ]  [  []  [] ]  [  []  [] ] ]
  p = all_tb_list[0]
  all_tb_list = all_tb_list[1:]
  for abl in all_tb_list:
    p = list(itertools.product(p,abl))
    if isinstance(p[0][0],tuple):
      for i in range(len(p)):
        p[i] = tuple(list(p[i][0]) + p[i][1])
  with open(work_path+"dikaer.txt",'w') as f:
        #[  ([]  []  [])   ()   ()  ]
    for p_item in p:
      for t_item in p_item:
        for li in t_item:
          f.write(li+" ")
      f.write("\n")