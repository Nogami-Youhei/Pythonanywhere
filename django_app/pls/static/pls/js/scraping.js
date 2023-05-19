document.addEventListener('DOMContentLoaded', function() {
	let btn = document.getElementById('btn');
	btn.addEventListener('click', function() {
		document.getElementById('message').innerHTML = 'ダウンロードを開始しました<br>しばらくお待ちください'
	}, false);
    const XHR = new XMLHttpRequest();
    XHR.onload
}, false);