# mysidewalk data engineer take home project
 
How to run program:
1. Unzip and extract using 7zip
2. Copy desired source data (input) file into the same directory as main.py
    or use the source data that is already in directory ('Fire_Department_Calls_for_Service.csv')
    2a. If you are copying over your own data input csv file. Alter the text on line 14 of main.py from 'Fire_Department_Calls_for_Service.csv' to the name of your source file. 
3. No arguments are needed to run the program. Simply run the program by calling your python3 path followed by the name of this program (main.py).
    i.e. 'C:/Users/Andrew/AppData/Local/Programs/Python/Python38-32/python.exe c:/Users/Andrew/OneDrive/Desktop/mysidewalk/main.py'
    3a. Also depending on which code editor you are using, you can potentially just right click anywhere in main.py and click 'run Python file from terminal'


What does program do?
Program creates 2 files, 'main_output.csv' and 'errors_output.csv'
main_output.csv consists of the requested data per the instructions. 
errors_output.csv shows the instances where there was data that I determined was not valid for main_output.csv
    The instances where I put the resulting data in errors_output.csv instead of main_output.csv is when either of these two conditions occured:
        1. The response time (on scene time - received time) was a negative value; i.e. they claimed to have arrived before the dispatch call was received.
        2. The response time was zero; i.e. the on scene time and received time were identical. 
            2a. I chose not to include this in the final results because it didn't feel valid to analyze the response time of the data set while allowing instances to skew the results where the unit was already on scene when the call was received. 


Other files included in this folder, and what they are:
DataStructurePlan.jpg: This shows my thought process of when I was brainstorming and coming up with an appropriate datastructure (dictionary) to store the data in.
notes.txt: includes some notes I took for myself to track some things I needed to do down the stretch of building this project.
sources-used.txt: this file sites the docs/sources that helped me build this project as well as a quick description of what I used the reference for

Thank you for taking the time to look over my project. 
-Andrew 