# TextureGenerator
A program that uses OpenCV and NumPy to generate output images using a background and an overlay image that get recolors by using an input file

The program takes a text file as input to define variables  the format is as follows:
```
<static background image location>
<intensity map image for colored overlay>
<what to put after the name for the color in the output image>
<the output location for the images>
<the output location for the name transformation csv>
[list of name, color pairs
<name1>| (<red1>,<green1>,<blue1>)
<name2>| (<red2>,<green2>,<blue2>)
...
...
<nameN>| (<redN>,<greenN>,<blueN>)
]
```
#See Below or frogs.txt as an example
```
input\blank.png
input\frog.png
_frog.png
C:\Users\frogm\source\repos\TextureGenerator\TextureGenerator\frogs\
C:\Users\frogm\source\repos\TextureGenerator\TextureGenerator\frogs\nameTransform.csv
maroon| (128,0,0)
dark_red| (139,0,0)
brown| (165,42,42)
firebrick| (178,34,34)
crimson| (220,20,60)
red| (255,0,0)
tomato| (255,99,71)
coral| (255,127,80)
```
