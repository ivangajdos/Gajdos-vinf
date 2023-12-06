
import os
import lucene

from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, TextField
from org.apache.lucene.index import IndexOptions, IndexWriter, IndexWriterConfig, DirectoryReader, Term
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import MMapDirectory
from org.apache.lucene.search import IndexSearcher


import csv



def load_csv_into_dictionary(file_path):
    data_dict = {}
    with open(file_path, 'r') as file:

        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            key = row.pop('id')
            data_dict[key] = row

    return data_dict

def create_doc(match):
    doc = Document()
    id = match[0]
    league = match[1]
    year = match[2]
    date = match[3]
    home = match[4]
    score = match[5]
    away = match[6]
    stadium = match[7]
    town_city = match[8]
    capacity = match[9]

    field_type = FieldType()
    field_type.setStored(True)
    field_type.setIndexOptions(IndexOptions.NONE)
    doc.add(Field("id", id, field_type))

    doc.add(Field("league", league, TextField.TYPE_NOT_STORED))
    doc.add(Field("season", year, TextField.TYPE_NOT_STORED))
    doc.add(Field("date", date, TextField.TYPE_NOT_STORED))
    doc.add(Field("home", home, TextField.TYPE_NOT_STORED))
    doc.add(Field("score", score, TextField.TYPE_NOT_STORED))
    doc.add(Field("away", away, TextField.TYPE_NOT_STORED))
    doc.add(Field("Stadium", stadium, TextField.TYPE_NOT_STORED))
    doc.add(Field("Town / City", town_city, TextField.TYPE_NOT_STORED))
    doc.add(Field("Capac", capacity, TextField.TYPE_NOT_STORED))

    return doc

def index(file_path):
    store = MMapDirectory(Paths.get('index'))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store,config)
    file = open(file_path, 'r', encoding='utf-8')
    csv_r = csv.reader(file)

    for row in csv_r:
        id,league,season,date,home,score,away,stadium,town_city,capacity = row
        doc = create_doc(row)
        writer.addDocument(doc)

    writer.commit()
    writer.close()

def simple_search_lucene(query_string):
    directory = MMapDirectory(Paths.get('index'))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer()
    query = QueryParser("home", analyzer).parse(query_string)
    return searcher.search(query, 2000000).scoreDocs, searcher

def complex_search_lucene(str1, str2,str3):
    directory = MMapDirectory(Paths.get('index'))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer()
    text = "your_search_text"
    if len(str3) < 1:
        special = "home:" + str1 + " AND away:" + str2
        default_field = "home"
    else:
        special = "league:" + str1 + " AND season:" + str2 + " AND date:" + str3
        default_field = "date"



    query_parser = QueryParser(default_field, analyzer)
    query = query_parser.parse(special)
    hits = searcher.search(query, 1000)
    return hits.scoreDocs,searcher

def print_results(results, searcher, all_matches, test):
    string = ''
    whole_data = ''
    for i in range(len(results)):


        if i > len(results):

            print(len(string) * '-')
            print(f'Number of matching documents in total: {i}/{len(results)}\n')
            print('You saw all matches!')
            return
        doc = searcher.doc(results[i].doc)
        match = all_matches[doc.get("id")]

        string = f'|{i + 1}| score: {results[i].score} | {i + 1}| league: {match["league"]} | season: {match["season"]} | ' \
                 f'date: {match["date"]} | home: {match["home"]} | score: {match["score"]} | away: {match["away"]} | ' \
                 f'stadium: {match["Stadium"]} | town / city: {match["Town / City"]} | capacity: {match["Capac"]}'
        whole_data += string
        if not test:
            print(string)


    return whole_data

def main():
    file_name = 'merged_output.csv'
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])

    index(file_name)
    all_matches = load_csv_into_dictionary(file_name)
    query = ""
    choice = ""


    while choice != "exit":
        choice = input("Enter your choice:\n 1 - Search by team\n 2 - Search by home and away team\n 3 - searh by league, season and date\n test - test if query is getting right data\n exit - end program\n")

        if(choice == "1"):
            query = input('Team you are searching for: ')
            results, searcher = simple_search_lucene(query)
            test = False
        if(choice == "2"):

            home = input('Enter home team: ')
            away = input('Enter away team: ')
            results, searcher = complex_search_lucene(home, away, "")
        if (choice == "3"):
            league = input('Enter league: ')
            season = input('Enter season: ')
            date = input('Enter date: ')
            results, searcher = complex_search_lucene(league, season, date)
        if (choice == "test"):
            test = True
            results, searcher = simple_search_lucene("Chelsea")
            data = print_results(results,searcher,all_matches,test)
            with open("results.txt", 'r') as file:
                data_from_txt_file = file.read()

            if data == data_from_txt_file:
                print("Data from query: " + data)
                print("Data expected:   " + data_from_txt_file)
                print("------------------------------")
                print("Test passed, data are the same!")
                print("------------------------------")
            else:
                print("Test Failed!")



        if len(results) >= 1 and choice != "exit":
            print_results(results, searcher, all_matches,test)
        else:
            print("No records found.")


main()