#
# 
# @param s string字符串 
# @param p string字符串 
# @return bool布尔型
#
class Solution:
    def isMatch(self, s, p):
        # write code here
        # ac = len(s)
        if '*' not in p and '?' not in p:
            if p == s:
                return True
            else:
                return False
        ac = len(s)
        bc = len(p)
        if ac == 0 and p.count('*') == bc:
            return True
        elif ac == 0:
            return False

        last = []
        i = 0
        j = 0
        while i < bc:
            if last:
                if p[i] in s[j:]:
                    i = max(s.index(p[i]), i)
                    last.pop(-1)
                else:
                    return False
            else:

                if p[i] == s[j] or p[i] == '?':
                    i = i + 1
                    j = j + 1
                elif p[i] == '*':
                    last.append(p[i])
                    i = i + 1
                else:
                    return False
        if last or j == ac:
            return True
        elif j < ac:
            return False


