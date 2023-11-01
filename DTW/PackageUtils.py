from PIL import Image

def create_icon(image_path, icon_path, sizes=((16,16), (32,32), (48,48), (64,64),(1024,1024))):
    img = Image.open(image_path)
    img.save(icon_path, format='ICO', sizes=sizes)

create_icon('ToGithub/DTW/DSP.png', 'ToGithub/DTW/DSP.ico')
