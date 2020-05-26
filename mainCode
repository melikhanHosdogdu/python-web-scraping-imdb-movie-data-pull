

total_film_count = 9751

kalan = total_film_count % 250
liste_link_sayisi = (total_film_count - kalan ) / 250
 
#https://www.imdb.com/search/title/?title_type=feature&languages=en&view=simple&sort=num_votes,desc&count=250&start=1&ref_=adv_nxt
link_first_part = "https://www.imdb.com/search/title/?title_type=feature&languages=en&view=simple&sort=num_votes,desc&count=250&start="
link_secound_part = "&ref_=adv_nxt"
link_list_250 = []
count = 1
for sayi in range(int(liste_link_sayisi)):
    link_list_250.append(link_first_part + str(count) + link_secound_part)
    count +=250


sayac = 0
film_links = []
for name in link_list_250:
    r_250 = requests.get(name)
    soup_250 =  bs(r_250.content, 'html.parser')
    film_link = soup_250.find_all(class_="lister-item-header")
    print("Kalan : " +  str(len(link_list_250) - sayac) + " | İşlenen : " + str(sayac))
    sayac += 1
    for link in film_link:
        film_links.append(link.find("a").get("href"))

        
