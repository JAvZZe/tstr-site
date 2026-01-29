import os

SCRIPT_CONTENT = """  <script>function initApollo(){var n=Math.random().toString(36).substring(7),o=document.createElement("script");
  o.src="https://assets.apollo.io/micro/website-tracker/tracker.iife.js?nocache="+n,o.async=!0,o.defer=!0,
  o.onload=function(){window.trackingFunctions.onLoad({appId:"6979e8021ac917001927e9b2"})},
  document.head.appendChild(o)}initApollo();</script>"""

BASE_DIR = "/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/web/tstr-frontend/src/pages"

def inject_script(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if "initApollo" in content:
        print(f"Skipping {file_path}: already contains initApollo")
        return False

    if "</head>" not in content:
        # print(f"Skipping {file_path}: no </head> tag found")
        return False

    # Insert before </head>
    new_content = content.replace("</head>", SCRIPT_CONTENT + "\n</head>")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Injected script into {file_path}")
    return True

def main():
    modified_count = 0
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(".astro"):
                full_path = os.path.join(root, file)
                if inject_script(full_path):
                    modified_count += 1
    
    print(f"Total files modified: {modified_count}")

if __name__ == "__main__":
    main()
