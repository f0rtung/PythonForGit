# coding=utf-8

from git import Repo
import time
from optparse import OptionParser
import os

join = os.path.join

def showCommitsInfo(commit):
    message = "Author: " + str(commit.author) + "\n"
    message += "Date: " + str(time.strftime("%a, %d %b %Y %H:%M", time.gmtime(commit.committed_date))) + "\n"
    message += "Message: " + str(commit.message)
    message += "SHA: " + str(commit.hexsha) + "\n"
    print(message)


parser = OptionParser()
# путь до bin-папки с гитом
parser.add_option("-g", "--gitPath", action="store", type="string", dest="GitPath")
# путь до репозитория, который проверяется (папка, в которой находится .git)
parser.add_option("-r", "--repoPath", action="store", type="string", dest="RepoPath")
# последний успешный коммпит (sha)
parser.add_option("-s", "--sucCommit", action="store", type="string", dest="SucCommit")
(options, args) = parser.parse_args()

if options.GitPath is None or options.RepoPath is None or options.SucCommit is None:
    print("Error args!")
    exit(-1)

os.environ["PATH"] += os.pathsep + options.GitPath
repo = Repo(options.RepoPath)

last_commits = list(repo.iter_commits('master'))
for commit in last_commits:
    showCommitsInfo(commit)
    if str(commit) == options.SucCommit:
        break