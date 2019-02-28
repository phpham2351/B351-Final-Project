# training_data = [
#     ['Green', 3, 'Apple'],
#     ['Yellow', 3, 'Apple'],
#     ['Red', 1, 'Grape'],
#     ['Red', 1, 'Grape'],
#     ['Yellow', 3, 'Lemon']]

training_data = [['true', 204194, 58, 'True Disaster'],
                 ['false', 252534, 67, 'Love Me Like You Do'],
                 ['false', 176346, 52, 'Tripping Off'],
                 ['true', 178107, 50, 'Beg For It'],
                 ['false', 242021, 51, 'Chasing Marrakech']]

header = ["explicit", "duration", "popularity", "name"]


def uniqueVals(rows, col):
    return set([row[col] for row in rows])


def classArtists(rows):
    for row in rows:
        artist = row[3]
        song = row[4]
    return song, artist


def classCounts(rows):
    counts = {}
    for row in rows:
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts


def isNumeric(value):
    return isinstance(value, int) or isinstance(value, float)


class Question:
    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, example):
        val = example[self.column]
        if isNumeric(val):
            return val >= self.value
        else:
            return val == self.value

    def __repr__(self):
        condition = "=="
        if isNumeric(self.value):
            condition = ">="
        return "Is %s %s %s?" % (
            header[self.column], condition, str(self.value))


def partition(rows, question):
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows


def gini(rows):
    counts = classCounts(rows)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl**2
    return impurity


def info_gain(left, right, current_uncertainty):
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)


def find_best_split(rows):
    best_gain = 0
    best_question = None
    current_uncertainty = gini(rows)
    n_features = len(rows[0]) - 1

    for col in range(n_features):

        values = set([row[col] for row in rows])

        for val in values:  # for each value

            question = Question(col, val)
            true_rows, false_rows = partition(rows, question)

            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            gain = info_gain(true_rows, false_rows, current_uncertainty)

            if gain >= best_gain:
                best_gain, best_question = gain, question

    return best_gain, best_question


class Node:
    def __init__(self, rows):
        self.predictions = classCounts(rows)


class DTreeNode:

    def __init__(self,
                 question,
                 true_branch,
                 false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch


def build_tree(rows):
    gain, question = find_best_split(rows)

    if gain == 0:
        return Node(rows)

    true_rows, false_rows = partition(rows, question)

    true_branch = build_tree(true_rows)

    false_branch = build_tree(false_rows)
    return DTreeNode(question, true_branch, false_branch)


def print_tree(node, spacing=""):
    if isinstance(node, Node):
        print("Predict", node.predictions)
        return
    #print_tree(node.true_branch, spacing + "")

    print(spacing + str(node.question))

    print(spacing + '--> True:')
    print_tree(node.true_branch, spacing + "  ")

    print(spacing + '--> False:')
    print_tree(node.false_branch, spacing + "  ")


def print_tree2(node, spacing=""):
    if isinstance(node, Node):
        print("Recommend", node.predictions)
        return
    print_tree2(node.true_branch, spacing + "")


if __name__ == '__main__':

    my_tree = build_tree(training_data)
    print_tree(my_tree)

    my_tree = build_tree(training_data)
    print_tree2(my_tree)

    # Evaluate
    testing_data = [
        ['Green', 3, 'Apple'],
        ['Yellow', 4, 'Apple'],
        ['Red', 2, 'Grape'],
        ['Red', 1, 'Grape'],
        ['Yellow', 3, 'Lemon'],
    ]


