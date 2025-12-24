import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from cultivar_app import create_app
from app.models import db
from app.models.base_models import LeadMagnet

app = create_app()
with app.app_context():
    # Ensure static lead_magnets dir exists
    safe_dir = os.path.join(app.root_path, 'static', 'lead_magnets')
    os.makedirs(safe_dir, exist_ok=True)
    dummy_file = os.path.join(safe_dir, 'dummy.pdf')
    if not os.path.exists(dummy_file):
        with open(dummy_file, 'wb') as fh:
            fh.write(b'%PDF-1.4\n%Dummy PDF for testing\n')

    magnet = LeadMagnet.query.filter_by(name='test').first()
    if not magnet:
        magnet = LeadMagnet(name='test', file_path='dummy.pdf', download_count=0, is_active=True)
        db.session.add(magnet)
        db.session.commit()
        print('Added test lead magnet')
    else:
        print('Test lead magnet already exists')