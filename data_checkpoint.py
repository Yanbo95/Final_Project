#################
########   Final Project
#Name: Yanbo Shi
#Uniqname: yanboshi
#################

from bs4 import BeautifulSoup
import requests
import json
import sqlite3



def build_state_url_dict():
    ''' Make a dictionary that maps state name to state page url from "https://www.collegesimply.com/colleges/"

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is a state name and value is the url
    '''
    state_dict = {}
    url = 'https://www.collegesimply.com/colleges/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    lis = soup.find('select', class_='custom-select')
    state_list = lis.find_all('option')

    for infor in state_list:
        state_dict[infor.text.lower()] = url + infor['value']
    
    return state_dict


def get_university_sites_url_and_html_and_cashing():
    url = 'https://www.collegesimply.com/'
    state_sites_dict = build_state_url_dict()
    for state_site in state_sites_dict.values():
        response = requests.get(state_site)
        soup = BeautifulSoup(response.text, 'html.parser')
        lis = soup.find('ol', class_='list-unstyled')
        univer_list = lis.find_all('h4')

        for univ in univer_list:
            univer_url = url + univ.find('a')['href']
            make_request_using_cache(univer_url,CACHE_DICT)

    return None


def create_database():

    conn = sqlite3.connect("final_project.sqlite")
    cur = conn.cursor()

    drop_Universities_in_states = '''
        DROP TABLE IF EXISTS "Universities_in_states";
    '''

    create_Universities_in_states = '''
        CREATE TABLE IF NOT EXISTS "Universities_in_states" (
            "Id"        INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            "UniversityName"  TEXT NOT NULL,
            "State"  TEXT NOT NULL,
            "NationalRank"    INTEGER
        );
    '''

    drop_University_details = '''
        DROP TABLE IF EXISTS 'University_details'
    '''

    create_University_details = '''
        CREATE TABLE 'University_details' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Name' TEXT NOT NULL,
        'StudentPopulation' INTEGER NOT NULL,
        'SchoolType' TEXT NOT NULL,
        'Size' TEXT NOT NULL,
        'Tuition' TEXT NOT NULL,
        'ApplicationAccepted' TEXT NOT NULL,
        'AverageSalaryAfterTenYears' TEXT NOT NULL,
        'BachelorDegreeGraduationRate' TEXT NOT NULL
        ); 
    '''


    cur.execute(drop_Universities_in_states)
    cur.execute(create_Universities_in_states)
    cur.execute(drop_University_details)
    cur.execute(create_University_details)

    conn.commit()

    return None






#--------------------------------------------------------------------------------------------
#Adding caching(Using some codes from class material)

CACHE_FILENAME = "final_proj.json"
CACHE_DICT = {}

def load_cache():
    ''' opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()


def make_request_using_cache(url,cache):
    ''' Check Whether the information is in the cache dictionary.
    ----------
    url: string
        The keys of the dictionary
    cache: dictionary
        A dictionary is used to store information
    Returns
    -------
    item
        The item of the dictionary.
    '''
    if (url in cache.keys()): 
        print("Using cache")
        return cache[url]
    else:
        print("Fetching")       
        response = requests.get(url)
        cache[url] = response.text
        save_cache(cache)
        return cache[url]

#--------------------------------------------------------------------------------------------




if __name__ == "__main__":

    #---------------------------caching
    CACHE_DICT = load_cache()
    #-----------------------------

    create_database()

    conn = sqlite3.connect("final_project.sqlite")
    cur = conn.cursor()


    insert_instructors = '''
        INSERT INTO Universities_in_states
        VALUES (NULL, 'The University of Alabama', 'Alabama', 169)
    '''

    insert_ins = '''
        INSERT INTO University_details
        VALUES (NULL, 'The University of Alabama', 38390, 'Public 4 Year','Large','$29230','59.1%','49900','66%')
    '''

    cur.execute(insert_instructors)
    cur.execute(insert_ins)
    conn.commit()

