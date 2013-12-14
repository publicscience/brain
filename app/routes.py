from flask import Blueprint, render_template, redirect, request, url_for, jsonify
from flask.views import MethodView
from flask.ext.mongoengine.wtf import model_form
from app import app
from app.models import Mentor

# Landing page
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


def register_api(view, endpoint, url, id='id', id_type='int'):
    """
    Covenience function for building APIs.
    """
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={id: None}, view_func=view_func, methods=['GET'])
    app.add_url_rule(url, view_func=view_func, methods=['POST'])
    app.add_url_rule('%s<%s:%s>' % (url, id_type, id), view_func=view_func, methods=['GET', 'PUT', 'DELETE'])


class MentorAPI(MethodView):
    form = model_form(Mentor, exclude=['created_at'])

    def get_context(self, username):
        mentor = Mentor.objects.get_or_404(username=username)
        form = self.form(request.form)

        context = {
                'mentor': mentor,
                'form': form
        }
        return context

    def get(self, username):
        # List view
        if username is None:
            mentors = Mentor.objects.all()
            form = self.form(request.form)
            return render_template('mentors/list.html', mentors=mentors, form=form)
        # Detail view
        else:
            context = self.get_context(username)
            return render_template('mentors/detail.html', **context)

    def post(self):
        form = self.form(request.form)

        if form.validate():
            mentor = Mentor()
            form.populate_obj(mentor)
            mentor.save()
            return redirect(url_for('mentor_api'))

        return redirect(url_for('mentor_api'))

    def delete(self, username):
        context = self.get_context(username)
        mentor = context.get('mentor')
        mentor.delete()

        return jsonify({'success':True})

register_api(MentorAPI, 'mentor_api', '/mentors/', id='username', id_type='string')
