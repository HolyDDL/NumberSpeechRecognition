from DTW import DTW
import numpy as np
from tqdm import tqdm

class Test_DTW():

    def __init__(self, Pattern_root, val_set, savefile) -> None:
        self.Pattern_root = Pattern_root
        self.Val_set = val_set
        self.val_range = range(1,10)
        self.numbers = range(10)
        self.savefile = savefile

    def _test_dtw(self):
        import os
        classifier = DTW(self.Pattern_root, 1)
        pred_matrix = np.zeros((len(self.numbers), len(self.val_range)+1))
        for real_num in tqdm(self.numbers, desc='All times'):
            pred_matrix[real_num][0] = real_num
            for index in tqdm(self.val_range, desc=f'in number {real_num}', leave=False):
                file = os.path.join(self.Val_set, f'{real_num}_{index}.wav')
                pred = classifier(file)
                pred_matrix[real_num][index] = pred
                # print(f'at number: {real_num}_{index}') 
        return pred_matrix
    
    def save_matrix(self):
        import csv
        data_matrix = self._test_dtw()
        with open(self.savefile,'a') as file:
            writer = csv.writer(file)
            writer.writerows(data_matrix)

if __name__ == '__main__':
    tester = Test_DTW('LiAudio', 'LiAudio', 'test_result.csv')
    tester.save_matrix()
    tester = Test_DTW('MaAudio', 'MaAudio', 'test_result.csv')
    tester.save_matrix()
    tester = Test_DTW('RenAudio', 'RenAudio', 'test_result.csv')
    tester.save_matrix()
