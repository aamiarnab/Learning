import time
import webbrowser

i = 0
while i < 3:
    print ("Start your work ", time.ctime())
    time.sleep(10)
    print ("Break number ", i+1, " starts at ", time.ctime())   
    webbrowser.open("https://www.youtube.com/watch?v=EPYupizJYQI")
    i +=1


