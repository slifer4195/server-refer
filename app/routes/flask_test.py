from sqlalchemy import inspect
from flask import Blueprint, render_template
from ..models import db


api_bp = Blueprint('api_test', __name__)

@api_bp.route("/db-inspect", methods=['GET'])
def db_inspect():
    print("test")
    inspector = inspect(db.engine)
    tables = {}
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        tables[table_name] = columns  # list of dicts with column info
    return render_template("db_inspect.html", tables=tables)