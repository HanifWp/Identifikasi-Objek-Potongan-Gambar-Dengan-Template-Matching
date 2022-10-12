var loadFile = function(event) {
	var image = document.getElementById('output');
	image.src = URL.createObjectURL(event.target.files[0]);
};

var loadFile2 = function(event) {
	var image = document.getElementById('output2');
	image.src = URL.createObjectURL(event.target.files[0]);
};