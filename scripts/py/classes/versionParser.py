from pygit2 import Repository
from classes.helper import commitsForFile, commitsForFiles


class FileVersionParser:

    def __init__(self):

        self.repo = Repository('./.git')
        self.postIndexEntries = list()
        self.lastCommit = self.repo[self.repo.head.target]

    def loadFiles(self, path='posts'):

        for entry in self.repo.index:

            # Todo: Rewrite with proper Path handling

            # compares IndexEntry path to given path
            if '/'.join((entry.path.split('/'))[0:-1]) == path:
                self.postIndexEntries.append(entry)

        return

    def getCommitsForFiles(self, filepathList=None):
        '''wraps commitForFiles()'''

        # default is the own postIndexEntries, with full path
        if not filepathList:
            filepathList = [e.path for e in self.postIndexEntries]

        return commitsForFiles(self.repo, self.lastCommit, filepathList)

    def getCommitsForFile(self, path):
        '''wraps commitsForFile()'''

        commitList = list()
        for commit in commitsForFile(self.repo, self.lastCommit, path):
            commitList.append(commit)

        return commitList

