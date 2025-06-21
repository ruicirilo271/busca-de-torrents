from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = 'https://testbay.onrender.com//api/v1/search'  # Ou a tua API URL real
TMDB_API_KEY = '516adf1e1567058f8ecbf30bf2eb9378'  # A tua chave TMDB

def get_poster_url(title):
    try:
        url = "https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "query": title
        }
        response = requests.get(url, params=params)
        data = response.json()
        if data.get('results'):
            poster_path = data['results'][0].get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w300{poster_path}"
    except:
        pass
    return "/static/default.jpg"  # fallback

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    searched = False
    if request.method == 'POST':
        searched = True
        query = request.form['query']
        data = {'search_term': query}  # CORRETO aqui!
        try:
            response = requests.post(API_URL, json=data)
            if response.ok:
                json_data = response.json()
                results = json_data.get('data', [])
                for item in results:
                    clean_title = item['name'].split('(')[0].strip()
                    item['poster'] = get_poster_url(clean_title)
        except Exception as e:
            print("Erro ao contactar API:", e)
    return render_template('index.html', results=results, searched=searched)

if __name__ == '__main__':
    app.run(debug=True)
