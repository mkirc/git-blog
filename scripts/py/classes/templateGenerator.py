from html import escape
from classes.helper import escapedFileName, escapedShortHash


class NavTemplate:

    def __init__(self, post, shortHash, postsCommits, cssClass):

        self.cssClass = cssClass
        self.post = post
        self.baseURL = 'blog/'
        self.shortHash = shortHash
        self.postsCommits = postsCommits

class NavSide(NavTemplate):

    def __init__(self, *args):

        super(NavSide, self).__init__(*args)

    def assembleHTML(self):

        html = '<nav class="' + escape(self.cssClass) + '"><ul>'

        for postpath, commits in self.postsCommits.items():
            _post = escapedFileName(postpath)
            _shortHash = escapedShortHash(commits[0][0])
            html += '<li'
            if _post == self.post and _shortHash == self.shortHash:
                html += ' class="active"'
            html += '><a'
            html += ' id="' + _shortHash + '"'
            html += ' href="/' + self.baseURL + _post + '/' + _shortHash + '.html"'
            html += '>'
            html += _post
            html += '</a></li>'
        else:
            html += '</ul></nav>' + '\n'

        return html

class NavTop(NavTemplate):

    def __init__(self, *args):

        # Note, that self.post is in fact the postpath,
        # not the filename, like in NavSide

        super(NavTop, self).__init__(*args)

    def assembleHTML(self):
        html = '<nav class="' + escape(self.cssClass) + '"><ul>'

        for commit in self.postsCommits[self.post]:
            _post = escapedFileName(self.post)
            _shortHash = escapedShortHash(commit[0])
            html += '<li'
            if _shortHash == self.shortHash:
                html += ' class="active"'
            html += '><a'
            html += ' id="' + _shortHash + '"'
            html += ' href="/' + self.baseURL + _post + '/' + _shortHash + '.html"'
            html += '>'
            html += _shortHash
            html += '</a></li>'
        else:
            html += '</ul></nav>' + '\n'

        return html



class TemplateFactory:
    
    def __init__(self):

        self.postsCommits = None

    def loadPostsCommits(self, postsCommits):

        '''expects a postsCommits - dict like
        {postpath: [(commit.oid, obj.oid)]'''

        self.postsCommits = postsCommits
        return

    def yieldSideNavs(self):

        if self.postsCommits:
            for postpath, commits in self.postsCommits.items():
                post = escapedFileName(postpath)
                shortHash = escapedShortHash(commits[0][0])
                yield NavSide(post, shortHash, self.postsCommits, 'nav-side')

    def yieldTopNavsForPostPath(self, postpath):

        if self.postsCommits:
            for commit in self.postsCommits[postpath]:
                shortHash = escapedShortHash(commit[0])
                yield NavTop(postpath, shortHash, self.postsCommits, 'nav-top')

