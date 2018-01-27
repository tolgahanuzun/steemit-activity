from flask import Flask, render_template, request
from functools import reduce
import steemit

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		url = request.form.get('link') or False
		handle = request.form.to_dict()
		handle.pop('link')
		handle = handle.keys()
		if not url or not handle:
			return render_template('index.html', data={'error':'Make a selection or enter a URL. Or both.'})
		if  not steemit.test_url(url):
			return render_template('index.html', data={'error':'I guess this is not the right link.'})

		filterd = {}
		if request.form.get('rt') or False:
			rt = set(steemit.post_resteem(url))
			filterd['rt'] = rt
		if request.form.get('comment') or False:
			comment = set(steemit.post_comment(url))
			filterd['comment'] = comment
		if request.form.get('follow') or False:
			follow = set(steemit.post_follow(url))
			filterd['follow'] = follow
		if request.form.get('upvote') or False:
			vote = set(steemit.post_vote(url))
			filterd['upvote'] = vote


		eval_list = [filterd[hand] for hand in handle]
		result = reduce(lambda x, y: set(x) & set(y), eval_list)
		results = {'result': [x for x in iter(result)], 'count': len(result)}
		return render_template('index.html', data=results)

	return render_template('index.html')


if __name__ == '__main__':
	app.debug = False
	app.secret_key = "123"
	app.run(host='0.0.0.0')
	