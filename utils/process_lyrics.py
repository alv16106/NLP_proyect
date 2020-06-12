import argparse
import pandas as pd
import sys


parser = argparse.ArgumentParser(description='Put lyrics in csv')
parser.add_argument('-i', '--input', type=str, help='Input file dataset')
parser.add_argument('-d', '--directory', type=str, help='Lyrics Directory')

args = parser.parse_args()

def progress(count, total, status=''):
  bar_len = 60
  filled_len = int(round(bar_len * count / float(total)))

  percents = round(100.0 * count / float(total), 1)
  bar = '=' * filled_len + '-' * (bar_len - filled_len)

  sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
  sys.stdout.flush()  # As suggested by Rom Ruben (see: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/27871113#comment50529068_27871113)

def songs_count(path):
  with open(path) as f:
    count = len(f.readlines()) - 1
    return count


if __name__ == '__main__':
    totalTitles = songs_count(args.input)
  # Download songs
    count = 0
    errCount = 0
    Lyrics = []
    df = pd.read_csv(args.input)
    for _idx, song in df.iterrows():
        progress(count, totalTitles, 'Errors encountered: {}'.format(errCount))
        print(song)
        name = args.directory + '_'.join([song['mood'], song['artist'], song['title']])
        try:
            lf = open(name, 'r')
            count += 1
        except:
            print('No lyrics for:', name)
            df.drop(df.index[_idx])
            errCount += 1
        text = lf.read()
        Lyrics.append(text)
    
    df2 = df.assign(Lyrics = Lyrics)
    train = df2.sample(frac=0.8, random_state=200) #random state is a seed value
    test = df2.drop(train.index)
    train.to_csv('mood_train.csv')
    test.to_csv('mood_test.csv')


