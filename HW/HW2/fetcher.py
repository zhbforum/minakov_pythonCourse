import requests
import csv
import os
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, FrozenSet
from config import HEADERS, BASE_URL, GENRE_URL
from copy import deepcopy


class MovieFetcher:
    def __init__(self, pages: int):
        self.pages = pages
        self.headers = HEADERS
        self.base_url = BASE_URL
        self.genre_url = GENRE_URL
        self.movies = []
        self.genres = {}
        self._initial_data = []

    def fetch_data(self):
        genre_response = requests.get(GENRE_URL, headers=HEADERS)
        self.genres = {genre['id']: genre['name']
                       for genre in genre_response.json()['genres']}

        for page in range(1, self.pages + 1):
            url = f"{BASE_URL}?include_adult=false&include_video=false&sort_by=popularity.desc&page={page}"
            response = requests.get(url, headers=HEADERS)
            if response.ok:
                self.movies.extend(response.json().get("results", []))
        self._initial_data = deepcopy(self.movies)

    def get_all_data(self) -> List[Dict]:
        return self.movies

    def get_indexed_data(self) -> List[Dict]:
        return self.movies[3:20:4]

    def most_popular_title(self) -> str:
        if not self.movies:
            return "No movies found."
        return max(self.movies, key=lambda x: x.get("popularity", 0)).get("title", "")
    
    def search_by_keywords(self, *keywords: List[str]) -> List[str]:
        return [
            movie.get("title", "")
            for movie in self.movies
            if any(kw.lower() in movie.get("overview", "").lower() for kw in keywords)
        ]

    def unique_genres(self) -> FrozenSet[str]:
        return frozenset(
            self.genres[gid]
            for movie in self.movies
            for gid in movie.get("genre_ids", [])
            if gid in self.genres
        )

    def delete_by_genre(self, genre_name: str) -> None:
        target_ids = {
            gid for gid, name in self.genres.items()
            if name.lower() == genre_name.lower()
        }
        self.movies = [
            m for m in self.movies
            if not any(gid in target_ids for gid in m.get("genre_ids", []))
        ]
    
    def most_popular_genres(self) -> Dict[str, int]:
        counter = Counter(
            self.genres.get(gid)
            for movie in self.movies
            for gid in movie.get("genre_ids", [])
            if gid in self.genres
        )
        return counter.most_common()

    def group_titles_by_genres(self) -> FrozenSet[Tuple[str, str]]:
        genre_to_titles = defaultdict(list)

        for movie in self.movies:
            for gid in movie.get("genre_ids", []):
                genre_to_titles[gid].append(movie["title"])
        result = set()

        for titles in genre_to_titles.values():
            for i in range(0, len(titles) - 1, 2):
                result.add((titles[i], titles[i + 1]))
                
        return frozenset(result)

    def get_original_and_modified_data(self) -> Tuple[List[Dict], List[Dict]]:
        copy_data = deepcopy(self._initial_data)
        for movie in copy_data:
            if "genre_ids" in movie and movie["genre_ids"]:
                movie["genre_ids"][0] = 22
        return self._initial_data, copy_data

    def processed_movie_data(self) -> List[Dict]:
        result = []
        for movie in self._initial_data:
            try:
                release = datetime.strptime(movie.get("release_date", ""), "%Y-%m-%d")
                last_day = release + timedelta(weeks=10)
            except (ValueError, TypeError):
                last_day = None
                
            result.append({
                "title": movie.get("title", ""),
                "popularity": round(movie.get("popularity", 0), 1),
                "score": int(movie.get("vote_average", 0)),
                "last_day_in_cinema": last_day.strftime("%d-%m-%Y") if last_day else "Unknown",
            })
           
        return sorted(result, key=lambda x: (-x["score"], -x["popularity"]))

    def csv_export(self, path: str):
        data = self.processed_movie_data()

        dir_path = os.path.dirname(path) 
        if dir_path: 
            os.makedirs(dir_path, exist_ok=True) 

        with open(path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["title", "popularity",
                            "score", "last_day_in_cinema"]
            )
            writer.writeheader()
            writer.writerows(data)
