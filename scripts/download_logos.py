
import requests
import os

manufacturers = {
    'athena_logo.png': 'athenaag.com',
    'gavita_logo.png': 'gavita.com',
    'canna_logo.png': 'canna.com',
    'biobizz_logo.png': 'biobizz.com',
    'gh_logo.png': 'generalhydroponics.com',
    'trolmaster_logo.png': 'trolmaster.com',
    'quest_logo.png': 'questclimate.com',
    'hlg_logo.png': 'horticulturelightinggroup.com'
}

save_dir = r"a:\dev\CultivAREmergant\flutter_app\assets\images\manufacturers"
os.makedirs(save_dir, exist_ok=True)

for filename, domain in manufacturers.items():
    filepath = os.path.join(save_dir, filename)
    if os.path.exists(filepath):
        print(f"Skipping {filename}, already exists.")
        continue
        
    url = f"https://logo.clearbit.com/{domain}"
    print(f"Fetching {url}...")
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(r.content)
            print(f"Successfully saved {filename}")
        else:
            print(f"Failed to fetch {filename} (Status: {r.status_code})")
    except Exception as e:
        print(f"Error fetching {filename}: {e}")
