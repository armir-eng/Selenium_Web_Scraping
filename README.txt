In order to obtain a working execution, you should follow these instructions:

- Go to the projects folder in teminal or CMD (if you are using an advanced IDE just open folder's project or type " cd 'folder's path' " in the terminal)

- Firstly, activate the virtual enviroment in the terminal (or CMD in Windows) with this command --> .env\Scripts\activate
    - This way, libraries needed, installed in this venv, are usable.

- Then, the most important thing is to get a Chrome webdriver, matching the Chrome browser's current variant:

    - To get the current version of Chrome you are using:
        - Open Chrome
	- Click the 3-dots button, adjacent to the user's profile icon (colored circle with the first letter of the username)
	- In the dropdown menu opened, go to "Help"
	- Then, in the list appeared, click the "About Chrome" button.
	- In the new tab, you will see the exact Chrome version used in the current moment (e.g: 110.0.5481.178)

    - After being aware of the Chrome's version you use in your computer:
	- Go to this URL: https://chromedriver.chromium.org/downloads
	- Get the matching webdriver version	
	    - You will see this kind of instruction: "If you are using Chrome version 110, please download ChromeDriver 110.0.5481.77"
            - If your Chrome's version is "110.0.5481.178", then get the webdriver whose version contains "110.0.5481" or if it is "111.0.5563.2", then get the webdriver's version that contains "111.0.5563".
	    - Click the respective link
	    - If you use Windows, click the link with the text "chromedriver_win32.zip"
	    - Then, extract the zip file and get the executable file, and place it in the project's folder.
	    - Then you'll get a correctly working execution.


- Finally, run the "main.py" module.
