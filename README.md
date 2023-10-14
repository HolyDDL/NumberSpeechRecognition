# Audio Digital Signal Processing

## Data Collection

.wav文件命名格式 NUM_TIMES.wav, NUM表示录音数字, TIMES表示次数

- 开启后进入循环, 先输入需要采集的数字(用于自动命名.wav文件)
- 每次要收集该数字数据时, 输入any key(除了q和c). 回车后进行2s的录音转wav
- 更改数字时, 输入c, 回车. 然后在提示后输入数字, 回车. **此时.wav文件命名将从该数字的0开始**
- 要结束. 输入q
- 要更改录音时长改动`record_audio(f'{number}_{global_times}.wav')`为`record_audio(f'{number}_{global_times}.wav'), record_second=NUMBER`将录音NUMBERs.
- 采样率RATE, 采样深度FORMAT, 每个缓冲采样数量CHUNK进入`record_audio`体内修改

## ExtractFeature

需要读取./DataSet/下的文件.
ExtractFeature.py 下有数据处理的类DataProcessing()

- 提取特征时, 先将`DataProcessing(FilePath:str, segmet_time = 30e-3, cover_time = 10e-3, amp_threshold=5, cr_threshold=0.05)`实例化.
- 再调用`DataProcessing.FeatureDetect(plot=False, plot3d=False, window_type='hanning')`函数提取特征. `window_type`用于选取窗函数.
- 函数将会返回三个特征, `amps, crs, seg_fre`, 每个返回的特征维度为:(N,), 即帧数.
- 相同样本的三个特征的维数(帧数)是相同的. 但是不同的样本提取出的帧数是不同的.

## FeatureSave

存储数据特征原始文件和特征归一化的结果.

- 存储时, 先将`SaveFeature(source_dir, destination_dir, destination_name='Cluster_Data.csv', window_type='hanning')`实例化. `source_dir`是原始数据集根目录位置. `destination_dir`是特征提取后特征文件保存的根目录. `destination_name`是特征文件存储的名字. `window_type`是选择分帧的窗函数.
- 再调用`SaveFeature.GetData()`得到数据集文件.
- 最后调用`SaveFeature.CulsterData()`进行特征归一化.