# Fantastic-Music-Player
Graphical Music Player using python
_____________________________________________________________________________
Fantastic Music Player
    With the help of this application, you don't need to visit YouTube, everytime you want to listen your favourite song. You can create your playlist of your favourite songs and play them easily
## Dependencies
[Python](https://www.python.org/)
    Used as a backend
PyQt5
    Graphics Library
requirements.txt
    All the required modules
## Controls
<ol>
1. On Screen Controls
<ol type='a'>
    <li>Play/Pause Button</li>
        <ul type='circle'>
            <li>Used to Play or Pause the media.Play media if has been yet, else pause the media</li>
        </ul>
    <li>Volume Down Button</li>
        <ul type='circle'>
            <li>
                Used to Decrease Media Volume by 3
            </li>
        </ul>
    <li>Volume Up Button</li>
        <ul type='circle'>
            <li>
                Used to Turn up the media volume by 3
            </li>
        </ul>
    <li>Stop Button</li>
        <ul type='circle'>
            <li>Stops the current media. Once stopped, on playing media, it will starts for beginning.</li>
        </ul>
    <li>Next/Previous Button</li>
        <ul type='circle'>
            <li>
                Change to Next/Previous media as it's labeled
            </li>
        </ul>
    <li>Mute Button</li>
        <ul type='circle'>
            <li>
                Used to mute the volume of media
            </li>
    </ul>
    <li>Download Button</li>
        <ul type='circle'>
            <li>
                Used to download currently loaded/Playing media to your local directory (Downloads Folder within this application installation folder)
            </li>
        </ul>
    <li>Update Button</li>
        <ul type='circle'>
            <li>Used to add new Musics to Playlist</li>
        </ul>
    <li>Vertical Slider</li>
        <ul type='circle'>
            <li>Used to adjust volume</li>
        </ul>
    <li>Horizontal Slider</li>
    <ul type='circle'>
        <li>Used to show current progress of media and can also be used as a seekbar i.e jummping to certain position (Note: To Use seekbar to some position, media must be paused)</li>
    </ul>
</ol>
2. OffScreen Controls
<ol type='a'>
    <li>
        Left Arrow
    </li>
    <ul type='circle'>
        <li>Used to Go 5000 ms (5 Second) Frame Back</li>
    </ul>
        <li>
        Right Arrow
    </li>
    <ul type='circle'>
        <li>Used to Go 5000 ms (5 Second) Frame Forward</li>
    </ul>
        <li>
        Up Arrow
    </li>
    <ul type='circle'>
        <li>Increase volume by 5</li>
    </ul>
        <li>
        Down Arrow
    </li>
    <ul type='circle'>
        <li>Decrease volume by 5</li>
    </ul>
    <li>
        Key S
    </li>
    <ul type='circle'>
        <li>Stops currently playing media</li>
    </ul>
    <li>
            Key M
    </li>
    <ul type='circle'>
        <li>Mute and Unmute Current media</li>
    </ul>
    <li>
            Ctrl+D
    </li>
    <ul type='circle'>
        <li>Download Current media</li>
    </ul>
</ol>

## Content Included
01. Icon (Directory): Contains all the icons used in the Graphical Interface
02. [Fantastic Music Player.exe](https://github.com/Sachinacharya-Project/Fantastic-Music-Player/blob/main/Fantastic%20Music%20Player.exe) (Executable) is the Installer of the application
03. Fantastic Music Player.zip (Archive) is a zip file which can be extracted to use application directly (Without installing)
04. Rest are the core of the application for developer (Edit accordingly)
## Installation
1. [Download](https://github.com/Sachinacharya-Project/Fantastic-Music-Player/blob/main/Fantastic%20Music%20Player.exe) Installer for Windows
2. Once downloaded, check in default download folder and then double click the downloaded application.
3. Follow up as prompted.
4. Choose installation path and all carefully and now start using files by navigating to installation path and clicking Fantastic Music Player.exe file
## Error Handelling
(Must read before installations)
Sometime you might get some error after installation like below
<br>
<img src="./Error Handles/step-1.png">
<br>
If you got error something like this you need to provide administrator permission to the the file or you can install the program somewhere else that doesn't require administrator previlege like in another drive or something or to Desktop, you get the idea!
<br><br>
If you want don't want to change the default directory or had already installed it and facing the problem, here is the solution
<br><br>
Right-Click on the Desktop icon of Fantastic Music Player
<br><br>
<img src="./Error Handles/step-0.png">
<br><br>
You will see something like this
<br><br>
<img src='./Error Handles/step-2.png'>
<br><br>
Now click on properties and something like this prompt up in the screen
<br><br>
<img src="./Error Handles/step-3.png">
<br><br>
Click on Advance option under shortcut heading
And you will get something like this
<br><br>
<img src="./Error Handles/step-4.png">
<br><br>
Check the "Run as Administrator" option and click OK
and again click Apply and OK
<br><br>
<img src="./Error Handles/step-5.png">
<br><br>
Now run the program with no error.