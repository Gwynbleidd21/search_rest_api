from numpy import zeros
import unidecode


def levenshtein_distance(s, de):
    # Funkcia pre výpočet  Levenštejnovej vzdialenosti (alebo editačnej vzdialenosti)
    # pre zistenie rozdielov medzi dvoma string-ami
    n = len(s)
    m = len(de)
    d = zeros([m, n])

    for i in range(1, m):
        d[i, 0] = i

    for j in range(1, n):
        d[0, j] = j

    for j in range(1, n):
        for i in range(1, m):
            if s[j - 1] == de[i - 1]:
                substitution_cost = 0
            else:
                substitution_cost = 1
            d[i, j] = min(d[i - 1, j] + 1,
                          d[i, j - 1] + 1,
                          d[i - 1, j - 1] + substitution_cost)
    return d[m-1, n-1]


def find_all(street_names, data):
    # Vo finálnej verzii nepoužitá funkcia
    to_find = data['searched']
    item = {
        "street": {
            "name": "sad",
            "token": "w"
        }
    }
    items = []
    possible_streets = []

    for street_name in street_names:
        universal_street = street_name.upper().replace(" ", "")
        universal_street = unidecode.unidecode(universal_street)
        universal_demanded = to_find.upper().replace(" ", "")
        universal_demanded = unidecode.unidecode(universal_demanded)

        if universal_street.find(universal_demanded) != -1 \
                and street_name.replace(" ", "") not in possible_streets:
            probability = len(to_find.replace(" ", "")) / len(street_name.replace(" ", "")) * 100
            items.append({
                "name": street_name,
                "token": "{:.0f} %".format(probability)
            }, )
            possible_streets.append(street_name)

    item['street'] = items
    return item


def find_one(street_names, data):
    # Vo finálnej verzii nepoužitá funkcia
    last_one = {
        "street": {
            "name": "sad",
            "token": "w"
        }
    }
    result = []
    possible_streets = []
    to_find = data['searched']
    chosen_one = 0
    for street_name in street_names:
        universal_street = street_name.upper().replace(" ", "")
        universal_street = unidecode.unidecode(universal_street)
        universal_demanded = to_find.upper().replace(" ", "")
        universal_demanded = unidecode.unidecode(universal_demanded)

        if universal_street.find(universal_demanded) != -1 \
                and street_name.replace(" ", "") not in possible_streets:
            probability = len(to_find.replace(" ", "")) / len(street_name.replace(" ", "")) * 100

            if probability > chosen_one:
                chosen_one = probability
                result = ({
                    "name": street_name,
                    "token": "{:.0f} %".format(probability)
                }, )
            possible_streets.append(street_name)

    last_one['street'] = result

    if len(result) < 1:
        minimum = 1000
        for street in street_names:
            difference = levenshtein_distance(street, to_find)
            if difference < minimum:
                minimum = difference
                result = ({
                              "name": street,
                              "token": "{:.0f} %".format((10 - difference) * 10)
                          },)

    last_one['street'] = result
    return last_one


def helping(to_compare, desired, chosen_one):
    # Pomocná funkcia na zistenie či sa vstup nenachádza v druhom vstupe
    # bez interpunkčných znamienok a za podmienok, že sú obe malými pismenami
    it_was = False
    universal_street = to_compare.upper().replace(" ", "")
    universal_street = unidecode.unidecode(universal_street)
    universal_demanded = desired.upper().replace(" ", "")
    universal_demanded = unidecode.unidecode(universal_demanded)

    if universal_street.find(universal_demanded) != -1:
        probability = len(desired.replace(" ", "")) / len(to_compare.replace(" ", "")) * 100

        if probability > chosen_one:
            chosen_one = probability
            it_was = True
    return chosen_one, it_was


def analyze(street, input_parts, street_parts):
    # Funkcia na zaistenie logiky,
    # že po zadaní slov oddelených n-počtom medzier (n + 1 slov),
    # bude tieto slová porovnávať s ulicami, ktorých slová sú na zodpovedajúcich pozíciách
    pom = 0
    can_it = False
    if len(street.split(" ")) > 1:
        if len(input_parts) > 1 and len(input_parts) == len(street_parts):
            for i in range(0, len(input_parts)):
                if len(input_parts[i]) > 0 and len(street_parts[i]) > 0:
                    if input_parts[i][0].lower() != street_parts[i][0].lower():
                        pom += 1
            if pom > 0:
                can_it = False
            elif pom == 0:
                can_it = True
    elif len(input_parts) == 1:
        if input_parts[0][0].lower() == street_parts[0][0].lower():
            can_it = True
        else:
            can_it = False

    return can_it


def find_street(street_names, data):
    last_one = {
        "street": {
            "name": "sad",
            "token": "w"
        }
    }
    minimum, chosen_one, to_find_two = 1000, 0, ""
    result, more_words = [], []

    to_find = data['searched']
    # Funkcionalita pre opravu možných chybných reťazcov načítaných z Excelu
    if len(to_find.split(" ")) > 1:
        more_words = to_find.split(" ")
        for word in more_words:
            if len(word) == 0:
                more_words.remove(word)
        to_find_two = ''.join([more_words[i] + " " if i < len(more_words) - 1 else
                               more_words[i] for i in range(len(more_words))])
    else:
        more_words = [to_find]
    if len(to_find_two) > 0:
        to_find = to_find_two

    for street in street_names:
        street_parts = street.split(" ")
        pom_street = street
        # Funkcionalita pre opravu možných chybných reťazcov načítaných z Excelu
        for part in street_parts:
            if len(part) == 0:
                pom_street = street.replace(" ", "")
        street_parts = pom_street.split(" ")

        can_it = analyze(street, more_words, street_parts)

        if can_it and len(to_find.split(" ")[0]) >= 3 and len(to_find.split(" ")) == 1:
            chosen_one, it_was = helping(street, to_find, chosen_one)

            if it_was:
                result = ({
                          "name": street,
                          "token": "{:.0f} %".format(chosen_one)
                          },)
        if can_it and len(street.split(" ")) == len(to_find.split(" ")):
            difference = levenshtein_distance(street, unidecode.unidecode(to_find))
            if minimum > difference > chosen_one:
                minimum = difference
                if ((len(street) - difference)/len(street)) * 100 < 0:
                    token = 'low'
                else:
                    token = "{:.0f} %".format(((len(street) - difference)/len(street)) * 100)
                result = ({
                              "name": street,
                              "token": token
                          },)

    last_one['street'] = result

    return last_one
