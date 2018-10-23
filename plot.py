import matplotlib
import parse
import random
import ID3
from random import shuffle

# importing the required module
import matplotlib.pyplot as plt

def plot(inFile):

    accuracy_per_epoch_without_pruning = []
    accuracy_per_epoch_with_pruning = []
    data = parse.parse(inFile)
    num_training = 10
    goal_training = 300
    step_training = 1

    x_axis = range(num_training, goal_training, step_training)



    while num_training < goal_training:
        withPruning = []
        withoutPruning = []
        for i in range(1000):
            random.shuffle(data)
            train = data[:num_training]
            valid = data[num_training:3 * len(data) // 4]
            test = data[3 * len(data) // 4:]

            tree = ID3.ID3(train, 'democrat')
            acc = ID3.test(tree, train)
            acc = ID3.test(tree, valid)
            acc = ID3.test(tree, test)

            ID3.prune(tree, valid)
            acc = ID3.test(tree, train)
            acc = ID3.test(tree, valid)
            acc = ID3.test(tree, test)
            withPruning.append(acc)
            tree = ID3.ID3(train + valid, 'democrat')
            acc = ID3.test(tree, test)
            withoutPruning.append(acc)
        accuracy_per_epoch_with_pruning.append(sum(withPruning) / len(withPruning))
        accuracy_per_epoch_without_pruning.append(sum(withoutPruning) / len(withoutPruning))
        num_training+=step_training

    themin = min(accuracy_per_epoch_without_pruning)
    themax = max(accuracy_per_epoch_without_pruning)
    step = (themin + themax) / 20

    y_axis = range(90, 98, 1)

    plt.plot(x_axis, accuracy_per_epoch_with_pruning,label='With Pruning')
    plt.plot(x_axis, accuracy_per_epoch_without_pruning, label='Without Pruning')


    # naming the x axis
    plt.xlabel('Number of examples')
    # naming the y axis
    plt.ylabel('Accuracy')
    # giving a title to my graph
    plt.title('Accuracy of decision tree on political policies')

    # show a legend on the plot
    plt.legend()
    plt.show()

if __name__ == "__main__":
    plot('house_votes_84.data')