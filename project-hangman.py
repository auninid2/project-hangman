import ast


def create_dict(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        word_dict = {line.strip(): len(line.strip()) for line in f if line.strip()}

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(str(word_dict))


def is_dict_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
        return isinstance(ast.literal_eval(content), dict)
    except (ValueError, SyntaxError):
        return False


def filter_by_value(d, value):
    return [key for key, val in d.items() if val == value]


def create_histogram(words):
    histogram = {}
    for word in words:
        letter_counts = {}
        for c in word:
            letter_counts[c] = letter_counts.get(c, 0) + 1
        histogram[word] = letter_counts
    return histogram


def most_common_letter(histogram):
    total_counts = {}

    for word_counts in histogram.values():
        for letter, count in word_counts.items():
            total_counts[letter] = total_counts.get(letter, 0) + count

    most_common = max(total_counts, key=total_counts.get)
    return most_common, total_counts[most_common]


def dicting(filepath, chosen="animal"):
    with open(filepath, "r", encoding="utf-8") as f:
        data = ast.literal_eval(f.read())

    matches = filter_by_value(data, len(chosen))
    liste = create_histogram(matches)
    print(most_common_letter(liste))
