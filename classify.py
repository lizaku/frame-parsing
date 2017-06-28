from sklearn.naive_bayes import MultinomialNB
#gnb = GaussianNB()

from sklearn.preprocessing import label_binarize
from sklearn.linear_model import SGDClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import average_precision_score, roc_curve, auc, \
    precision_recall_curve, accuracy_score, roc_auc_score, classification_report
from sklearn.externals import joblib
from sklearn import grid_search
import csv
import numpy
from scipy import interp
from sklearn.externals import joblib

def import_csv(path):
    """
    Import feature data from a given csv file
    :param path: path to CSV file containing tokens and features
    :return features and target tags as numpy arrays
    """
    with open(path) as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader, None)  # skip header

        data = []
        target = []
        for row in reader:
            data.append(row[:-1])
            target.append(row[-1])

        # convert to numpy arrays
        data = numpy.array(data)
        target = numpy.array(target)
    return data, target
    

def import_as_dict(path):
    """
    Import feature data from a given csv file
    :param path: path to CSV file containing tokens and features
    :return features and target tags as sparse matrices
    Should deal with categorical input.
    """

    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader, None)

        data = []
        target = []

        # read things from csv
        for row in reader:
            data.append(dict(zip(header[:-1], row[:-1])))  # make a dict of feature : value
            target.append(row[-1])

        from sklearn.feature_extraction import DictVectorizer
        vec = DictVectorizer()

        # convert categorical features to floats
        data_matrix = vec.fit_transform(data)
        v = vec.transform(data[1])

        # convert targets to numpy array as strings
        target_matrix = numpy.array(target)

        # save converter to use in prediction
        #joblib.dump(vec, 'feature_transformer.pkl')
    #target_names = set(target)
    joblib.dump(vec, 'feature_transformer.pkl')
    return data_matrix, target_matrix #, target_names
    

if __name__ == '__main__':
    import warnings
    warnings.filterwarnings("ignore")

    # import data
    print("Import data")
    data, target = import_as_dict('arguments_roles_merged.csv')
    print(data.shape, target.shape)
    # todo early stopping

    # split data into train and test subsets
    print("Split data")
    data_train, data_test, target_train, target_test = train_test_split(data, target)
    #y = label_binarize(target, classes=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
    #n_classes = y.shape[1]
    #print(n_classes)
    # greedy()
    
    #clf = MultinomialNB()
    clf = SGDClassifier(penalty='elasticnet', eta0=0.00390625, learning_rate='constant', alpha=1e-06, loss='hinge')
    y_score = clf.fit(data_train, target_train) #.decision_function(data_test)
    y_true, y_pred = target_test, clf.predict(data_test)
    print(classification_report(y_true, y_pred))
    joblib.dump(clf, 'frame_parser.pkl')
    #print(y_score)
