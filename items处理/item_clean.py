def clean_str(x):
    ret = ""
    for ch in x:
        if u'\u4e00' <= ch <= u'\u9fff':
            ret += ch
    return ret


mp = {}
with open("items.txt", "r", encoding="utf-8") as f:
    for line in f.readlines():
        now_elem = clean_str(line)
        if now_elem not in mp:
            mp[now_elem] = 1
        else:
            mp[now_elem] += 1

with open("clean_items.txt", "w", encoding="utf-8") as f:
    for now_elem in mp:
        if mp[now_elem] <= 15:
            continue
        # f.write("%s: %d\n" % (now_elem, mp[now_elem]))
        f.write("%s = scrapy.Field()\n" % now_elem)

