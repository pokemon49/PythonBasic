import random

class randomStudy():
    def run(self):
        ra = random
        r0 = ra.random()          #随机浮点数（0.0~1.0）
        r1 = ra.randint(100, 999)  #随机区间整数
        r2 = ra.uniform(1, 100)    #随机区间浮点数
        r3 = ra.randrange(1, 100, 3) #随机区间指定间隔整数
        r4 = ra.choice('zbcdefghijk23879') #随机序列1
        r5 = ra.choice(['aa', 'bb', 'cc', 'dd', 'ee', 'ff']) #随机序列2
        p = ["Java", "C++", "Python", "C", "PHP", "Scala"]
        r6 = ra.shuffle(p)           #随机打乱序列
        r7 = ra.sample(p, k=3)        #随机选择序列中的指定数量项目
        r8 = ra.expovariate(21/7)    #随机指数分布浮点数，带入参数
        r9_1 = ra.triangular(1, 10, 9) #三角分布函数
        r9_2 = ra.triangular(1, 10)   #三角分布函数
        r10 = ra.betavariate(7,9)     #beta分布函数
        r11 = ra.gammavariate(7,9)    #伽玛分布函数
        r12 = ra.gauss()              #高斯分布函数,样式：gauss(mu, sigma)
        r13 = ra.lognormvariate()     #长正态分布函数,样式： lognormvariate(mu, sigma)
        r14 = ra.normalvariate()      #正态分布函数,样式：normalvariate(mu, sigma)
        r15 = ra.vonmisesvariate()    #冯米塞斯分布函数,样式：vonmisesvariate(mu, kappa)
        r16 = ra.paretovariate()      #帕累托分布函数,样式：paretovariate(alpha)
        r17 = ra.weibullvariate()     #布尔分布函数 ,样式：weibullvariate(alpha, beta)


        s = "随机小数:"+str(r0)+chr(10) \
           +"随机整数:"+str(r1)+chr(10) \
           +"随机浮点:" + str(r2) + chr(10) \
           +"随机间隔整数:" + str(r3) + chr(10) \
           +"随机序列1:" + str(r4) + chr(10) \
           +"随机序列2:" + str(r5) + chr(10) \
           +"随机打乱序列:" + str(r6) + chr(10) \
           +"随机指定序列数量:" + str(r7) + chr(10) \
           +"随机指数分布浮点数:" + str(r8) + chr(10)

        print(s)

rs = randomStudy()
rs.run()