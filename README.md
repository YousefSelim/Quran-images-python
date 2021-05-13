# بسم الله الرحمن الرحيم
# Quran-images-python
Python generated Quran page using king fahd complex fonts ,and marker positions in json file
# installation and requirements
Built using python 3.6<br>
needs PIL (python image library):<br>
install PIL -> pip3 install PIL
# Generating images
just run main.py ->python3 run main.py<br>
Output folder is "_out" , you should find 604 pages + json file containing ayah marker positions

# tweaks and settings
In main.py you would find 3 variables: <br><br>
1-export_images : this defaults to true , if false no image will be generated just the ayah markers json file<br><br>
2-debug : this draws rectangles around every marker and every line to make debugging and checking their validity easier<br><br>
3-factor: the resolution factor of generated images for larger screens , increasing factor will increase the resolution but with the same aspect ratio (originally 1024*1690).
Please note that increasing factor will increase processing time of each page



