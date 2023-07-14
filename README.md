Simple pixelscanner orbwalker using python

How it works: It will take a screenshot and look for image.jpg in it using opencv's image matching algorithm, then calculate the timing etc of your auto attacks

Important:
Bind player move click to "k" and player attack move click to "l".
Needs to pip install a few libraries such as opencv-python, pywin32, pydirectinput, requests
You will need to replace the float t in line 17 with your pc's calculation time. You can just play around with the value until it won't cancel auto attacks anymore and not wait too long after each auto attack.
