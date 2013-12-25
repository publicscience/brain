from flask import Blueprint, render_template, redirect, request, url_for, jsonify, flash
from flask.views import MethodView
from flask.ext.mongoengine.wtf import model_form
from app import app, brain
from app.models import Muse, Tweet, Config, Doc
from app.auth import requires_auth

# Logging
from app.logger import logger
logger = logger(__name__)

# Landing page
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/generate')
def generate():
    return render_template('generate.html', speech=brain.MKV.generate())

@app.route('/status')
def status():
    return render_template('status.html', tweets=Tweet.objects.count(), docs=Doc.objects.count(), muses=Muse.objects.count())

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

def register_api(view, endpoint, url, id='id', id_type='int'):
    """
    Covenience function for building APIs.
    """
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={id: None}, view_func=view_func, methods=['GET'])
    app.add_url_rule(url, view_func=view_func, methods=['POST'])
    app.add_url_rule('%s<%s:%s>' % (url, id_type, id), view_func=view_func, methods=['GET', 'PUT', 'DELETE'])


class MuseAPI(MethodView):
    form = model_form(Muse, exclude=['created_at'])

    def get_context(self, username):
        muse = Muse.objects.get_or_404(username=username)
        form = self.form(request.form)

        context = {
                'muse': muse,
                'form': form
        }
        return context

    @requires_auth
    def get(self, username):
        # List view
        if username is None:
            muses = Muse.objects.all()
            form = self.form(request.form)
            return render_template('muses/list.html', muses=muses, form=form)
        # Detail view
        else:
            context = self.get_context(username)
            return render_template('muses/detail.html', **context)

    def post(self):
        form = self.form(request.form)

        if form.validate():
            muse = Muse()
            form.populate_obj(muse)
            muse.save()
            return redirect(url_for('muse_api'))

        return redirect(url_for('muse_api'))

    def delete(self, username):
        context = self.get_context(username)
        muse = context.get('muse')

        # Fetch and clear out this user's tweets.
        tweets = Tweet.objects(username=username)
        for tweet in tweets:
            tweet.delete()

        muse.delete()

        return jsonify({'success':True})

register_api(MuseAPI, 'muse_api', '/muses/', id='username', id_type='string')


class ConfigAPI(MethodView):
    form = model_form(Config, exclude=['created_at'])

    @requires_auth
    def get(self):
        config = Config.objects[0]
        form = self.form(request.form, obj=config)
        return render_template('config/index.html', config=config, form=form)

    def post(self):
        config = Config.objects[0]
        form = self.form(request.form, obj=config)

        if form.validate():
            form.populate_obj(config)

            # Need to reload the brain.
            if form.ramble.data != brain.MKV.ramble or form.spasm.data != brain.MKV.spasm:
                logger.info('Brain config value changed!')
                brain.MKV.ramble = form.ramble.data
                brain.MKV.spasm = form.spasm.data

            # If the ngram size has changed,
            # the brain needs to be retrained.
            if form.ngram_size.data != brain.MKV.n:
                logger.info('Brain ngram size changed! Retraining...')
                brain.MKV.n = form.ngram_size.data
                brain.retrain()

            config.save()
            flash('I will change my ways.')
            return redirect(url_for('config_api'))

        return redirect(url_for('config_api'))
config_api = ConfigAPI.as_view('config_api')
app.add_url_rule('/config/', view_func=config_api, methods=['GET', 'POST'])


class DocAPI(MethodView):
    form = model_form(Doc, exclude=['created_at'])

    @requires_auth
    def get(self):
        form = self.form(request.form)
        return render_template('train.html', form=form)

    def post(self):
        form = self.form(request.form)

        if form.validate():
            doc = Doc()
            form.populate_obj(doc)
            doc.save()
            brain.MKV.train([form.body.data])
            flash('I\'m learning!')
            return redirect(url_for('doc_api'))

        return redirect(url_for('doc_api'))

doc_api = DocAPI.as_view('doc_api')
app.add_url_rule('/train/', view_func=doc_api, methods=['GET', 'POST'])


