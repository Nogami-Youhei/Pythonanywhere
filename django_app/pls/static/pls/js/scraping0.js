document.addEventListener('DOMContentLoaded', function() {
	let btn = document.getElementById('btn');
	btn.addEventListener('click', function() {
		document.getElementById('message').classList.add('start')
		document.getElementById('message').innerHTML = 'ダウンロードを開始します<br>しばらくお待ちください...'
	}, false);

}, false);