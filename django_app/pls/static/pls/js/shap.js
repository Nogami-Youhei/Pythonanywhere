document.addEventListener('DOMContentLoaded', function() {
	let btn = document.getElementById('btn');
	btn.addEventListener('click', function() {
		document.getElementById('message').classList.add('start')
		document.getElementById('message').innerHTML = '計算を開始しますしばらくお待ちください...'
	}, false);
}, false);

$('form').submit(function(event){
	event.preventDefault();
	var form = $(this);
	$.ajax({
		url: form.prop('action'),
		method: form.prop('method'),
		data: form.serialize(),
	})
	.done(function(data){
		if (data.trim()[0] === '<') {
			console.log('result')
			$('#shap_result').html(data);
			$('#message').empty();
		} else if (data === '0') {
			console.log('error1')
			$('#message').removeClass('start');
			$('#message').text('入力値が不正です。入力データ数、特徴量の数は適切ですか？');
		} else if (data === '1') {
			console.log('error2')
			$('#message').removeClass('start');
			$('#message').text('サンプル行番号の指定は適切ですか？');
		} else {
			$('#message').removeClass('start');
			$('#message').text(data);
		}
	})
	.fail((jqXHR, textStatus, errorThrown) => {
		alert('Ajax通信に失敗しました。');
		console.log("jqXHR          : " + jqXHR.status); // HTTPステータスを表示
		console.log("textStatus     : " + textStatus);    // タイムアウト、パースエラーなどのエラー情報を表示
		console.log("errorThrown    : " + errorThrown.message); // 例外情報を表示
	});
});