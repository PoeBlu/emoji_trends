import csv
import datetime
import os
from downsample import downsample
from tqdm import tqdm

start_date = datetime.datetime(2013,1,1)
days_number = 2405
downsample_factor = 50
date_array = [start_date + datetime.timedelta(days=x) for x in range(days_number)]

base_path = '/media/enric/enric_hdd/datasets/emoji_trends'

def clean(folder_name):
    print('-----------------')
    print(f'Digesting: {folder_name}')

    print('Merging all CSV files in one...')
    os.system(
        f'cat {base_path}/emojis_raw/{folder_name}/* > {base_path}/clean_emojis/{folder_name}_unified.csv'
    )
    print('Removing headers...')
    remove = '"username","date","retweets","favorites","text","geo","mentions","hashtags","id","permalink","emoji"'
    os.system(
        f"awk '!/{remove}/' {base_path}/clean_emojis/{folder_name}_unified.csv > temp && mv temp {base_path}/clean_emojis/{folder_name}_no_header.csv"
    )

    date_dict = {date: 0 for date in date_array}
    print('Digesting...')
    with open(f'{base_path}/clean_emojis/{folder_name}_no_header.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in tqdm(csv_reader):
            try:
                datetime_object = datetime.datetime.strptime(row[1],'%Y-%m-%d %H:%M').replace(hour=0,minute=0)
                date_dict[datetime_object] += 1
            except:
                pass

    print('Deleting intermediate files...')
    os.system(f'rm {base_path}/clean_emojis/{folder_name}_unified.csv')
    print("Writing CSV...")
    with open(f'{base_path}/emojis_3600/{folder_name}.csv', mode='w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['day,usage'])
        for date in date_array:
            writer.writerow([date.strftime("%Y-%m-%d"), date_dict[date]])

    downsample(
        f'{base_path}/emojis_3600/{folder_name}.csv',
        f'{base_path}/emojis_50/{folder_name}.csv',
        downsample_factor,
    )

clean("football")
clean("bee")
clean("american_football")
clean("spain")
clean("catalonia")
clean("shooting_star")
clean("factory")
clean("pig")
clean("panda")
clean("snake")
clean("santa")
clean("fuel")
clean("game")
clean("beer")
clean("chart_incr")
clean("chart_decr")
clean("japan")
clean("korea")
clean("germany")
clean("china")
clean("france")
clean("itlay")
clean("money")
clean("rose")
clean("recycle")
clean("broken")
clean("angry")