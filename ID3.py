from node import Node
import math

debug = 0

def ID3(examples, default):
    '''
  Takes in an array of examples, and returns a tree (an instance of Node)
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''
    #convert missing attributes to mode
    clean_data(examples)
    if len(examples) == 0:
        return Node(default)
    else:
        if check_target_classes(examples) or check_non_trivial_split(examples):
            return Node(find_mode(examples), None, find_mode(examples))
        else:
            best_node = choose_attribute(examples)
            root = Node(best_node.label, {}, best_node.mode)
            values = best_node.children.copy()
            for key, val in values.items():
                examples_v = find_examples(root.label, key, examples)
                sub_tree = ID3(examples_v, find_mode(examples))
                root.children[key]=sub_tree
            return root



def prune(node, examples):
    clean_data(examples)
    original_pointer = node
    return call_prune(node, examples, original_pointer)

def call_prune(node, examples, original_pointer):
    if node.children is not None:
        for branch, child_node in node.children.items():
            acc = test(original_pointer, examples)
            if not is_leaf(child_node):
                call_prune(child_node, examples, original_pointer)
            else:
                grandpa = Node(original_pointer.label, original_pointer.children, original_pointer.mode)
                node.children = None
                node.label = node.mode
                new_acc = test(original_pointer, examples)
                if new_acc < acc:
                    original_pointer.label = grandpa.label
                    original_pointer.children = grandpa.children
                    original_pointer.mode = grandpa.mode
                else:
                    acc = new_acc
                return
def is_leaf(node):
    if node.children is None:
        return True
    else:
        return False

def test(node, examples):
    clean_data(examples)
    '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''
    num_correct = 0
    for e in examples:
        picked = evaluate(node, e)
        # print('picked: ', picked)
        # print('target: ', e['Class'])
        if picked == e['Class']:
            num_correct+=1
    return num_correct/len(examples)

def evaluate(node, example):
    '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
    while node.children is not None:
        branch = example[node.label]
        next_tmp = node.children[branch]
        node = next_tmp
    return node.label

def find_mode(examples):
    values = {}
    for example in examples:
        if example['Class'] in values:
            values[example['Class']] = values[example['Class']] + 1
        else:
            values[example['Class']] = 1
    max_key, _ = find_max_value_in_dict(values)
    return max_key


def check_target_classes(examples):
    target_value = None
    for dict in examples:
        if (target_value == None):
            target_value = dict['Class']
        if dict['Class'] != target_value:
            return False
    return True

def clean_data(examples):
    column = {}
    modeDict = {}
    for example in examples:
        for key, value in example.items():
            if key not in column:
                column[key] = []
            column[key].append(value)
    for attribute, values in column.items():
        mode = get_mode_from_list(values)
        modeDict[attribute] = mode

    # print(modeDict)
    for example in examples:
        for key, val in example.items():
            if val == '?':
                example[key] = modeDict[key]
def choose_attribute(examples):
    column = {}
    for example in examples:
        for key,value in example.items():
            if key not in column:
                column[key] = []
            column[key].append(value)
    ig = {}
    for attribute, values in column.items():
        if attribute != 'Class':
            ig[attribute] = find_information_gain(values, column['Class'])

    min_key, _ = find_min_value_in_dict(ig)

    ret = Node.create_node(min_key,set(column[min_key]))
    ret.mode = find_mode(examples)
    return ret

def get_mode_from_list(values):
    value_freq = {val: values.count(val) for val in set(values)}
    maxval = 0
    maxkey = None
    for key, val in value_freq.items():
        if val > maxval:
            maxval = val
            maxkey = key
    return maxkey

def find_information_gain(values, fx):

    #Should give me a dict of each value in attribute
    #matched to the list of fx values
    '''
    Iterating through attribute and adding f(x) values to a list
    that is added to the dictionary.
    '''
    dict = {}
    for idx, value in enumerate(values):
        if value not in dict:
            dict[value] = []
        dict[value].append(fx[idx])
    ig = 0
    denom = len(values)
    sum = 0
    for key, value in dict.items():
        sum += len(value)
        ig += calculate_ig(key, value, denom)
    return ig

def calculate_ig(key, lst_of_values, denom):
    prob = len(lst_of_values)/denom
    value_freq = {val:lst_of_values.count(val) for val in set(lst_of_values)}

    sum = 0
    for key, value in value_freq.items():
        term1 = value/len(lst_of_values)
        sum += term1*math.log2(term1)
    return -sum*prob


def find_min_value_in_dict(dict):
    min_val = None
    min_key = None
    for key,value in dict.items():
        # print(key, value)
        if min_val is None:
            min_val, min_key = value, key
        if min_val > value:
            min_val, min_key = value, key
    return min_key,min_val
def find_max_value_in_dict(dict):
    max_val = None
    max_key = None
    for key,value in dict.items():
        if max_val is None:
            max_val, max_key = value, key
        if max_val < value:
            max_val, max_key = value, key
    return max_key,max_val

def find_examples(label, value, examples):
    lst_of_examples =  []
    for example in examples:
        if example[label]==value:
            new_example = {} # Filtering out the attribute that was split on.
            for key, val in example.items():
                if key != label:
                    new_example[key] = val
            lst_of_examples.append(new_example)
    return lst_of_examples



def check_non_trivial_split(examples):
    column = {}
    for example in examples:
        for key, value in example.items():
            if key != 'Class':
                if key not in column:
                    column[key] = set()
                column[key].add(value)
    for key, val in column.items():
        if len(val) > 1:
            return False
    if debug:
        print("trivial split for ", column)
    return True
########
def entropy(pos=0, neg=0):
    sum = pos+neg
    res = (pos/sum)*math.log2(pos/sum)+(neg/sum)*math.log2(neg/sum)
    return res
