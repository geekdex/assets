import os
import urllib.parse

def get_title(name):
    """Converts filename/dirname to a pretty title."""
    name = os.path.splitext(name)[0]  # Remove extension
    name = name.replace('_', ' ').replace('-', ' ')
    # If it starts with numbers like 01.Name, remove the number part for display
    parts = name.split('.', 1)
    if len(parts) > 1 and parts[0].isdigit():
        return parts[1].strip()
    return name

def generate_gallery():
    root_dir = os.getcwd()
    subdirs = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d)) and not d.startswith('.')]
    subdirs.sort()

    categories = []
    
    # Process each subdirectory
    for subdir in subdirs:
        subdir_path = os.path.join(root_dir, subdir)
        images = [f for f in os.listdir(subdir_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
        images.sort()

        if not images:
            continue

        categories.append({
            'dir': subdir,
            'title': subdir.capitalize(),
            'count': len(images)
        })

        # Generate index.html for the subdirectory
        generate_category_html(subdir, images)

    # Generate root index.html
    generate_root_html(categories)
    print("Gallery generation complete!")

def generate_root_html(categories):
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Photo Gallery</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f0f2f5;
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }}
        header {{
            background-color: #fff;
            width: 100%;
            padding: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
            margin-bottom: 40px;
        }}
        h1 {{
            margin: 0;
            font-weight: 300;
        }}
        .container {{
            display: flex;
            gap: 30px;
            justify-content: center;
            flex-wrap: wrap;
            max-width: 800px;
            width: 100%;
            padding: 20px;
        }}
        .card {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow: hidden;
            width: 300px;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            text-decoration: none;
            color: inherit;
        }}
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 15px rgba(0,0,0,0.1);
        }}
        .card-content {{
            padding: 40px 20px;
        }}
        .card h2 {{
            margin: 0;
            font-size: 24px;
            color: #007bff;
        }}
        .card p {{
            color: #666;
            margin-top: 10px;
        }}
        .icon {{
            font-size: 48px;
            margin-bottom: 20px;
            display: block;
        }}
    </style>
</head>
<body>
    <header>
        <h1>My Photo Gallery</h1>
    </header>
    <div class="container">
"""
    
    for category in categories:
        html_content += f"""
        <a href="{category['dir']}/index.html" class="card">
            <div class="card-content">
                <span class="icon">📁</span>
                <h2>{category['title']}</h2>
                <p>{category['count']} photos</p>
            </div>
        </a>
"""

    html_content += """
    </div>
</body>
</html>
"""
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated index.html with {len(categories)} categories.")

def generate_category_html(subdir, images):
    title = subdir.capitalize()
    
    image_cards = ""
    for img in images:
        caption = get_title(img)
        img_url = urllib.parse.quote(img)
        image_cards += f"""
        <div class="photo-card">
            <img src="{img_url}" alt="{caption}" loading="lazy">
            <div class="caption">{caption}</div>
        </div>"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Photo Gallery</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8f9fa;
            margin: 0;
            padding: 0;
            color: #333;
        }}
        header {{
            background-color: #fff;
            padding: 20px 40px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .back-link {{
            text-decoration: none;
            color: #007bff;
            font-weight: 500;
        }}
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            padding: 40px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .photo-card {{
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: transform 0.2s;
            cursor: pointer;
        }}
        .photo-card:hover {{
            transform: scale(1.02);
            box-shadow: 0 5px 15px rgba(0,0,0,0.15);
        }}
        .photo-card img {{
            width: 100%;
            height: 200px;
            object-fit: cover;
            display: block;
        }}
        .caption {{
            padding: 15px;
            text-align: center;
            font-size: 14px;
            color: #555;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        /* Lightbox CSS */
        .lightbox {{
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.9);
            justify-content: center;
            align-items: center;
        }}
        .lightbox-content {{
            margin: auto;
            display: block;
            max-width: 90%;
            max-height: 90vh;
            border-radius: 5px;
            box-shadow: 0 0 20px rgba(255,255,255,0.2);
            transition: transform 0.1s ease-out;
            cursor: grab;
            transform-origin: center center;
        }}
        .lightbox-content:active {{
            cursor: grabbing;
        }}
        .close {{
            position: absolute;
            top: 15px;
            right: 35px;
            color: #f1f1f1;
            font-size: 40px;
            font-weight: bold;
            transition: 0.3s;
            cursor: pointer;
            z-index: 1001;
        }}
        .close:hover,
        .close:focus {{
            color: #bbb;
            text-decoration: none;
            cursor: pointer;
        }}
    </style>
</head>
<body>
    <header>
        <h1>{title}</h1>
        <a href="../index.html" class="back-link">← Back to Gallery</a>
    </header>
    <div class="gallery">
{image_cards}
    </div>

    <div id="lightbox" class="lightbox">
        <span class="close">&times;</span>
        <img class="lightbox-content" id="lightbox-img">
    </div>

    <script>
        const lightbox = document.getElementById('lightbox');
        const lightboxImg = document.getElementById('lightbox-img');
        const closeBtn = document.querySelector('.close');
        const cards = document.querySelectorAll('.photo-card');

        // Zoom and Pan variables
        let scale = 1;
        let isDragging = false;
        let startX = 0, startY = 0;
        let translateX = 0, translateY = 0;

        function resetZoom() {{
            scale = 1;
            translateX = 0;
            translateY = 0;
            updateTransform();
        }}

        function updateTransform() {{
            lightboxImg.style.transform = `translate(${{translateX}}px, ${{translateY}}px) scale(${{scale}})`;
        }}

        cards.forEach(card => {{
            card.addEventListener('click', (e) => {{
                e.preventDefault();
                const img = card.querySelector('img');
                lightbox.style.display = 'flex';
                lightboxImg.src = img.src;
                resetZoom();
            }});
        }});

        closeBtn.addEventListener('click', () => {{
            lightbox.style.display = 'none';
        }});

        lightbox.addEventListener('click', (e) => {{
            if (e.target === lightbox) {{
                lightbox.style.display = 'none';
            }}
        }});

        // Wheel Zoom
        lightbox.addEventListener('wheel', (e) => {{
            e.preventDefault();
            const delta = e.deltaY * -0.001;
            const newScale = Math.min(Math.max(0.5, scale + delta), 5);
            scale = newScale;
            updateTransform();
        }});

        // Drag Pan
        lightboxImg.addEventListener('mousedown', (e) => {{
            isDragging = true;
            startX = e.clientX - translateX;
            startY = e.clientY - translateY;
            lightboxImg.style.cursor = 'grabbing';
            e.preventDefault();
        }});

        window.addEventListener('mousemove', (e) => {{
            if (!isDragging) return;
            e.preventDefault();
            translateX = e.clientX - startX;
            translateY = e.clientY - startY;
            updateTransform();
        }});

        window.addEventListener('mouseup', () => {{
            if (isDragging) {{
                isDragging = false;
                lightboxImg.style.cursor = 'grab';
            }}
        }});
    </script>
</body>
</html>
"""
    output_path = os.path.join(subdir, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated {output_path} with {len(images)} images.")

if __name__ == "__main__":
    generate_gallery()
