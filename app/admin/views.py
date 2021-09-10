from app.user.decorators import admin_required
from flask import Blueprint, render_template

blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@blueprint.route('/admin')
@admin_required
def admin_index():
    title = 'Control Panel'
    return render_template('admin/index.html', page_title=title)
