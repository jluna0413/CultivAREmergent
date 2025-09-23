from cultivar_app import create_app
import re

app = create_app()

with app.test_client() as client:
    resp = client.get('/')
    csp = resp.headers.get('Content-Security-Policy')
    print('CSP header:')
    print(csp)

    # Try to extract nonce from CSP header
    nonce_match = None
    if csp:
        # look for nonce-<value> in style-src or script-src using regex for 'nonce-...'
        m = re.search(r"nonce-([A-Za-z0-9+/=-]{8,})", csp)
        if m:
            nonce_match = m.group(1)
            print('Found nonce in CSP header (nonce-...):', nonce_match)
        else:
            # sometimes CSP uses "'nonce-value'" tokens
            m2 = re.search(r"'nonce-([A-Za-z0-9+/=-]{8,})'", csp)
            if m2:
                nonce_match = m2.group(1)
                print('Found nonce in CSP header (\'nonce-...\'):', nonce_match)

    data = resp.get_data(as_text=True)
    # check for script tag with nonce and window.cspNonce assignment
    script_nonce = None
    m3 = re.search(r"<script[^>]*nonce=[\"']([^\"']+)[\"'][^>]*>\s*\n?\s*window.cspNonce\s*=\s*'([^']*)'", data)
    if m3:
        script_nonce = m3.group(1)
        window_nonce = m3.group(2)
        print('Found <script nonce=...> with window.cspNonce value:', script_nonce, window_nonce)
    else:
        print('No script nonce or window.cspNonce assignment found in rendered HTML')

    # check for generated <style nonce=...> or theme-manager.js created ones aren't in server-rendered HTML, but ensure template injection worked
    print('\nLength of response HTML:', len(data))
    # For debugging, optionally print the head
    head = data.split('<head',1)[-1].split('</head>',1)[0]
    print('\n---- head snippet ----')
    print(head[:800])
    print('---- end head snippet ----')

print('Debug script completed')
