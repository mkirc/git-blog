from os import path
from datetime import datetime
from html import escape
from pygit2 import GIT_SORT_TIME

def getFnameFromPath(filepath):

    return escape(path.split(filepath)[-1])

def stripSuffix(filename):

    return path.splitext(filename)[0]

def escapedFileName(filepath):

    x = getFnameFromPath(filepath)
    
    return stripSuffix(x)

def escapedShortHash(commitID):

    return escape(str(commitID)[0:7])

def utcFromUnixTs(unixtime):

    out = datetime.utcfromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S')
    return out

def addPlusIfGEZero(number):
    '''this may be the dumbest thing i ever wrote'''

    if number >= 0:
        return '+' + str(number)
    else:
        return str(number)

def metaDataForCommitAndRepo(commitID, repo):

    commit = repo[commitID]
    time = utcFromUnixTs(commit.commit_time) + ' UTC '
    time += addPlusIfGEZero(commit.commit_time_offset // 60)
    return {'author' : commit.author.name,
            'date': time,
            'commitmsg' : escape(commit.message.strip())}

def getMetaDataBlock(commitID, repo):
    ''' returns yml metadata block for pandoc'''

    data = metaDataForCommitAndRepo(commitID, repo)
    block = '---\n'
    for k,v in data.items():
        block += k + ': ' + v 
        block += '\n'
    else:
        block += '...\n'
    return block

def commitsForFiles(repo, lastCommit, filepathList):
    '''
    takes a repo, a commit and a list of filepaths,
    performs a TIME_SORT and
    returns {filepath: [{commit.oid, blob.object}] }
    '''
    files_commits = dict()

    for commit in repo.walk(lastCommit.id, GIT_SORT_TIME):
        for filepath in filepathList:
            if filepath in commit.tree:
                if not filepath in files_commits.keys():
                    files_commits[filepath] = []
                _oidObjTuple = (commit.oid, commit.tree[filepath])
                files_commits[filepath].append(_oidObjTuple)

    return filterUniqueCommits(files_commits)

def filterUniqueCommits(files_commits):
    ''' 
    takes files_commits dict, iterates over its entries,
    compares the commits list against a set of themselves.
    Goal is to keep time-sorted order, which set() removes.
    returns files_commits dict
    '''

    unique_files_commits = dict()
    
    for postpath, commits in files_commits.items():
        unique_ids = set([c[1].oid for c in commits])
        filtered_commits = []
        found_ids = []

        for commit in reversed(commits):
            cur_id = commit[1].oid
            if cur_id in unique_ids and cur_id not in found_ids:
                filtered_commits.append(commit)
                found_ids.append(cur_id)
            if len(found_ids) >= len(unique_ids):
                break
        unique_files_commits[postpath] = list(reversed(filtered_commits))

    return unique_files_commits

def commitsForFile(repo, lastCommit, filepath):
    '''
    accepts the name of the file to search, and a commit,
    from which on to search, returns an iterator over the
    objects related to the file, descending in time.
    '''
    last_oid = None

    # iterate over commits
    for commit in repo.walk(lastCommit.id, GIT_SORT_TIME):
        # check occurence of file
        if filepath in commit.tree:
            # compare to last found object
            if commit.tree[filepath].oid != last_oid:
                yield commit
            # either w)y, set last_obj to this object
            last_oid = commit.tree[filepath].oid

