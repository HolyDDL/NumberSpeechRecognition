# -----------------------------------------
# @Description: This file is for prediction.
# @Author: Yiwei Ren.
# @Date: 十月 25, 2023, 星期三 12:10:29
# @Copyright (c) 2023 Yiwei Ren. All rights reserved.
# -----------------------------------------

from Train import SVM_Classify
from DataCollection import record_audio
from ExtractFeature import DataProcessing
import numpy as np

class Predict():
    '''
        Record a piece of audio and predict the number of it.
    '''
    def __init__(self, model_root, model_name) -> None:
        '''
            Arguments:
                model_root: the dir that saved svm model data
                model_name: model_root/model_name is the svm model data.
        '''
        self.model_root = model_root
        self.model_name = model_name

    def del_temp_files(self, path):
        import os
        for i in os.listdir(path):
            if os.path.isdir(os.path.join(path,i)):
                self.del_temp_files(os.path.join(path,i))
            os.remove(os.path.join(path,i))
        os.rmdir(path)

    def temp_file_path(self, path):
        import os
        folder = os.path.exists(path)
        if not folder:                 
            os.mkdir(path)
        return os.path.join(path,'temp.wav')

    def collection(self):
        audio_path = self.temp_file_path('temp')
        record_audio(audio_path)

    def feature_processing(self):
        wavefile = DataProcessing('temp/temp.wav')
        amps, crs, seg_fres = wavefile.FeatureDetect(window_type='rectangle')
        features = np.concatenate((amps, crs, seg_fres))
        normailized_data = self.normalize(features)
        point = self.culster_data(normailized_data)
        return point
       
    def culster_data(self, normailized_data):
        from sklearn.cluster import KMeans
        n = len(normailized_data)
        points = []
        for j in range(int(n/3)):
            point = [normailized_data[j], normailized_data[int(n/3)+j], normailized_data[int(n*2/3)+j]]
            points.append(point)
        points = np.array(points)
        cluster = KMeans(2, random_state=0,n_init='auto').fit(points)
        centroid=cluster.cluster_centers_
        if centroid[0][2] > centroid[1][2]:
            centroid[[0,1],:] = centroid[[1,0],:]
        culsterpoint = centroid.ravel()
        return np.array(culsterpoint)
    
    def normalize(self,data):
        maxium = np.ones(3)
        minium = np.zeros(3)
        n = len(data)
        for i in range(3):
            d = n/3
            imax = np.max(data[int(i*n/3):int((i+1)*n/3)])
            imin = np.min(data[int(i*n/3):int((i+1)*n/3)])
            if imax > maxium[i]:
                maxium[i] = imax
            if imin < minium[i]:
                minium[i] = imin
        new_frame = []
        for i in range(3):
            data[int(i*n/3):int((i+1)*n/3)]/= (maxium[i] - minium[i])
        new_frame.append(data)
        return np.array(new_frame).squeeze()

    def __call__(self):
        self.collection()
        data = self.feature_processing()
        classfier = SVM_Classify('','',self.model_root, self.model_name)
        ans = classfier.Predict(data)
        print(f'Predicted number is {ans}')
        self.del_temp_files('temp')

if __name__ == '__main__':
    pred = Predict('Models','svm_model.pkl')
    pred()