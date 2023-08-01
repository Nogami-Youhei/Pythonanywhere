async function submitNew() {
	document.getElementById('message').classList.add('start')
	document.getElementById('message').innerHTML = '計算を開始しますしばらくお待ちください...'
	const form = document.getElementById('shap')
	
	const endPoint = document.getElementById('shap').action
    let apiRes = await fetch(endPoint, {
        method: 'POST',
        body: new FormData(form)
    });
	const res = await apiRes.text();

	if (res.trim()[0] === '<') {
		document.getElementById('shap_result').innerHTML = res;
		document.getElementById('message').innerHTML = ''
		
		let clear_btn = document.getElementById('clear_btn');
		clear_btn.addEventListener('click', submitClear)
	
	} else if (res === '0') {
		const message = document.getElementById('message')
		message.classList.remove('start');
		message.textContent = '入力値が不正です。入力データ数、特徴量の数は適切ですか？';
	} else if (res === '1') {
		const message = document.getElementById('message')
		message.classList.remove('start');
		message.textContent = 'サンプル行番号の指定は適切ですか？';
	} else {
		const message = document.getElementById('message')
		message.classList.remove('start');
		message.textContent = res;
	}
}

async function submitClear() {
	const form = document.getElementById('clear_shap')
	
	const endPoint = document.getElementById('clear_shap').action
    let apiRes = await fetch(endPoint, {
        method: 'POST',
        body: new FormData(form)
	});

	const res = await apiRes.text();
	if (res == '3') {
		document.getElementById('shap_result').innerHTML = '';
	}
}

document.addEventListener('DOMContentLoaded', function() {
	let btn = document.getElementById('btn');
	btn.addEventListener('click', submitNew)
}, false);