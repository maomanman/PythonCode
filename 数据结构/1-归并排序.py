
def merge_sort( data, l,  r):
    """
    递归归并
    :param data:
    :param l:
    :param r:
    :return:
    """
    if l >= r:
        return 0
    mid =l+(r-l)//2
    count1= merge_sort(data, l, mid)
    count2=merge_sort(data, mid+1, r)
    count3 = merge(data, l, mid, r)
    return count1+count2+count3

def merge( data, l, mid, r):
    """
    归并排序
    :param data:
    :param l:
    :param mid:
    :param r:
    :return:
    """
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
count = merge_sort(data,0,len(data)-1)
print(data)
