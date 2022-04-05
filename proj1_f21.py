#########################################
##### Name:  Yi Sun                     #####
##### Uniqname: freyasun                    #####
#########################################
import json
import requests
import webbrowser
class Media:

    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", json=None):
        if json is not None:
            try:
                self.title = json["trackName"]
            except KeyError:
                self.title = json["collectionName"]
            self.author = json["artistName"]
            self.release_year = json["releaseDate"].split("-")[0]
            try:
                self.url = json["trackViewUrl"]
            except KeyError:
                self.url = json["collectionViewUrl"]

        else:
            self.title = title
            self.author = author
            self.release_year = release_year
            self.url = url

        
    def info(self):
        return f"{self.title} by {self.author} ({self.release_year})"
    def length(self):
        return 0
class Song(Media):
    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", album="No Album", genre="No Genre", track_length=0, json=None):
        super().__init__(title, author, release_year, url, json)
        if json is not None:
            self.album = json["collectionName"]
            self.track_length = json["trackTimeMillis"]
            self.genre = json["primaryGenreName"]
            self.title = json["trackName"]
        else:
            self.album = album
            self.genre = genre
            self.track_length = track_length
    def info(self):
        return f"{super().info()} [{self.genre}]"
    def length(self):
        return int((int(self.track_length) / 1000))
class Movie(Media):
    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL",rating="No Rating", movie_length=0, json=None):
        super().__init__(title, author, release_year, url, json)
        if json is not None:
            self.rating = json["contentAdvisoryRating"]
            try:
                self.movie_length = json["trackTimeMillis"]
            except KeyError:
                pass
        else:
            self.rating = rating
            self.movie_length = movie_length
    def info(self):
        return f"{super().info()} [{self.rating}]"
    def length(self):
        return int(int(self.movie_length) / 60000)

#query: fetch the movie type using info() method from the itunes API
def get_movie(param):
    movies = []
    url = "https://itunes.apple.com/search?term="
    response = response = requests.get(url + param).json()
    for result in response['results']:
        if result['kind'] == 'feature-movie':
            movies.append(Movie(json=result).info())
    return movies



# functions for Q4

def overall_result(param):
    output={
        "SONGS":[],
        "MOVIES":[],
        "OTHER MEDIA":[]
    }
    url = "https://itunes.apple.com/search?term="
    response = response = requests.get(url + param).json()
    for result in response['results']:
        if "kind" in result.keys():
            if result["kind"] == 'song':
                output["SONGS"].append(Song(json=result))
            elif result["kind"] == 'feature-movie':
                output["MOVIES"].append(Movie(json=result))
            else:
                output["OTHER MEDIA"].append(Media(json=result))
    return output

def interactive(query):
    count = 1
    print("SONGS")
    if len(query["SONGS"]) == 0:
        print("No songs")
    else:
        for song in query["SONGS"]:
            print(f"{count} {song.info()}")
            count += 1

    print("MOVIES")
    if len(query["MOVIES"]) == 0:
        print("No movies")
    else:
        for movie in query["MOVIES"]:
            print(f"{count} {movie.info()}")
            count += 1

    print("OTHER MEDIA")
    if len(query["OTHER MEDIA"]) == 0:
        print("No other media")
    else:
        for media in query['OTHER MEDIA']:
            print(f"{count} {media.info()}")
            count += 1




if __name__ == "__main__":
    # your control code for Part 4 (interactive search) should go here
    term = input('Enter a search term, or "exit" to quit: ')
    if term == "exit":
        print("Bye!")
        exit()
    else:
        interactive(overall_result(term))
        overall = overall_result(term)['SONGS'] + overall_result(term)['MOVIES'] + overall_result(term)['OTHER MEDIA']
        while True:
            num = input('Enter a number for more info, or another search item, or exit: ')
            if num.isnumeric():
                if 1 <= int(num) <= len(overall):
                    print(f"Launching {overall[int(num)-1].url} in web browser...")
                    webbrowser.open(overall[int(num)-1].url)
            elif num == "exit":
                print("Bye!")
                break
            else:
                interactive(overall_result(num))


