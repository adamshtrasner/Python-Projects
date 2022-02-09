# FILE : decision_trees
# WRITER : Adam Shtrasner 
# WEB PAGES I USED:
# https://stackoverflow.com/questions/31369262/python-list-of-frequent-occurrences-in-a-list-of-strings
# https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value


from itertools import combinations
import copy


class Node:
    def __init__(self, data, positive_child=None, negative_child=None):
        self.data = data
        self.positive_child = positive_child
        self.negative_child = negative_child

    def set_data(self, data):
        # added: a function that receives data and sets it to the node.
        self.data = data


class Record:
    def __init__(self, illness, symptoms):
        self.illness = illness
        self.symptoms = symptoms


def parse_data(filepath):
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.strip().split()
            records.append(Record(words[0], words[1:]))
        return records


class Diagnoser:
    def __init__(self, root):
        self.root = root

    def diagnose_helper(self, symptoms, node):
        """
        :param symptoms: a list of strings - each string is
        some illness' symptom.
        :param node: a Node object.
        :return: a Node object, which is the diagnosis of an illness according
        to given symptoms and a given symptoms tree(returns the illness - a string)
        """
        if node.positive_child is None and node.negative_child is None:
            return node.data
        for symptom in symptoms:
            if symptom == node.data:
                symptoms.remove(symptom)
                return self.diagnose_helper(symptoms, node.positive_child)
        return self.diagnose_helper(symptoms, node.negative_child)

    def diagnose(self, symptoms):
        """
        :param symptoms: a list of strings - each string is
        some illness' symptom.
        :return: the program returns the diagnosis according to the symptoms given(a string).
        """
        symptoms_helper = symptoms[:]
        return self.diagnose_helper(symptoms_helper, self.root)

    def calculate_success_helper(self, illness, symptoms):
        """
        :param illness: a string that represents an illness.
        :param symptoms: a list of strings - each string is
        some illness' symptom.
        :return: the program return True if the illness given is the diagnosis
        according to given symptoms, False otherwise.
        """
        if illness == self.diagnose(symptoms):
            return True
        return False

    def calculate_success_rate(self, records):
        """
        :param records: a list of Record objects.
        :return: the program counts the number of times each record's illness in the records' list
        matches the diagnosis of the record according to its symptoms, and returns the division
        between that number and total number of records.
        """
        counter = 0
        for record in records:
            if self.calculate_success_helper(record.illness, record.symptoms):
                counter += 1
        return counter / len(records)

    def all_illnesses_helper(self, illnesses, node):
        """
        :param illnesses: list of strings - each string is an illness
        :param node: a Node object(a root)
        The program returns a list with illnesses. each illness appears in the list the same
        number of times it appears in the tree.
        """
        if node.positive_child is None and node.negative_child is None:
            if node.data is not None:
                illnesses.append(node.data)
        else:
            self.all_illnesses_helper(illnesses, node.positive_child)
            self.all_illnesses_helper(illnesses, node.negative_child)

    def all_illnesses(self):
        """
        :return: returns a list of the tree's illnesses.
        The list is sorted in a way that the first illness is the illness that appears
        the most in the tree, and the last illness appears the less.
        """
        illnesses = []
        self.all_illnesses_helper(illnesses, self.root)
        illnesses_helper = illnesses[:]
        set_illnesses = set(illnesses_helper)
        illnesses_helper = list(set_illnesses)
        count_lst = []
        for illness in illnesses_helper:
            count_lst.append(illnesses.count(illness))
        illnesses_final = []
        count_set = set(count_lst)
        count_lst = list(count_set)
        count_lst.sort()
        count_lst.reverse()
        for k in range(len(count_lst)):
            for ill in illnesses_helper:
                if illnesses.count(ill) == count_lst[k]:
                    illnesses_final.append(ill)
        return illnesses_final

    def paths_to_illness_helper(self, illness, paths, path, node):
        """
        :param illness: a string. represents an illness.
        :param paths: the main list. lists of the path list are being appended to it.
        :param path: an empty list. boolean objects are being appended to the list.
        :param node: a Node object.
        The programs appends path lists to the given paths list. each path is a True and
        False list according to the choice in the tree('yes' for True, 'no' for False)
        """
        if node.positive_child is None and node.negative_child is None:
            if node.data == illness:
                path_helper = path[:]
                paths.append(path_helper)
            if path:
                path.pop()
        else:
            path.append(True)
            self.paths_to_illness_helper(illness, paths, path, node.positive_child)
            path.append(False)
            self.paths_to_illness_helper(illness, paths, path, node.negative_child)
            if path:
                path.pop()

    def paths_to_illness(self, illness):
        """
        :param illness: a string. represent an illness.
        :return: a list of lists. each list is a list of True and False which represents the
        path to the illness in the tree.
        """
        paths = []
        illnesses = self.all_illnesses()
        for ill in illnesses:
            if ill == illness:
                self.paths_to_illness_helper(illness, paths, [], self.root)
                break
        return paths


def most_common_illness(illnesses):
    """
    :param illnesses: a list of string. each string represents an illness.
    the list is not sorted and an illness can appears multiple times.
    :return: a list of the illnesses which appear the most in the illnesses list.
    """
    lcounts = [(illnesses.count(word), word) for word in illnesses]
    lcounts.sort(reverse=True)
    ltrending = []
    for count, word in lcounts:
        if count == lcounts[0][0]:
            if word not in ltrending:
                ltrending.append(word)
        else:
            break
    return ltrending


