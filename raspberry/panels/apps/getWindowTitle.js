//Requires installation of active-window
//Pomoću paketa acitve-window pokušavamo dohvatiti ime prozora koji je u fokusu

var monitor = require('active-window');

callback = (window) => {
	try {
		console.log(window.title);
	} catch (err) {
		console.log(err);
	}
}

monitor.getActiveWindow(callback)