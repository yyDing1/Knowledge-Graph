import json


def filter1():
    concept = {}
    mp = {}
    index = {}
    entity = {}
    relation = {}
    picture_link = []
    with open("weapon_tree.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            split_space = []
            for i in range(len(line)):
                if line[i] == '｜':
                    split_space.append(i)
            item = line[split_space[0] + 1: split_space[1]]
            ty = line[0: split_space[0]]
            if line[split_space[1] + 1: -1] == "entity":
                mp[item] = ty
            else:
                concept[item] = ty
            if ty not in index:
                index[ty] = "%06d" % (len(index) + 1)
            if item not in index:
                index[item] = "%06d" % (len(index) + 1)
            if item not in entity:
                entity[item] = index[item]
    with open("record.json", "r", encoding="utf-8") as f:
        lst = json.load(f)
    concept_level = []
    new_lst = []
    for item in lst:
        name = item["名称"]
        if name not in index:
            index[name] = "%06d" % (len(index) + 1)
        if name not in entity:
            entity[name] = index[name]
        if name not in mp:
            item["分类"] = ["暂无", "-1"]
            continue
        else:
            item["分类"] = [mp[name], index[name]]

        if "图片" not in item:
            item["图片"] = []
        picture_list = item["图片"]
        new_picture_list = []
        for picture in picture_list:
            if picture[1][:7] == "uploads":
                picture_link.append([picture[0], "http://www.wuqibaike.com/" + picture[1]])
                picture[1] = "./resource/picture/%s.jpg" % picture[0]
                new_picture_list.append([picture[0], picture[1]])
        item["图片"] = new_picture_list

        for key in item:
            if key == "名称" or key == "介绍":
                continue
            now = item[key]
            if str(type(now)) == "<class 'str'>" and now in entity:
                item[key] = [now, index[now]]
                if key not in relation:
                    relation[key] = 1
                else:
                    relation[key] += 1
        ss = item["介绍"]
        ret = ""
        for ch in ss:
            if ch == ' ':
                continue
            ret += ch
        item["介绍"] = ret

        new_item = {"Lemma_ID": index[name]}
        for key in item:
            new_item[key] = item[key]
        new_lst.append(new_item)

    for key in concept:
        concept_level.append({"Concept_ID": index[key], "名称": key, "isA": [concept[key], index[concept[key]]]})
    new_lst = concept_level + new_lst

    with open("index.txt", "w", encoding="utf-8") as f:
        for key in index:
            f.write("%s: %s\n" % (key, index[key]))
    with open("res.json", "w", encoding="utf-8") as f:
        json.dump(new_lst, f, ensure_ascii=False, indent=4)
    with open("relation.txt", "w", encoding="utf-8") as f:
        for key in relation:
            f.write("%s: %d\n" % (key, relation[key]))
    with open("picture.txt", "w", encoding="utf-8") as f:
        for link in picture_link:
            f.write("%s %s\n" % (link[0], link[1]))


def main():
    filter1()


if __name__ == "__main__":
    main()