def change_leafs_to_most_common(tree):
    """
    :param tree: a Node object.
    The program changes the leafs in the tree(I set the leafs in the tree in a way that their data
    would be a list of illnesses which match the path to that leaf according)
    to the most common illness that match the path to
    that leaf according to the symptoms.
    """
    if tree.negative_child is None and tree.positive_child is None:
        if tree.data is not None:
            lst_common = most_common_illness(tree.data)
            tree.set_data(lst_common[0])
    else:
        change_leafs_to_most_common(tree.positive_child)
        change_leafs_to_most_common(tree.negative_child)


def diagnose_illness(root, record):
    """
    :param root: a Node object.
    :param record: a Record object.
    if all the symptoms in the tree match the symptoms in the record,
    we change the leaf's data to the record's illness. if more records match
    to the same leaf, we append that illness to the leaf.
    Same if all the symptoms in the tree don't match the symptoms in the record.
    """
    if root.negative_child is None and root.positive_child is None:
        if root.data is None:
            lst = []
            lst.append(record.illness)
            root.data = lst
        else:
            root.data.append(record.illness)
    else:
        flag = False
        for symptom in record.symptoms:  # symptoms in the record
            if symptom == root.data:
                # a symptom from records is a symptom in the node's data
                flag = True
                diagnose_illness(root.positive_child, record)
                break
        if flag is False:
            # the symptom does not exist in the record
            diagnose_illness(root.negative_child, record)


def build_tree_helper(root, symptoms, i):
    """
    :param root: a Node object.
    :param symptoms: a list of strings - each string is
    some illness' symptom.
    :param i: an interpreter.
    :return: a tree(a Node object) built in a way that the data of each node is the symptom
    in the i position, and the i is the current tree's degree at which we're at, and the leafs
    are empty.
    """
    if i < 0:
        return root
    return build_tree_helper(Node(symptoms[i], copy.deepcopy(root), copy.deepcopy(root)), symptoms, i - 1)


def build_tree(records, symptoms):
    """
    :param records: a list of Record objects.
    :param symptoms: a list of strings - each string is
        some illness' symptom.
    :return: a full tree according to the symptoms and each record in the records.
    """
    if symptoms:
        tree = build_tree_helper(Node(symptoms[len(symptoms) - 1], Node(None), Node(None)), symptoms, len(symptoms) - 2)
        for record in records:
            diagnose_illness(tree, record)
        change_leafs_to_most_common(tree)
        return tree
    if records:
        illnesses = []
        for rec in records:
            illnesses.append(rec.illness)
        return Node(most_common_illness(illnesses)[0])
    return Node(None)


def optimal_tree(records, symptoms, depth):
    """
    :param records: a list of Record objects.
    :param symptoms: a list of strings - each string is
    some illness' symptom.
    :param depth: an integer.
    :return: an optimal tree. This means a tree with the best success rate according
    to a number of symptoms from symptoms that equals to depth.
    """
    if depth == 0:
        return Node(None)
    if depth == len(symptoms) or not records or not symptoms:
        return build_tree(records, symptoms)
    lst_combinations = list(combinations(symptoms, depth))
    trees_rates = []
    rates = []
    for lst in lst_combinations:
        tree = build_tree(records, lst)
        diagnose = Diagnoser(tree)
        rate = diagnose.calculate_success_rate(records)
        rates.append(rate)
        trees_rates.append((tree, rate))
    best_rate = max(rates)
    best_tree = list(filter(lambda x: x[1] == best_rate, trees_rates))
    return best_tree[0][0]


if __name__ == "__main__":

    # Manually build a simple tree.
    #                cough
    #          Yes /       \ No
    #        fever           healthy
    #   Yes /     \ No
    # influenza   cold

    flu_leaf = Node("influenza", None, None)
    cold_leaf = Node("cold", None, None)
    inner_vertex = Node("fever", flu_leaf, cold_leaf)
    healthy_leaf = Node("healthy", None, None)
    root = Node("cough", inner_vertex, healthy_leaf)

    diagnoser = Diagnoser(root)

    # Simple test
    diagnosis = diagnoser.diagnose(["cough"])
    if diagnosis == "cold":
        print("Test passed")
    else:
        print("Test failed. Should have printed cold, printed: ", diagnosis)

    diag1 = diagnoser.paths_to_illness("healthy")
    if diag1 == [[False]]:
        print("Test passed")
    else:
        print("Test failed. Should have printed cold, printed: ", diag1)

    diag2 = diagnoser.all_illnesses()

    flu_leaf1 = Node(["fever", "cancer", "cancer"], None, None)
    cold_leaf1 = Node(["inf", "inf", "cold", "inf"], None, None)
    inner_vertex1 = Node("fever", flu_leaf1, cold_leaf1)
    healthy_leaf1 = Node(["healthy"], None, None)
    root1 = Node("cough", inner_vertex1, healthy_leaf1)

    records3 = parse_data("test4.txt")
    tree3 = build_tree(records3, ["cold", "cough"])
