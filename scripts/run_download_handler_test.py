import os
import sys
import traceback

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from cultivar_app import create_app

app = create_app()

with app.app_context():
    from app.blueprints.marketing import download_lead_magnet
    magnet_name = 'test'
    email = 'invalid-email@example'
    path = f'/marketing/download/{magnet_name}?email={email}'
    try:
        with app.test_request_context(path):
            # call the view function directly
            result = download_lead_magnet(magnet_name)
            print('Handler returned:', type(result))
            try:
                # If it's a Response-like object, print status
                print('Result repr:', repr(result))
            except Exception:
                pass
    except Exception as e:
        print('Exception while running handler:')
        traceback.print_exc()
        # also dump any marketing_errors.log if present
        logpath = os.path.join(app.root_path, 'logs', 'marketing_errors.log')
        if os.path.exists(logpath):
            print('\n--- marketing_errors.log ---')
            print(open(logpath, 'r', encoding='utf-8').read())
        sys.exit(1)

print('Test finished')