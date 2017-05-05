### Overview
This repository contains a solution to take readings from a touch sensor and send them to cloud (Microsoft Azure) for real-time analytics, using Node.JS/Python on a Raspberry Pi running Raspbian OS.

## Workshop #1

### Steps
To get this to work, follow the steps below:

1.  Without giving power to the Raspberry Pi yet, make sure you have connected the touch sensor to the Raspberry Pi as per below. Pin mapping of Raspberry Pi  is [available here.](https://developer.microsoft.com/en-us/windows/iot/docs/pinmappingsrpi).

    -   GND of touch sensor to GND (Pin 6) of Raspberry Pi
    -   VCC of touch sensor to 5V PWR (Pin 2) of Raspberry Pi
    -   SIG of touch sensor to GPIO 2 (Pin 3) of Raspberry Pi

Refer to the image below 

![Fritzing Diagram - Touch Sensor on RPI3](/images/Fritzing_bb.png)

2.  Connect the HDMI cable from the Raspberry Pi to the Monitor. Also, connect the wired keyboard and wired mouse to the USB slots in the Raspberry Pi.

3.  Power up the Pi, by connecting it to a power socket. Wait for a minute once this is done. If you are using a **Raspberry Pi 2**, connect the WiFi module to the USB port of the Pi and follow the instructions [here](https://www.hackster.io/achindra/setting-wireless-on-raspberry-pi-f3e78d) to configure WiFi for the Pi. If you are using a **Raspberry Pi 3**, there is no need to connect a separate WiFi module, just follow the steps in the above link. 

4.  Put the Raspberry Pi and your development machine on the same network. Get the IP address of the Pi (by viewing the IP on a display connected to the Pi - go to Terminal and type ifconfig).

5.  From your laptop, ensure you are able to ping the Pi using the IP - open cmd and ping the IP. You should be getting a successful ping.
  
6.  Go back to your laptop and open a SSH client (use [Putty](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html) if you are on a Windows machine), and SSH into the Pi using its IP. Default username: pi , default password: raspberry .

7.  Open a FTP client, like Filezilla, and access the Pi using the IP. (Username and password as same, Default port as 22)

## Step 8 for NodeJS developers only
8.  Go to Putty, and follow these steps:

    ```
    git clone https://github.com/rexington/quick2wire-gpio-admin.git

    cd quick2wire-gpio-admin

    make

    sudo make install

    sudo adduser $USER gpio
    ```

    `gpio-admin export 2`
    *(Ignore the error message if any.)*
 
     `gpio-admin export 4`
    *(Ignore the error message if any.)*



9.  Go back to your laptop or ssh to your RaspberryPI and clone this repository.
    
    `git clone https://github.com/brijrajsingh/touch-sensor-azureIoT`

    `cd touch-sensor-azureIoT `

    cd to the directory of your choice nodejs or python   

10. Get the IOTHub connection string from your mentor.

11.  Install the Device Explorer utility (if on a Windows dev machine) if you don't have it already. Then, create a new device and note down the **device connection string**. [Instructions here.](https://github.com/Azure/azure-iot-sdk-csharp/tree/master/tools/DeviceExplorer). If you are on a non-Windows dev machine, use the iothub-explorer CLI tool - [instructions are here.](https://github.com/Azure/iothub-explorer)

12.  
#### NodeJS
Paste the **device connection string** obained from the above step in connectionString variable in the file nodejs/pi-gpio-to-cloud.js (which you would have obtained in your laptop after cloning the repository)

#### Python
Paste the **device connection string** obained from the above step in connectionString variable in the file python/d2cMsgSender.py (which you would have obtained in your laptop after cloning the repository)

##### You may upload the files to your raspberrypi using filezilla or you may clone this repo directly into your raspberry pi, or create these files in raspberrypi using nano editor

13.
#### NodeJs 
 SSH and Run *npm install* to install all the required dependencies automatically. This process can take about a minute or so to complete.

#### Python
[Install Azure IoT sdk for python](https://docs.microsoft.com/en-us/azure/python-how-to-install) 

14.
#### NodeJS  
Run the nodejs/pi-gpio-to-cloud.js file with sudo - *sudo node pi-gpio-to-cloud.js*. If successful, you will start seeing '-------' every one second, and as soon as you touch the touch sensor the value should be sent to Azure.

#### Python
Run the python/d2cMsgSender.py
`python d2cMsgSender.py`

as soon as you touch the touch sensor the value should be sent to Azure.

15.  The data is now being sent to Azure. You can verify that the data is being sent to Azure by using the same Device Explorer tool above. Go to the Data tab, choose the device, and click on Monitor. Now touch the touch sensor again - the data format being sent is of the form *{"VoteCount":1,"TimeFlag":"2016-11-09T20:22:53.845Z"}*

18.  We'll now analyze this data real-time in the cloud, by using a Stream Analytics job and Power BI dashboards. Follow along.


## Workshop #2

##### Create Stream Analytics jobs
1. Go to portal.azure.com
2. Click + sign, search for Stream Analytics job, click on Create. Give it a name "iotnext-sa", select Same region and the same resource group as that of your IOT Hub.
3. Click on iotnext-sa, click on "Inputs" and add a new input. Give an input alias name like "input1", select option "Data Stream" , Source as "IoT Hub", use IoT Hub from the current subscription, and choose the same IoT Hub you had created earlier. Endpoint: Messaging. Shared access policy name: iothubowner. Event serialization format: JSON.

4. Click on "Outputs" and add a new output. Give an output alias name "outputpbi", Sink: Power BI , Authorize Power BI if you have an account, else signup and authorize yourself. 
        Table name - iotnext-table
        Dataset name - iotnext-dataset
5. Click on "Query". Copy Paste this query in the box given

       `
       SELECT VoteCount INTO outputpbi FROM input1 
       `
        
6. Go back to your Stream Analytics job and click on "Start"; it may take sometime.
                     
#### Creating PowerBI report

1. Go to [PowerBI.com] (http://www.powerbi.com)
2. A dataset by the name iotnext-dataset should appear on the left bottom, under the 'Datasets'- click on it.
3. From right side toolbox, select votecount and select the Gauge chart in Visualizations.
4. Click on Pin visual, give a name to your Report.
5. Then select the name of Dashboard you want it to be pinned to, or Create a new Dashboard, and it'll get pinned to the same.
6. Go to the Dashboards tab in the Left menu and open the Dashboard you have just created.
7. Now touch the sensor - and the value should update in the Power BI within a few seconds. You'll be able to see real-time data from the sensor getting analyzed on the cloud!

*Congratulations! You have completed this workshop.*       

### Credits

For NodeJs Workshop, the code uses [this NPM module](https://github.com/rakeshpai/pi-gpio) for GPIO read and write.
