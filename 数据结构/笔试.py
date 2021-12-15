import numpy as np
def test1():
    n,m = map(int,input().split())

    pw = np.array([0] * n)
    i = 1
    dic = []
    while i <= m:
        li,ri = map(int,input().split())

        dic.append([li,ri,i])
        # pw[li:(ri + 1)] = [i] * (ri - li + 1)
        i = i + 1

    print(dic)
    dic.reverse()
    print(dic)
    s =0
    print(pw)
    for ii in dic:
        count = pw[ii[0]:ii[1]+1].count(0)
        i = 0
        index = ii[0]
        while i<count:
            index = pw[index:ii[1]+1].index(0)+index
            print(index)
            pw[index]=ii[2]
            i = i + 1
            s = s+ index * ii[2]
        print(pw)

    # s = 0
    # for i, num in enumerate(pw):
    #     s = s + i * num
    password = s % 100000009
    #
    print(password)


def new_sec(a,b,j):
    m = a
    while m <= b:
        sec[m] = j
        m += 1
    return sec
def test2():
    INPUT = input().split(" ")
    N = int(INPUT[0])
    M = int(INPUT[1])
    sec = [0]*N

    i=1
    while i <= M:
        LR= input().split(" ")
        new_sec(int(LR[0]) , int(LR[1]) , i)
        # print(sec)
        # print(i)
        i += 1

    k = 0
    sum = 0
    while k<N:
          sum = sum + sec[k]*k
          k += 1
    sum = sum%100000009
    print(sum)


def test3():
    N, M = eval(input())
    code = [0] * N
    res = 0
    for i in range(M):
        L, R = eval(input())
        code[L:R + 1] = [i + 1] * (R - L + 1)

    for j in range(N):
        res += j * code[j]

    print(res)

# test3()
# test1()

def InversePairs(data):
    # write code here
    tem = data[0]
    data.sort()
    index = data.index(tem)

    return index


def inputData( allData):
    P = 0
    for i in range(len(allData) - 1):
        P = P + InversePairs(allData[i:])
    return  P


# arr = eval(input())
# arr =  [364,637,341,406,747,995,234,971,571,219,993,407,416,366,315,301,601,650,418,355,460,505,360,965,516,648,727,667,465,849,455,181,486,149,588,233,144,174,557,67,746,550,474,162,268,142,463,221,882,576,604,739,288,569,256,936,275,401,497,82,935,983,583,523,697,478,147,795,380,973,958,115,773,870,259,655,446,863,735,784,3,671,433,630,425,930,64,266,235,187,284,665,874,80,45,848,38,811,267,575]
#
# # brr =arr.copy()
#
#
# P = inputData(arr)
#
# print(P % 1000000007)

def merge_sort( data, l,  r):
    if l >= r:
        return 0
    mid =l+(r-l)//2
    count1= merge_sort(data, l, mid)
    count2=merge_sort(data, mid+1, r)
    count3 = merge(data, l, mid, r)
    return count1+count2+count3

def merge( data, l, mid, r):
    j = mid+1
    tem = []
    i=l
    count = 0
    i_flag = 1
    while i <= mid and j <= r:
        if data[i] > data[j]:
            tem.append(data[j])
            count = count + mid-i+ 1
            j = j + 1
        else:
            tem.append(data[i])
            i = i + 1


    if i <= mid:
        tem.extend(data[i:mid+1])
    elif j <= r:
        tem.extend(data[j:r + 1])
    data[l:r + 1] = tem

    return count

data = [364,637,341,406,747,995,234,971,571,219,993,407,416,366,315,301,601,650,418,355,460,505,360,965,516,648,727,667,465,849,455,181,486,149,588,233,144,174,557,67,746,550,474,162,268,142,463,221,882,576,604,739,288,569,256,936,275,401,497,82,935,983,583,523,697,478,147,795,380,973,958,115,773,870,259,655,446,863,735,784,3,671,433,630,425,930,64,266,235,187,284,665,874,80,45,848,38,811,267,575]
print(data)
# mid= (len(data)-1)//2
count = merge_sort(data,0,len(data)-1)
# merge(data,0,mid,len(data)-1)
print(data)
print(count % 1000000007)