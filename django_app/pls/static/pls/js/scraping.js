document.addEventListener('DOMContentLoaded', function() {
	let btn = document.getElementById('btn');
	btn.addEventListener('click', function() {
		document.getElementById('message2').classList.add('start')
		document.getElementById('message2').innerHTML = 'ダウンロードを開始します<br>しばらくお待ちください...'
	}, false);

}, false);