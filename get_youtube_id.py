import requests

API_KEY = "API_KEY"  # Substitua pela sua chave de API
PLAYLIST_URL = "PLAYLIST_LINK" #Link da Playlist

# Extrair o ID da playlist do link
import urllib.parse as urlparse
from urllib.parse import parse_qs

parsed = urlparse.urlparse(PLAYLIST_URL)
playlist_id = parse_qs(parsed.query)["list"][0]

def get_video_ids_from_playlist(api_key, playlist_id):
    url = "https://www.googleapis.com/youtube/v3/playlistItems"
    video_ids = []
    params = {
        "part": "contentDetails",
        "playlistId": playlist_id,
        "maxResults": 50,
        "key": api_key
    }

    while True:
        response = requests.get(url, params=params)
        data = response.json()

        # Adiciona os IDs dos vídeos à lista
        for item in data["items"]:
            video_id = item["contentDetails"]["videoId"]
            video_ids.append(video_id)

        # Verifica se há mais páginas
        if "nextPageToken" in data:
            params["pageToken"] = data["nextPageToken"]
        else:
            break

    return video_ids

# Buscar os IDs
ids = get_video_ids_from_playlist(API_KEY, playlist_id)

# Mostrar no console
for i, vid in enumerate(ids, 1):
    print(f"{i}. {vid}")

# Opcional: salvar em um arquivo
with open("video_ids.txt", "w") as f:
    for vid in ids:
        f.write(f"{vid}\n")

print(f"\nTotal de vídeos encontrados: {len(ids)}")
print("Os links foram salvos em 'video_ids.txt'")
