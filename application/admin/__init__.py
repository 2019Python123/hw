from flask import Blueprint


admin_bp = Blueprint('admin_bp',__name__)


from . import views,forms,model_view
