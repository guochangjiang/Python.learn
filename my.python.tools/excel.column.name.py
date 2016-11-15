# 26进制转换
def Num_2_AZ(num):
    twenty_six_dic = {  1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',
                        7:'G',8:'H',9:'I',10:'J',11:'K',12:'L',
                        13:'M',14:'N',15:'O',16:'P',17:'Q',18:'R',
                        19:'S',20:'T',21:'U',22:'V',23:'W',24:'X',
                        25:'Y',26:'Z'}
    remainder_str = ''
    while num  >= 1:
        rem = num % 26
        num = int(num/26)
        if rem == 0:
            rem = 26
            num = num - 1
        remainder_str += twenty_six_dic[rem]
    return(remainder_str[::-1])

for i in range(1000):
    print(i, Num_2_AZ(i))