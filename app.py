from flask import Flask
from flask_restful import Resource, Api
from gh_helpers import *


app = Flask(__name__)
api = Api(app)


gh_data = None

def clean_up(aRepos, aMembers):
  repos = []
  members = []
  for r in aRepos:
    rep = {
      'description':r['description'],
      'stargazers_count':r['stargazers_count'],
      'forks_count':r['forks_count'],
      'html_url':r['html_url'],
      'watchers_count':r['watchers_count'],
      'open_issues_count':r['open_issues_count'],
      'name':r['name']
    }
    repos.append(rep)

  for m in aMembers:
    mem = {
      'login':m['login'],
      'html_url':m['html_url']
    }
    members.append(mem)
    
  return repos, members

def getGhData():
  repos = getRepositories('moztn')
  repos = add_langs_to_repos(repos)
  leaders = get_leaders(repos)
  members = get_org_members('moztn')
  repos, members = clean_up(repos, members)
  global gh_data
  gh_data = {'repos':repos, 'leaders':leaders, 'members':members}
  print "Number of access {0}".format(api_access)


class GhData(Resource):
  def get(self):
    getGhData()
    return gh_data

#TODO:
# Raw data

api.add_resource(GhData, '/')

if __name__ == '__main__':
  app.run(debug=True)
