
# Sleep Quality Assessment Application

This docker application is for Sleep Quality Assessment. It is developed in Ubuntu18.04 environment.

### Installation

1. Clone the repository to the working directory.
2. Change the paths of data storation customly in the code. Create directories to store ecg, fitbit and polar data.  
3. Open the terminal in the current directory. Build the image.  
    `docker build -t databox_app:2`
4. Enable X connection of the docker.  
    `xhost +local:docker`
5. Run the container of the application. The path of volume is changed following users' own data paths.  
    `docker run -it -v /tmp/.X11-unix:/tmp/.X11-unix -v /home/gaoziang/databox:/home/gaoziang/databox -e DISPLAY=$DISPLAY databox_app:2 python3 app/gui.py`  

### Sensor Registration

Create directory 'device_config' in 'dt' directory to store config information of two sensors.

* Fitbit Alta HR  
    Enter in [the developer page of Fitbit](https://dev.fitbit.com/) and log in using Fitbit account. Request client id and client secret to retrieve data from Fitbit Alta HR. When users run fitbit mode at first time, write down client information.
* Polar H10
    Go to [PolarAccessLink page](https://admin.polaraccesslink.com/) and log in using your Polar Flow credentials or create new Flow account. Fill your application/service information to create a client. After client is created, write down OAuth2 clientID and secret into the application when you enter in polar mode at first time.
