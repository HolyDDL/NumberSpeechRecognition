# -----------------------------------------
# @Decription: this file aim to save a file that saved normalized feature data and labels, which can be used in classification
# @Author: Yiwei Ren.
# @Date: 十月 14, 2023, 星期六 08:40:23
# @Copyright (c) 2023 Yiwei Ren.. All rights reserved.
# -----------------------------------------

import ExtractFeature
import os
import csv
import re
import tqdm
import numpy as np

class SaveFeature():
    '''
        Save a file that includes normalized feature data and labels.
    '''

    def __init__(self, source_dir, destination_dir, destination_name='Cluster_Data.csv', window_type='hanning') -> None:
        '''
            Arguments:
                source_dir: root path of dataset
                destination_dir: root path of files that saved features and labels
                destination_dir: name of files that saved feature and labels. Default='Cluster_Data.csv'
                window_type: the function of window for processing segment audio data. Default='hanning', Optional: 'hanning', 'hamming', 'rectangle'

        '''
        self.source_dir = source_dir
        self.destination_dir = destination_dir
        self.Original_data_name = 'Original_Data.csv'
        self.cluster_data_name = destination_name
        self.window_type = window_type

    def getfiles(self):
        file_names = os.listdir(self.source_dir)
        return file_names
    
    def extract_features(self):
        file_names = self.getfiles()
        all_files_features = []
        print('Extracting Features...')
        for i in tqdm.tqdm(range(len(file_names))):
            name = file_names[i]
            number_times = re.findall(r'[0-9]', name)
            print(f'Extrtacting number={number_times[0]}, times={number_times[1]}')
            number = int(number_times[0])
            wavefile = ExtractFeature.DataProcessing(os.path.join(self.source_dir, name))
            amps, crs, seg_fres = wavefile.FeatureDetect(window_type=self.window_type)
            features = np.concatenate((amps, crs, seg_fres,[number]))
            all_files_features.append(features)
        print('done!')
        return all_files_features
    
    def load_data(self):
        orifile = os.path.join(self.destination_dir, self.Original_data_name)
        data_frame = []
        with open(orifile) as file:
            reader = csv.reader(file)
            for row in reader:
                if eval(row[0]) == -1:
                    continue
                else:
                    data_frame.append([float(x) for x in row])
        print(f'loaded {len(data_frame)} pieces data')
        return data_frame
    
    def normalize(self,data_frame):
        maxium = np.ones(3)
        minium = np.zeros(3)
        for data in data_frame:
            n = len(data) - 1
            for i in range(3):
                d = n/3
                imax = np.max(data[int(i*n/3):int((i+1)*n/3)])
                imin = np.min(data[int(i*n/3):int((i+1)*n/3)])
                if imax > maxium[i]:
                    maxium[i] = imax
                if imin < minium[i]:
                    minium[i] = imin
        new_frame = []
        for j,data in enumerate(data_frame):
            n = len(data) - 1
            for i in range(3):
                data[int(i*n/3):int((i+1)*n/3)]/= (maxium[i] - minium[i])
            new_frame.append(data)
        return new_frame
    
    def CulsterData(self):
        from sklearn.cluster import KMeans
        frame = self.normalize(self.load_data())
        culs_points = []
        for data in frame:
            n = len(data) - 1
            points = []
            class_num = data[-1]
            for j in range(int(n/3)):
                point = [data[j], data[int(n/3)+j], data[int(n*2/3)+j]]
                points.append(point)
            points = np.array(points)
            cluster = KMeans(2, random_state=0,n_init='auto').fit(points)
            centroid=cluster.cluster_centers_
            if centroid[0][2] > centroid[1][2]:
                centroid[[0,1],:] = centroid[[1,0],:]
            culsterpoint = centroid.ravel()
            culsterpoint = np.concatenate((culsterpoint, [class_num]))
            culs_points.append(culsterpoint)
        culs_points = np.array(culs_points)
        self.save_data(self.cluster_data_name, culs_points)
        return culs_points

    def save_data(self, name, data_matrix):
        dir = os.path.exists(self.destination_dir)
        if not dir:
            os.mkdir(self.destination_dir)
        desfile = os.path.join(self.destination_dir, name)
        with open(desfile,'w') as file:
            print(f'Saving Data to {name}... ')
            writer = csv.writer(file)
            writer.writerows(data_matrix)
            print('Save Success!')

    def GetData(self):
        self.save_data(self.Original_data_name, self.extract_features())
        
if __name__ =='__main__':
    saver = SaveFeature('LiAudio','RectangleWindow','Li_DATA.csv','rectangle')
    saver.GetData()
    saver.CulsterData()