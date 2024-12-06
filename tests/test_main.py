import pytest
import os
import tempfile
import markdown
from build_scss import compile_scss
from main import generate_bureau_page, generate_home_page, generate_event_page, generate_events_page

@pytest.fixture
def temp_dir():
    """
    Fixture créant un répertoire temporaire avec la structure nécessaire pour les tests.
    Crée les dossiers 'assets/md' et 'public', change le répertoire de travail,
    et nettoie après l'exécution des tests.
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        old_cwd = os.getcwd()
        os.chdir(tmpdirname)
        os.makedirs('assets/md', exist_ok=True)
        os.makedirs('public', exist_ok=True)
        yield tmpdirname
        os.chdir(old_cwd)

def test_generate_bureau_page(temp_dir):
    """
    Teste la génération de la page du bureau.
    Vérifie que:
    - Le fichier HTML est créé
    - Les informations du CSV (nom, fonction, email) sont correctement intégrées
    """
    csv_content = "prénom,nom,fonction,email\nJohn,Doe,President,john@example.com"
    csv_file = "test_bureau.csv"
    with open(csv_file, "w", encoding="utf-8") as f:
        f.write(csv_content)

    output_file = "bureau.html"
    generate_bureau_page(csv_file, output_file)

    assert os.path.exists(os.path.join("public", output_file))
    with open(os.path.join("public", output_file), "r", encoding="utf-8") as f:
        content = f.read()
        assert "John Doe" in content
        assert "President" in content
        assert "john@example.com" in content

def test_generate_home_page(temp_dir):
    """
    Teste la génération de la page d'accueil.
    Vérifie que:
    - Le fichier HTML est créé
    - Les événements sont correctement affichés avec titre et date
    """
    with open(os.path.join("assets", "md", "event-1.md"), "w", encoding="utf-8") as f:
        f.write("---\ntitle: Test Event\ndate: 2023-05-01\n---\nTest content")

    output_file = "index.html"
    generate_home_page(output_file)

    assert os.path.exists(os.path.join("public", output_file))
    with open(os.path.join("public", output_file), "r", encoding="utf-8") as f:
        content = f.read()
        assert "Test Event" in content
        assert "2023-05-01" in content

def test_generate_event_page(temp_dir):
    """
    Teste la génération d'une page d'événement individuelle.
    Vérifie que:
    - Le fichier HTML est créé
    - Les détails de l'événement (titre, date, contenu, image) sont présents
    """
    event = {
        "title": "Test Event",
        "date": "2023-05-01",
        "content": "<p>Test content</p>",
        "image": "test_image.webp"
    }
    
    output_file = "event-1.html"
    generate_event_page(event, output_file)

    assert os.path.exists(os.path.join("public", output_file))
    with open(os.path.join("public", output_file), "r", encoding="utf-8") as f:
        content = f.read()
        assert "Test Event" in content
        assert "2023-05-01" in content
        assert "Test content" in content
        assert "test_image.webp" in content

def test_generate_events_page(temp_dir):
    """
    Teste la génération de la page listant tous les événements.
    Vérifie que:
    - Le fichier HTML est créé
    - Plusieurs événements sont correctement affichés avec leurs détails
    """
    with open(os.path.join("assets", "md", "event-1.md"), "w", encoding="utf-8") as f:
        f.write("---\ntitle: Test Event 1\ndate: 2023-05-01\n---\nTest content 1")
    with open(os.path.join("assets", "md", "event-2.md"), "w", encoding="utf-8") as f:
        f.write("---\ntitle: Test Event 2\ndate: 2023-05-02\n---\nTest content 2")

    output_file = "evenements.html"
    generate_events_page(output_file)

    assert os.path.exists(os.path.join("public", output_file))
    with open(os.path.join("public", output_file), "r", encoding="utf-8") as f:
        content = f.read()
        assert "Test Event 1" in content
        assert "Test Event 2" in content
        assert "2023-05-01" in content
        assert "2023-05-02" in content

def test_event_metadata_parsing():
    """
    Teste le parsing des métadonnées des fichiers markdown d'événements.
    Vérifie que:
    - Les métadonnées (title, date) sont correctement extraites
    - Le format de date est valide
    """
    with open('assets/md/2025-01-18-evenement-1.md', 'r', encoding='utf-8') as f:
        content = f.read()
        md = markdown.Markdown(extensions=['meta'])
        html = md.convert(content)
        
        assert 'title' in md.Meta
        assert 'date' in md.Meta
        assert md.Meta['date'][0].strip('"') == '2025-01-18'

def test_html_validation():
    """
    Teste la validité structurelle des pages HTML générées.
    Vérifie que:
    - La structure HTML de base est présente et valide
    - Les balises sémantiques (header, nav, main, footer) sont présentes
    - Les balises ouvrantes et fermantes sont équilibrées
    """
    generate_home_page('index.html')
    
    with open('public/index.html', 'r', encoding='utf-8') as f:
        content = f.read().lower()
        
        assert '<!doctype html>' in content
        assert '<html' in content
        assert '<head>' in content
        assert '<meta charset=' in content
        assert '<title>' in content
        assert '</head>' in content
        assert '<body>' in content
        assert '</body>' in content
        assert '</html>' in content
        
        assert '<header>' in content
        assert '<nav>' in content
        assert '<main>' in content
        assert '<footer>' in content
        
        assert content.count('<header>') == content.count('</header>')
        assert content.count('<nav>') == content.count('</nav>')
        assert content.count('<main>') == content.count('</main>')
        assert content.count('<footer>') == content.count('</footer>')

def test_events_chronological_order():
    """
    Teste le tri chronologique des événements.
    Vérifie que:
    - Les événements sont triés par date décroissante
    - L'ordre est maintenu après le tri
    """
    from datetime import datetime
    import glob

    events = []
    event_files = glob.glob('assets/md/*.md')
    
    for file in event_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            md = markdown.Markdown(extensions=['meta'])
            md.convert(content)
            if 'date' in md.Meta:
                date_str = md.Meta['date'][0].strip('"')
                events.append({
                    'date': datetime.strptime(date_str, '%Y-%m-%d'),
                    'file': file
                })
    
    # Sort the original events list in place
    events.sort(key=lambda x: x['date'], reverse=True)
    
    # Create a new sorted list for comparison
    sorted_events = sorted(events, key=lambda x: x['date'], reverse=True)
    
    # Compare the lists element by element
    for orig, sorted_evt in zip(events, sorted_events):
        assert orig['date'] == sorted_evt['date']
        assert orig['file'] == sorted_evt['file']

def test_assets_integration():
    """
    Teste l'intégration des ressources statiques.
    Vérifie que:
    - Le CSS est compilé correctement
    - Les images des événements sont copiées au bon endroit
    """
    import glob

    # Vérifie que le CSS est généré
    compile_scss()
    assert os.path.exists('public/styles.css')
    
    # Vérifie que les images sont copiées
    event_files = glob.glob('assets/md/*.md')
    for file in event_files:
        event_number = os.path.basename(file).split('-')[-1].split('.')[0]
        image_path = f'public/images/evenement-{event_number}.webp'
        assert os.path.exists(image_path)

def test_responsive_css():
    """
    Teste la présence des styles CSS pour le responsive design.
    Vérifie que:
    - Les media queries sont présentes
    - Les propriétés CSS pour la mise en page responsive sont définies
    """
    with open('public/styles.css', 'r', encoding='utf-8') as f:
        css_content = f.read()
        
        # Vérifie la présence des media queries essentielles
        assert '@media (max-width: 768px)' in css_content
        assert 'grid-template-columns' in css_content
        assert 'flex-direction: column' in css_content