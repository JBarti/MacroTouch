//Requires installation of active-window

var monitor = require('active-window');

callback = (window)=>{
	try{
		console.log(window.title);
	}catch(err){
		console.log(err);
}
}

monitor.getActiveWindow(callback)