import sys
import json
import csv

sys.path.append('../')

from ckan_clan import ckan_api

def download_set():
    api = ckan_api.CkanApi('')

    sets = api.list_datasets

    for idx, item in enumerate(sets):
        print('[' + str(idx) + '] ' + item)

    try:
        set_idx = int(input('choose a dataset to download:'))
    except ValueError:
        print("Not a number")

    set_name = sets[set_idx]

    csv_set = api.get_dataset(set_name)

    file = open(set_name + '.csv', 'w', newline='')
    csv_writer = csv.DictWriter(file, csv_set.fieldnames)

    csv_writer.writeheader()
    for row in csv_set:
       csv_writer.writerow(row)

    print('Downloaded ' + set_name + ' to ' + set_name + '.csv')

def count_sets():
    api = ckan_api.CkanApi('')

    count = api.count_datasets()
    print(count)

def main():

    commands = ['download data set from ckan', 'count published datasets on beta.ckan.org']

    for idx, cmd in enumerate(commands):
        print('[' + str(idx) + '] ' + cmd)
    try:
        cmd_idx = int(input('choose a command:'))
    except ValueError:
        print("Not a number")

    if cmd_idx == 0:
        download_set()
    if cmd_idx == 1:
        count_sets()


main()