# ImageOptimizedScript

---
### Pillow script app to optimize your images by using your os iu

### run 
* Step 0 (Optional) -> Create virtual env
```
python3 -m venv env
source env/bin/activate
```
* Step 1 -> Install requiremts
```
pip3 install -r requirements.txt
```
* Step 2 -> Run
```
python3 main.py
```

### Usage
After first init the script **will check** files
* readme.txt file -> Contain the docs of the script

Usage is really simple if you just want to optimize images of current folder with default values just run 
```
python3 main.py
```

And images will be optimized with 60% in current folder

Also we have params to customize the execution

***These params are***
* img=example.jpg -> image to optimize / default * (all)
* q=55                     -> quality to optimize / default 60 %
* c_directory="new_folder" -> folder to search images / default "." (current directory)
* output="new_folder"      -> folder where found images / default "." (current directory)
* help -> show params

Example
```
python3 main.py image=example.png q=70 output=optimized_one
```

this command will create a folder named optimized_one with a copy of example.png optimized at 70%






