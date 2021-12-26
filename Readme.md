

![Github Releases](https://img.shields.io/badge/Python-3.6-green) ![Github Releases](https://img.shields.io/badge/Django-2.0.1-green)

:books:项目目录

onlineExam
├─apps
│  ├─login             登录模块
│  │  ├─migrations
│  ├─paper           试题模块
│  │  ├─migrations
│  ├─student       学生模块
│  │  ├─migrations
│  └─teacher       教师模块
│  │  ├─migrations
├─extra_apps      外部库
│  ├─xadmin        xadmin库
├─logs          		日志
├─middleware    中间件
├─onlineExam    项目主目录
├─static				静态文件目录
│  ├─css
│  ├─fonts
│  ├─images
│  └─js
├─templates        模板目录
│  ├─student       学生模板‘
│  └─teacher       教师模板

:key: 导入excel的格式（打 * 号的为必填项）

1、导入试题

| *科目                   | *题目                            | *A                 | *B                 | *C                 | *D             | *答案 | *难度                       |
| ----------------------- | -------------------------------- | ------------------ | ------------------ | ------------------ | -------------- | ----- | --------------------------- |
| 1（对应数据库中科目id） | 利用fseek函数可实现的操作是( )。 | 实现文件的顺序读写 | 改变文件的位置指针 | 实现文件的随机读写 | 以上答案均正确 | D     | 1(1:简单，2：一般，3：困难) |

2、学生导入

| *学院 | *专业 | *班级 | *姓名 | *一卡通号 | *性别 |
| ----- | ----- | ----- | ----- | --------- | ----- |
|       |       |       |       |           |       |

3、教师导入

| *工号      | *姓名 | *性别 | 手机号      |
| ---------- | ----- | ----- | ----------- |
| 2020211425 | 张三  | 男    | 17321035647 |

