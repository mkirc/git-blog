from os import path, mkdir, listdir
from pathlib import Path
from shutil import rmtree
from classes.helper import (
        escapedFileName,
        escapedShortHash,
        getFnameFromPath,
        getMetaDataBlock
    )
from classes.versionParser import FileVersionParser
from classes.templateGenerator import TemplateFactory, NavTemplate




class ProjectController:

    def __init__(self):

        self.fvp = FileVersionParser()
        self.fvp.loadFiles()
        self.tf = TemplateFactory()
        self.tmpBase = self.getTMPBase()
        self.postPaths = [e.path for e in self.fvp.postIndexEntries]

    def getTMPBase(self):
        '''
        Finds relative Path to git-blog/tmp regardless of nt / posixness
        of path
        '''

        tmpPath = Path(path.split(path.realpath(__file__))[0])
        tmpPath = tmpPath / '../../tmp'
        if tmpPath.exists():
            return tmpPath
        else:
            # No tmp path error
            pass

    def getCommitsForPosts(self):

        self.postsCommits = self.fvp.getCommitsForFiles()

        return

    def readyTemplateFactory(self):

        self.tf.loadPostsCommits(self.postsCommits)

        return


    def navTest(self):

        test_tf = TemplateFactory()
        test_fvp = FileVersionParser()
        _theStuff = dict()
        _commitlist = test_fvp.getCommitsForFile('README.md')
        _theStuff = [(e.oid, e.tree['README.md']) for e in _commitlist]
        test_tf.postsCommits = {'README.md': _theStuff}

        # for nav in test_tf.yieldTopNavsForPostPath('README.md'):
        #     print(nav.assembleHTML())
        #     break
        print([nav for nav in test_tf.yieldSideNavs()][0].assembleHTML())

        return

    def createTmpDirTree(self):
        '''
        creates a tree like post-1/ ... post-n/
        in self.tmpBase (defaults to projectdir/tmp/)
        '''


        if path.isdir(self.tmpBase):
            for postpath, commits in self.postsCommits.items():
                _post = escapedFileName(postpath)
                mkdir(self.tmpBase / _post)
        return

    def cleanTmpDir(self):

        if path.isdir(self.tmpBase):
            for file in listdir(self.tmpBase):
                if path.isdir(self.tmpBase / file):
                    rmtree(self.tmpBase / file)

        return


    def writeCommitDataToTmpPostDirs(self):

        for postpath, commits in self.postsCommits.items():
            tmpPostPath = self.tmpBase / escapedFileName(postpath)
            if path.isdir(tmpPostPath):
                suffix = path.splitext(getFnameFromPath(postpath))[-1]
                for commit in commits:

                    # creates yml metadata for pandoc
                    metaData = getMetaDataBlock(commit[0], self.fvp.repo)

                    shortHash = escapedShortHash(commit[0])
                    fileName = shortHash + suffix
                    outPath = tmpPostPath / fileName
                    # produces actually portable path
                    outPath = path.normpath(outPath)
                    with open(outPath, 'w+') as OpenFile:
                        OpenFile.write(metaData)
                        OpenFile.write(commit[1].data.decode('utf-8'))
        return

    def writeSideNavsToTmpPostDirs(self):

        for sideNav in self.tf.yieldSideNavs():
            tmpPostPath = self.tmpBase / sideNav.post
            if path.isdir(tmpPostPath):
                fileName = sideNav.shortHash + '_' + sideNav.cssClass + '.html'
                outPath = tmpPostPath / fileName
                outPath = path.normpath(outPath)
                with open(outPath, 'w+') as OpenFile:
                    OpenFile.write(sideNav.assembleHTML())
        return


    def writeTopNavsToTmpPostDirs(self):

        for postpath in self.postsCommits.keys():
            tmpPostPath = self.tmpBase / escapedFileName(postpath)
            if path.isdir(tmpPostPath):
                for topNav in self.tf.yieldTopNavsForPostPath(postpath):
                    fileName = topNav.shortHash + '_' + topNav.cssClass + '.html'
                    outPath = tmpPostPath / fileName
                    outPath = path.normpath(outPath)
                    with open(outPath, 'w+') as OpenFile:
                        OpenFile.write(topNav.assembleHTML())




if __name__ == '__main__':

    pc = ProjectController()
    pc.getCommitsForPosts()
    # for k,v in pc.postsCommits.items():
    #     print(k, v[0][0])
    pc.readyTemplateFactory()
    # pc.navTest()


    pc.cleanTmpDir() # cleans up old messes
    # creates new messes from here on

    pc.createTmpDirTree()
    pc.writeSideNavsToTmpPostDirs()
    pc.writeTopNavsToTmpPostDirs()
    pc.writeCommitDataToTmpPostDirs()

