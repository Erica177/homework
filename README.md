# homework
<h1>编译原理大作业-python </h1></br>
lexer - 词法分析器</br>
yaccer - 语法分析器</br>
process - 语义处理</br>
node - 语义动作辅助类</br>
main - 主函数 </br>
<h1>测试用例</h1>
创建数据库：</br>
CREATE DATABASE K;</br>
删除数据库：</br>
DROP DATABASE K;</br>
查看所有数据库：</br>
SHOW DATABASES;</br>
进入当前数据库：</br>
USE K;</br>
创建表格：</br>
CREATE TABLE STUDENT(SNAME CHAR(10),SAGE INT);</br>
CREATE TABLE TEACHER(TNAME CHAR(10),TNO INT);</br>
CREATE TABLE CLASS(CNAME CHAR(10),CDATA(10));</br>
查看当前数据库所有表格：</br>
SHOW TABLES;</br>
插入</br>
INSERT INTO STUDENT VALUES('LIMING',10);</br>
INSERT INTO TEACHER(TNAME) VALUES('NAN');</br>
删除</br>
DELETE FROM STUDENT WHERE SNAME='LIMING';</br>
更新</br>
UPDATE STUDENT SET SNAME='ZHANGSAN' WHERE SAGE=20;</br>
查询</br>
SELECT * FTOM STUDENT;</br>
SELECT * FROM STUDENT,TEACHER;</br>
SELECT STUDENT.SNAME,TEACHER.TNAME FROM STUDENT,TEACHER WHERE STUDENT.SAGE=TEACHER.TNO;</br>
SELECT SNAME FROM STUDENT WHERE SAGE=20;</br>
退出</br>
EXIT;
