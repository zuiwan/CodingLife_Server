## 原始需求

- (1) 用户登录
- (2) 学生注册模块
- (3) 自动组卷模块
- (4) 题目录入模块
- (5) 学生管理模块
- (6) 改卷功能模块
- (7) 考试答题模块
- (8) 查询成绩模块
- (9) 密码修改模块
- (10)权限管理模块

## 拆解
>关于模块报价，我会给出3个报价，对应的代码质量、鲁棒性、性能等会有相应的差异，请自行斟酌选择。
当然也可以先选择便宜的，写论文时需要有关该模块的帮助（或者是某些特殊情况下的bug
【我对自己写的代码负责，绝对不会在低价版本中写太差的代码】），可以升级一下^_^。
**另外，最高价的一档自带论文支持。**

1. ***登录注册模块。*** 显然在线考试系统有两类用户，老师（管理员）和学生（普通用户），(1),(2)中没有老师登录模块，
个人觉得不太合理，这两个模块实质上是一个模块。鉴于系统的用户复杂性，(1)(2)(9)合并为一个登录注册模块，
（后端的话密码修改没必要单列成模块）
    - 300元 简单的认证，较低的安全级别
    - 400元 较为简单的认证，安全性保障
    - 500 较为复杂的认证方案和较高的安全性保障
    - 600 第三方登录注册（支持一个加100）

2. ***学生管理模块。*** 这个复杂度可大可小。
    - 300 支持学生本人对自己的增删改查
    - 400 支持管理员及学生本人对学生信息的增删改查
    - 500 支持撤销更改（保留操作历史记录）

3. ***题目录入模块。*** 看题目有哪些形式吧。
    - 100 不支持图片和复杂题型；
    - 200 支持图片和复杂题型。
    - 300 支持断点录入（中途断网等，类似上传文件的断点续传）

4. ***自动组卷模块。*** 可能比较偏算法。
    - 300元 题库较大，试卷题型较为简单题量较少，试卷差异度要求较低
    - 400元 题库较大，试卷题型较为复杂题量较多，试卷差异度要求不高
    - 500元 试卷差异度要求较高（不会出雷同的试卷）

5. ***考试答题模块。*** 这个其实是一个答案存储和分数计算的模块。报价300, 400, 500。
    - 300 不持久化保存答案，只计算成绩；不支持主观题。
    - 400 持久化保存答案；支持主观题。
    - 500 支持主观题打分

6. ***查询成绩模块。***
    - 100 支持查询每次考试的成绩；
    - 200 支持查询每次考试每个部分的成绩（就像四六级一样分听力阅读等）;支持成绩对其他学生保密。
    - 300 支持打印成绩单

7. ***权限管理模块***
    - 300 支持学生和老师这两种身份的权限管理
    - 400 支持普通学生和学习委员，普通管理员和超级管理员等更为细分的权限管理

8. **服务器运维成本**
    - 20 /月

9. **HTTPS**支持
    - 100

11. **数据存储可靠性保障、备份等**
    - 100

12. **服务器一次性部署服务费**（如果不购买此项服务，则不支持9，11）
    - 100

