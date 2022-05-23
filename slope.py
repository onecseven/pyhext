import sys

path = sys.argv[1]


def get_num(arr):
    result = arr[0]
    indexslash = result.__str__().rfind("-") + 1
    indexdot = result.__str__().rfind(".")
    number = result[indexslash:indexdot]
    return int(number)


def order(path):
    result = []
    current_arr = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("    page"):
                if len(current_arr) > 0:
                    result.append(current_arr)
                    current_arr = []
                current_arr.append(line)
                current_arr.append([])
            else:
                current_arr[1].append(line)
        f.close()
    result.sort(key=get_num)
    return result

def write_sorted(path):
  arr = order(path)
  with open(path, "a+", encoding="utf-8") as f:
    f.truncate(0)
    for tuple in arr:
      title = tuple[0]
      f.write(title)
      text = tuple[1]
      for line in text:
        f.write(line)
    f.close()
