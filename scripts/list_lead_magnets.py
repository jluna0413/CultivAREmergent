import os
import sys

# Ensure repository root is on sys.path so we can import the app package
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from cultivar_app import create_app
from app.models import db
from app.models.base_models import LeadMagnet

app = create_app()
with app.app_context():
    magnets = LeadMagnet.query.all()
    if not magnets:
        print('No lead magnets found')
    for m in magnets:
        print(m.id, m.name, m.file_path, m.download_count)