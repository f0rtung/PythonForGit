# coding=utf-8
# скрипт принимает на вход путь до репозитория, в котором
# необходимо проверить переданную подпапку на наличие изменений
# Если в этой папке есть изменения, то скрипт завершается с
# ошибкой - ставить тег на весь репозиторий нельзя. Если
# в репозитории есть изменения, но измененные файлы находятся
# в других директориях, то считаем, что можно ставить тег на репозиторий


from git import Repo
from optparse import OptionParser
import os

join = os.path.join


def getListModifiedFiles(repo):
    print("Get modified files:")
    listOfFiles = []
    diff = repo.index.diff(None)
    for file in diff:
        print(file.a_path)
        listOfFiles.append(file.a_path)
    return listOfFiles


# проверяем список изменненных файлов на совпадение
# с частью пути до папки, изменения в которой проверяются
def CheckFolders(folderList, partOfFolder):
    for path in folderList:
        if path.find(partOfFolder) != -1:
            return True
    return False


def prepareFolderPart(path):
    return path.replace("\\", "/")


parser = OptionParser()
# путь до bin-папки с гитом
parser.add_option("-g", "--gitPath", action="store", type="string", dest="GitPath")
# путь до репозитория, который проверяется (папка, в которой находится .git)
parser.add_option("-r", "--repoPath", action="store", type="string", dest="RepoPath")
# часть пути отностиельно RepoPath до репозитория, который должен быть проверен
parser.add_option("-f", "--partOfFolder", action="store", type="string", dest="FolderPart")
(options, args) = parser.parse_args()

# если не была передана часть пути, то выводим сообщение с ошибкйой и заканчиваем работу
if options.FolderPart is None or options.GitPath is None or options.RepoPath is None:
    print("Error args!")
    exit(-1)
os.environ["PATH"] += os.pathsep + options.GitPath

# поворачиваем слеш в пути к репе
folderPart = prepareFolderPart(options.FolderPart)
# получаем список файлов, которые изменены во всем репозитории
listOfFiles = getListModifiedFiles(Repo(options.RepoPath))

if len(listOfFiles):
    # если есть модифицированные файлы + передан весь каталог на проверку = выход
    if options.FolderPart == ".":
        exit(-1)
    # если есть модифицированные файлы + они находятся в проверяемой директории = выход
    if CheckFolders(listOfFiles, folderPart):
        exit(-1)
exit(0)
