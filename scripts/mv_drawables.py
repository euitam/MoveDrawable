import sys, os, errno, shutil, signal, subprocess
from glob import glob

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def printTitle():
	print bcolors.WARNING
	print "   _             _           _     _ "
	print "  /_\  _ __   __| |_ __ ___ (_) __| |"
	print " //_\\\\| '_ \ / _` | '__/ _ \| |/ _` |"
	print "/  _  \ | | | (_| | | | (_) | | (_| |"
	print "\_/ \_/_| |_|\__,_|_|  \___/|_|\__,_|"
	print ""
	print "    ___                         _     _      "
	print "   /   \_ __ __ ___      ____ _| |__ | | ___ "
	print "  / /\ / '__/ _` \ \ /\ / / _` | '_ \| |/ _ \\"
	print " / /_//| | | (_| |\ V  V / (_| | |_) | |  __/"
	print "/___,' |_|  \__,_| \_/\_/ \__,_|_.__/|_|\___|"
	print bcolors.ENDC

def moveFileToTmp(file):
	destFile = ''
	if '1.5x' in file:
		filename = os.path.basename(file).replace('@1.5x', '').replace('1.5x', '').strip()
		destFile = HDPI_DIR + filename
	elif '2x' in file:
		filename = os.path.basename(file).replace('@2x', '').replace('2x', '').strip()
		destFile = XHDPI_DIR + filename
	elif '3x' in file:
		filename = os.path.basename(file).replace('@3x', '').replace('3x', '').strip()
		destFile = XXHDPI_DIR + filename
	elif '4x' in file:
		filename = os.path.basename(file).replace('@4x', '').replace('4x', '').strip()
		destFile = XXXHDPI_DIR + filename
	else:
		filename = os.path.basename(file).replace('@1x', '').replace('1x', '').strip()
		destFile = MDPI_DIR + filename

	if len(destFile) > 0:
		shutil.copyfile(file, destFile)


def createDirIfNotExists(directory):
	try:
		os.makedirs(directory)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise

def renameFile(srcFilename, destFilename):
	images = [y for x in os.walk(TMP_DIR) for y in glob(os.path.join(x[0], srcFilename))]
	for file in images:
		dirName = os.path.dirname(file)
		os.rename(file, dirName + '/' + destFilename)

def moveToDest(cwebp):
	for folder in RESULT_DIRS:
		currentFolder = TMP_DIR + folder
		destFolder = destDir + folder
		createDirIfNotExists(destFolder)
		srcFiles = os.listdir(currentFolder)
		for file in srcFiles:
			fullFileName = os.path.join(currentFolder, file)
			if len(cwebp) > 0:
				destFile = destFolder + file.replace('.png', '.webp').strip()
				FNULL = open(os.devnull, 'w')
				subprocess.call([cwebp, '-q', '80', fullFileName, '-o', destFile], stdout=FNULL, stderr=subprocess.STDOUT)
			else:
				destFile = destFolder + file
				shutil.move(fullFileName, destFile)
			print "move {} to {}".format(fullFileName, destFile)

def cleanup():
	if os.path.isdir(TMP_DIR):
		shutil.rmtree(TMP_DIR)

def getWebpConverter():
	base_dir = os.path.dirname(os.path.realpath(__file__))
	cwebp = "{}/cwebp".format(base_dir)
	if os.path.isfile(cwebp):
		return cwebp
	else:
		return ""

def sigint_handler(signum, frame):
	print ""
	print ""
	print bcolors.WARNING + "Exit script requested" + bcolors.ENDC
	sys.exit()
 
signal.signal(signal.SIGINT, sigint_handler)

# BEGIN SCRIPT
printTitle()

print bcolors.FAIL
print "Exit script anytime with CTRL+C"
print bcolors.ENDC

# Check argument number
if len(sys.argv) < 3:
	print "Usage: {} SRC_DIRECTORY ANDROID_RESOURCES_DIRECTORY".format(sys.argv[0])
	sys.exit()

srcDir = sys.argv[1]
destDir = sys.argv[2]

TMP_DIR = srcDir + '/tmp'

MDPI = '/drawable-mdpi/'
HDPI = '/drawable-hdpi/'
XHDPI = '/drawable-xhdpi/'
XXHDPI = '/drawable-xxhdpi/'
XXXHDPI = '/drawable-xxxhdpi/'

MDPI_DIR = TMP_DIR + MDPI
HDPI_DIR = TMP_DIR + HDPI
XHDPI_DIR = TMP_DIR + XHDPI
XXHDPI_DIR = TMP_DIR + XXHDPI
XXXHDPI_DIR = TMP_DIR + XXXHDPI

RESULT_DIRS = [MDPI, HDPI, XHDPI, XXHDPI, XXXHDPI]

cleanup()

# Check source directory
if not os.path.isdir(srcDir):
	print "{} should be a directory".format(srcDir)
	exit()

# Check destination directory
if not os.path.isdir(destDir):
	print "{} should be a directory".format(destDir)
	exit()

if not os.path.isdir(destDir+'/values'):
	print "{} is not an Android resources directory".format(destDir)
	exit()

if not os.path.isdir(destDir+'/layout'):
	print "{} is not an Android resources directory".format(destDir)
	exit()

images = [y for x in os.walk(srcDir) for y in glob(os.path.join(x[0], '*.png'))]

if len(images) == 0:
	print bcolors.FAIL+"No files to process"+bcolors.ENDC
	exit()

# CONSTANTS

# Create density directories
createDirIfNotExists(MDPI_DIR)
createDirIfNotExists(HDPI_DIR)
createDirIfNotExists(XHDPI_DIR)
createDirIfNotExists(XXHDPI_DIR)
createDirIfNotExists(XXXHDPI_DIR)

for file in images:
	# print "- {}".format(file)
	moveFileToTmp(file)

# build distinct names
newImages = [y for x in os.walk(TMP_DIR) for y in glob(os.path.join(x[0], '*.png'))]
distinctNames = []
print bcolors.BOLD + 'Drawable files found:' + bcolors.ENDC
for file in newImages:
	name = os.path.basename(file)
	if not name in distinctNames:
		print '- {}'.format(name)
		distinctNames.append(name)

# Ask for renaming
print ""
if len(distinctNames):
	print bcolors.HEADER + "Any existing file will be overwritten by the renaming" + bcolors.ENDC
for name in distinctNames:
	newName = raw_input('Rename '+bcolors.OKBLUE+name.replace('.png', '')+bcolors.ENDC+' to ('+bcolors.UNDERLINE+'leave blank to skip renaming'+bcolors.ENDC+'): ')
	newName = "{}.png".format(newName).strip()
	if len(newName) > 0:
		renameFile(name, newName)

# Ask for WebP compression
cwebp = getWebpConverter()
compress = False
if len(cwebp) > 0:
	compressResponse = raw_input('Compress files to WebP format? [y] or [n] ')
	compressResponse = compressResponse.strip()
	if len(compressResponse) > 0 and (compressResponse == 'y' or compressResponse == 'Y'):
		compress = True

# Move to destination folder
if compress:
	moveToDest(cwebp)
else:
	moveToDest("")

print ""
print bcolors.OKGREEN + '{} resource files moved to workspace'.format(len(newImages)) + bcolors.ENDC

cleanup()
