import csv
import os
import markdown
import glob
import re
from datetime import datetime

def generate_bureau_page(csv_file, output_file):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        members = list(reader)

    html_content = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Membres du Bureau - Vivre aux lilas</title>
        <link rel="stylesheet" href="styles.css">
    </head>
    <body>
        <header>
            <h1>Vivre aux lilas</h1>
            <nav>
                <ul>
                    <li><a href="index.html">Accueil</a></li>
                    <li><a href="bureau.html">Membres du Bureau</a></li>
                    <li><a href="evenements.html">Événements</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <h2>Membres du Bureau</h2>
            <ul class="members-list">
    """

    for member in members:
        html_content += f"""
                <li>
                    <strong>{member['prénom']} {member['nom']}</strong>
                    <br>{member['fonction']}
                    <br><a href="mailto:{member['email']}">{member['email']}</a>
                </li>
        """

    html_content += """
            </ul>
        </main>
        <footer>
            <p>&copy; 2024 Vivre aux lilas. Tous droits réservés.</p>
        </footer>
    </body>
    </html>
    """

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)

def generate_home_page(output_file):
    news_files = glob.glob('*.md')
    news_list = []

    for file in news_files:
        # Skip the README file
        if file.lower() == 'readme.md':
            continue

        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            md = markdown.Markdown(extensions=['meta'])
            html = md.convert(content)
            
            title = md.Meta.get('title', [os.path.splitext(file)[0]])[0]
            date_str = md.Meta.get('date', [''])[0]
            summary = md.Meta.get('summary', [''])[0] if 'summary' in md.Meta else html[:200] + '...'
            
            # Extract event number from filename
            event_number = file.split('-')[-1].split('.')[0]
            # Create link using the same format as in generate_events_page
            link = f"evenement-{event_number}.html"
            
            # Try to parse the date, use a default if parsing fails
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                # If date parsing fails, use the file modification time as a fallback
                date = datetime.fromtimestamp(os.path.getmtime(file))
            
            news_list.append({
                'title': title,
                'date': date,
                'summary': summary,
                'link': link
            })

    news_list.sort(key=lambda x: x['date'], reverse=True)

    html_content = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Accueil - Vivre aux lilas</title>
        <link rel="stylesheet" href="styles.css">
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    </head>
    <body>
        <header>
            <h1>Vivre aux lilas</h1>
            <nav>
                <ul>
                    <li><a href="index.html">Accueil</a></li>
                    <li><a href="bureau.html">Membres du Bureau</a></li>
                    <li><a href="evenements.html">Événements</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <h2>Actualités</h2>
            <div class="news-grid">
    """

    for news in news_list:
        formatted_date = news['date'].strftime('%d %B %Y')
        html_content += f"""
                <article class="news-card">
                    <h3><a href="{news['link']}">{news['title']}</a></h3>
                    <p class="date">{formatted_date}</p>
                    <p class="summary">{news['summary']}</p>
                    <a href="{news['link']}" class="read-more">Lire la suite</a>
                </article>
        """

    html_content += """
            </div>
        </main>
        <footer>
            <p>&copy; 2024 Vivre aux lilas. Tous droits réservés.</p>
        </footer>
    </body>
    </html>
    """

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)

def generate_event_page(event, output_file):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{event['title']} - Vivre aux lilas</title>
        <link rel="stylesheet" href="styles.css">
    </head>
    <body>
        <header>
            <h1>Vivre aux lilas</h1>
            <nav>
                <ul>
                    <li><a href="index.html">Accueil</a></li>
                    <li><a href="bureau.html">Membres du Bureau</a></li>
                    <li><a href="evenements.html">Événements</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <article>
                <h2>{event['title']}</h2>
                <p class="date">{event['date']}</p>
                <img src="{event['image']}" alt="Illustration pour {event['title']}" class="event-image">
                {event['content']}
            </article>
        </main>
        <footer>
            <p>&copy; 2024 Vivre aux lilas. Tous droits réservés.</p>
        </footer>
    </body>
    </html>
    """

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)

def generate_events_page(output_file):
    event_files = glob.glob('*.md')
    events_list = []

    for file in event_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            md = markdown.Markdown(extensions=['meta'])
            html_content = md.convert(content)
            title = md.Meta.get('title', [os.path.splitext(file)[0]])[0]
            date = md.Meta.get('date', [''])[0]
            
            event_number = file.split('-')[-1].split('.')[0]
            image_file = f"evenement-{event_number}.webp"
            event_page = f"evenement-{event_number}.html"
            
            event = {
                'title': title,
                'date': date,
                'content': html_content,
                'image': image_file,
                'page': event_page
            }
            events_list.append(event)
            
            generate_event_page(event, event_page)

    events_list.sort(key=lambda x: x['date'], reverse=True)

    html_content = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Événements - Vivre aux lilas</title>
        <link rel="stylesheet" href="styles.css">
    </head
    <body>
        <header>
            <h1>Vivre aux lilas</h1>
            <nav>
                <ul>
                    <li><a href="index.html">Accueil</a></li>
                    <li><a href="bureau.html">Membres du Bureau</a></li>
                    <li><a href="evenements.html">Événements</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <h2>Événements</h2>
    """

    for event in events_list:
        html_content += f"""
            <article>
                <h3><a href="{event['page']}">{event['title']}</a></h3>
                <p class="date">{event['date']}</p>
                <img src="{event['image']}" alt="Illustration pour {event['title']}" class="event-image">
                <p>{event['content'][:200]}...</p>
                <a href="{event['page']}" class="read-more">Lire la suite</a>
            </article>
        """

    html_content += """
        </main>
        <footer>
            <p>&copy; 2024 Vivre aux lilas. Tous droits réservés.</p>
        </footer>
    </body>
    </html>
    """

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)

if __name__ == "__main__":
    csv_file = "membres-bureau-association.csv"
    bureau_output_file = "bureau.html"
    generate_bureau_page(csv_file, bureau_output_file)
    print(f"Page générée : {bureau_output_file}")

    home_output_file = "index.html"
    generate_home_page(home_output_file)
    print(f"Page générée : {home_output_file}")

    events_output_file = "evenements.html"
    generate_events_page(events_output_file)
    print(f"Page générée : {events_output_file}")
