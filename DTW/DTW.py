# -----------------------------------------
# @Description: This file uses DTW method to recognize speech number signal.
# @Author: Yiwei Ren.
# @Date: 十一月 01, 2023, 星期三 14:42:25
# @Copyright (c) 2023 Yiwei Ren. All rights reserved.
# -----------------------------------------


import librosa
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

class DTW():
    '''
        Class to dtw recognization
    '''

    def __init__(self, pattern_root, default_pattern = 0) -> None:
        '''
            Arguments:
                pattern_root: root path of patterns
                default_pattern: the index of pattern. Default=0
        '''
        self.pattern_root = pattern_root
        self.default_pattern = default_pattern
    
    def extract_mfcc(self, audio_path):
        y, sr = librosa.load(audio_path) 
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=24)
        return mfccs.T

    def dtw_distance(self, template, test):
        distance, _ = fastdtw(template, test, dist=euclidean)
        return distance

    def __call__(self, test_file):
        '''
            Arguments:
                test_file: the .wav file need to be DTW recognized
        '''
        import os
        for num in range(10):
            pattern_file = os.path.join(self.pattern_root, f'{num}_{self.default_pattern}.wav')
            pattern_mfcc = self.extract_mfcc(pattern_file)
            test_mfcc = self.extract_mfcc(test_file)
            dis = self.dtw_distance(pattern_mfcc, test_mfcc)
            if num == 0:
                predict = 0
                mindis = dis
            else:
                if dis < mindis:
                    mindis = dis
                    predict = num
        return predict

if __name__ == '__main__':
    classifier = DTW('RenAudio')
    classifier('RenAudio/9_2.wav')

