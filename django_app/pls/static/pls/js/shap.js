document.addEventListener('DOMContentLoaded', function() {
	let btn = document.getElementById('btn');
	btn.addEventListener('click', function() {
		document.getElementById('message').classList.add('start')
		document.getElementById('message').innerHTML = '計算を開始しますしばらくお待ちください...'
	}, false);

}, false);