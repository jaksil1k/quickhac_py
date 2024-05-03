import codecs
import json


def parse(res: str):
    j = len(res) - 1
    while res[j] != '}':
        j -= 1
    ans = ''
    i = 0
    while res[i] != '{':
        i += 1
    while i <= j:
        if res[i] == '\\':
            i += 1
            if res[i] == 'n':
                i += 1
        ans += res[i]
        i += 1
    return json.loads(ans)