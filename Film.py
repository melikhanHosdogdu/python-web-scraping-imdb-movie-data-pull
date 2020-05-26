class Film:
    film_link = str()
    title = str()
    year = str()
    imdb_rate =  float()
    rating_count = float()
    duration = int()
    genres = str()
    creator = str()
    writer = str()
    stars = str()
    storyline = str()
    #2h 2min
    
    def duration_casting(self, _duration):   # movie duration type is string that's why we are casting as a int
        self.duration = 0
        hour = list()
        for letter in _duration:
            try:
                hour.append(int(letter))
            except:
                continue
        if len(hour) == 2:
            self.duration += 60 * hour[0]
            self.duration += hour[1]
        elif len(hour) == 3:
            self.duration += 60 * hour[0]
            self.duration += 10 * hour[1]
            self.duration += hour[2]



total_film_count = 9751

kalan = total_film_count % 250
list_link_number = (total_film_count - kalan ) / 250
 
#https://www.imdb.com/search/title/?title_type=feature&languages=en&view=simple&sort=num_votes,desc&count=250&start=1&ref_=adv_nxt
link_first_part = "https://www.imdb.com/search/title/?title_type=feature&languages=en&view=simple&sort=num_votes,desc&count=250&start="
link_secound_part = "&ref_=adv_nxt"
link_list_250 = []
count = 1
for sayi in range(int(list_link_number)):
    link_list_250.append(link_first_part + str(count) + link_secound_part)
    count +=250
# we are creating film links 

counter = 0
film_links = []
for name in link_list_250:
    r_250 = requests.get(name)
    soup_250 =  bs(r_250.content, 'html.parser')
    film_link = soup_250.find_all(class_="lister-item-header")
    print("Remaining Action : " +  str(len(link_list_250) - counter) + " | Processed : " + str(counter))
    counter += 1
    for link in film_link:
        film_links.append(link.find("a").get("href"))


from google.colab import auth
auth.authenticate_user()

import gspread
from oauth2client.client import GoogleCredentials

gc = gspread.authorize(GoogleCredentials.get_application_default())

sh = gc.create('Imdb Film Datas')



import requests
from bs4 import BeautifulSoup as bs

print("="*20)
print(len(film_links))

film = Film()

counter_2 = 0

worksheet = gc.open('Imdb Film Datas5').sheet1

print(len(film_links))
for d_film in  film_links:

  film_info = list()

  film.film_link ="https://www.imdb.com" + d_film 
  r = requests.get(film.film_link)
  soup = bs(r.content, 'html.parser')
  title = soup.find("div", attrs = {"class": "title_wrapper"}).h1.text.split("(")
  film.title = title[0]
  film.year =  soup.find(id="titleYear").a.text  
  film.imdb_rate = float(soup.find("span", attrs = {"itemprop": "ratingValue"}).text)
  rating_count = soup.find("span", attrs = {"itemprop": "ratingCount"}).text
  film.rating_count = float(rating_count.replace(",", ""))
  duration = soup.find("div", attrs = {"class": "subtext"}).time.text.strip()
  film.duration_casting(duration)

  genres_link = soup.find("div", attrs = {"class": "subtext"}).find_all("a", limit = 3, title = "")
  film.genres = []
  for genre in genres_link:
    film.genres.append(genre.text)

  cast = soup.find_all(class_ =  "credit_summary_item")
  film.creator = cast[0].a.text  # the fist element is creator we are getting text of link (a)
  try:
    film.writer =cast[1].a.text # secound elemet inculude all stars link  as list 
  except:
    film.writer  = "|No Data|"
  try:
    stars_link =cast[2].find_all("a", limit = 2) # secound elemet inculude all stars link  as list 
    film.stars = []
    for star in stars_link:
      film.stars.append(star.text)  # we are getting text os stars
  except:
    film.stars = "|No Data|"

  
  try:
    storyline_list = (soup.find(class_ = "inline canwrap").text).strip().split("\n",1)
    film.storyline = storyline_list[0]
  except:
    continue

  film_info.append(film.title)
  film_info.append(film.year)
  film_info.append(film.imdb_rate)
  film_info.append(film.rating_count)
  film_info.append(film.duration)
  film_info.append(film.genres)
  film_info.append(film.creator)
  film_info.append(film.writer)
  film_info.append(film.stars)
  film_info.append(film.storyline)

  for num2 in range(0,10):
    if type(film_info[num2]) == list:
      worksheet.update_cell((counter_2 + 2), (num2 + 1), str(film_info[num2]) )
    else:
      worksheet.update_cell((counter_2 + 2), (num2 + 1), film_info[num2] )
  
  
  if counter_2 % 10 == 0:
    print("Remaining Action : "  +  str(len(film_links) - counter_2) + " | Processed : " + str(counter_2))
  counter_2 += 1
  

print("#"*50)

print("Finish")
