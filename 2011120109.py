def main():
    i = 0
    with open("word.txt", "r", encoding="utf-8") as f:
        for line in f:
            text = line.strip()
            i = i + 1
            if (i+1) % 4 == 0:
                print(text)
