var gpio = require("pi-gpio");
var Protocol = require('azure-iot-device-http').Http;
var Client = require('azure-iot-device').Client;
var Message = require('azure-iot-device').Message;

var connectionString = 'Your device connection string goes here';
var client = Client.fromConnectionString(connectionString, Protocol);

var connectCallback = function (err) {
  if (err) {
    console.error('Could not connect: ' + err.message);
  } else {
    console.log('Client connected');

/*    gpio.setDirection(7, "output", function(err,value){
      if(err) throw err;
      console.log('Pin 7 set to output successful');
    });

    gpio.write(7,0, function(err, value){
     if(err) throw err;
    });*/

    setInterval(function() {
    gpio.read(3, function(err, value) {
        if(err) throw err;

        if(value==1)
        {
        console.log("You have registered your vote!"); // The current state of the pin
      	
        /*gpio.write(7,1, function(err, value){
         if(err) throw err;
        });*/
        value=0;

        var data = JSON.stringify({
             VoteCount:1,
             TimeFlag:new Date()
          });   
        var message = new Message(data);
        console.log('Sending message back to the IoT Hub: ' + message.getData());
        client.sendEvent(message, printResultFor('send'));    
        }

        else
       {
        console.log(".....");
        /*gpio.write(7,0, function(err, value){
        if(err) throw err;
        });*/
       }
    });
    }, 1000)
    }};

client.open(connectCallback);

// Helper function to print results in the console
function printResultFor(op) {
  return function printResult(err, res) {
    if (err) console.log(op + ' error: ' + err.toString() + "----");
    if (res) console.log(op + ' status: ' + res.constructor.name + "----");
  };
}
