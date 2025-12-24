import shutil
import os

# MAPPING: Where does the IDE look? -> Where do we keep it?
RULE_MAP = {
    ".clinerules": ".maestro/identities/roo_code.md",       # Roo/Cline
    ".cursorrules": ".maestro/identities/cursor.md",        # Cursor
    ".windsurfrules": ".maestro/identities/windsurf.md",    # Windsurf
    ".github/copilot-instructions.md": ".maestro/identities/github_copilot.md"
}

def sync_rules():
    print("🔄 Syncing IDE Agent Rules...")
    for target, source in RULE_MAP.items():
        if os.path.exists(source):
            # Ensure target dir exists (for .github/)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            
            shutil.copy(source, target)
            print(f"   ✅ Synced {source} -> {target}")
        else:
            print(f"   ⚠️ Source missing: {source}")

if __name__ == "__main__":
    sync_rules()