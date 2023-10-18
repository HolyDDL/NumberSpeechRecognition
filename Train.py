# -----------------------------------------
# @Description: This file include a class to train data and predict data using svm
# @Author: Yiwei Ren.
# @Date: 十月 18, 2023, 星期三 22:34:12
# @Copyright (c) 2023 Yiwei Ren. All rights reserved.
# -----------------------------------------

import numpy as np
from tqdm import tqdm

class SVM_Classify():
    '''
        Use svm to train svm and use it to predict new data
    '''

    def __init__(self, dataset_root, dataset_name, model_root, model_name) -> None:
        '''
            Arguments:
                dataset_root: the root dir saved feature for training
                dataset_name: the name of the feature data for training
                model_root: the root dir for saving models
                model_name: the filename for saving models
        '''
        self.dataset_root = dataset_root
        self.dataset_name = dataset_name
        self.model_root = model_root
        self.model_name = model_name

    def load_feature_data(self):
        import os
        import csv
        print('Loading feature data...')
        dataset = os.path.join(self.dataset_root, self.dataset_name)
        dataframe = []
        labelframe = []
        with open(dataset) as file:
            reader = csv.reader(file)
            for row in reader:
                dataframe.append([float(x) for x in row[:-1]])
                labelframe.append(float(row[-1]))
        print(f'Load feature data successfully! Loaded {len(dataframe)} pieces data')
        return np.array(dataframe, dtype=np.float64), np.array(labelframe, dtype=np.int8)
    
    def make_model(self):
        import os
        dir = os.path.exists(self.model_root)
        if not dir:
            os.mkdir(self.model_root)
        model_file = os.path.join(self.model_root, self.model_root)
        return model_file
    
    def Train(self, nu_min = 0.001, nu_max = 0.7, iter_times = 1000):
        '''
            Arguments:
                nu_min: the minimum value of nu argument in NuSVC(). Default=0.001
                nu_max: the maximum value of nu argument in NuSVC(). Default=0.7
                iter_times: set searching times between nu_min and nu_max to optimize NuSVC. Default=1000
        '''
        from sklearn.svm import NuSVC
        import pickle
        pre_data, pre_label = self.load_feature_data()
        index = np.random.permutation(pre_data.shape[0]) # random data
        data = pre_data[index, :]
        label = pre_label[index]
        train_set_len = int(len(data)*4 / 5)
        print(f'The train dataset length is {train_set_len}, and val dataset length is {len(data) - train_set_len}')
        maxsc = 0
        maxi = 0
        model_file = self.make_model()
        scale = np.linspace(nu_min,nu_max,iter_times)
        for i in tqdm(scale):
            clf = NuSVC(nu=i,kernel='rbf',gamma='scale')
            clf.fit(data[:train_set_len], label[:train_set_len])
            sc = clf.score(data[train_set_len:], label[train_set_len:])
            if sc > maxsc:
                s =pickle.dumps(clf)
                with open(model_file, 'wb') as f:
                    f.write(s)
                maxsc = sc
                maxi = i
        print(f'the best val accuracy is {maxsc*100:.2f}%, and the best nu is {maxi}')

    def Predict(self, features:np.array):
        '''
            Argument:
                features: input features of data for prediction
        '''
        import pickle
        model_file = self.make_model()
        with open(model_file, 'rb') as f:
            clf = pickle.loads(f.read())
        features = np.array(features)
        if features.ndim == 1:
            features = features[np.newaxis,:]
        return clf.predict(features)

if __name__ == '__main__':
    classifyer = SVM_Classify('WindowTypes/RectangleWindow', 'All_DATA.csv','Models','svm_model.pkl')
    classifyer.Train()