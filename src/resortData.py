import shutil, os

'''
Resort data into train folder and test folder
'''

lots = os.listdir('../output')

for lot in lots:
	traindir = '../train/'+lot
	testdir = '../test/'+lot
	os.makedirs(traindir)
	os.makedirs(testdir)

	lotdir = '../output/'+lot

	files = list()
	for filename in os.listdir(filepath):
        if filename.endswith('.csv'):
            files.append(filename)

	

