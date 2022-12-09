import os
import argparse
import sys

#
# Need to call this script:
#  1 - Enable Personal Access Tokens (PAT) for the organization (fine grained is better);
#  2 - Create a PAT in one member of the organization account, with access to read Members for organization;
#  3 - Create an environment variable with the PAT called GITHUB_ACCESS_TOKEN
#  4 - Run the script passing the organization name as argument.
#
# Obs: If your PAT is not from the organization, only public members are shown.
#      If yout PAT is from the organization, public and private members are shown.
#      If your PAT is not from an owner of the organization, the outside colaborators are not shown (and an error is thrown in the standard output)
#


import github

def main(org_name):
  access_token = os.getenv('GITHUB_ACCESS_TOKEN')

  if access_token == None:
    print('GITHUB_ACCESS_TOKEN environment variable not available.')
    return 1

  g = github.Github(access_token)

  o = g.get_organization(org_name)

  print('MemberName,MemberLogin,MemberEmail,MemberCompany,MemberType,Outside')
  for member in o.get_members():
    print("{},{},{},{},{}".format(str(member.name or ''), str(member.login or ''), str(member.email or ''), str(member.company or ''), str(member.type or '')), 'No')

  try:
    for outside in o.get_outside_collaborators():
      print("{},{},{},{},{}".format(str(outside.name or ''), str(outside.login or ''), str(outside.email or ''), str(outside.company or ''), str(outside.type or '')), 'Yes')
  except github.GithubException as error:
    print("Outside colaborators could not be retrieved. Reason: {}.".format(error), file=sys.stderr)


  return 0


if(__name__ == '__main__'):
  parser = argparse.ArgumentParser(description="Retrieves members of an organization. If your PAT is enabled for the organization, brings even the private members, if not, only the public ones. Outside collaborators are shown for PAT of organization owners.")
  parser.add_argument("organization")
  args = parser.parse_args()
  exit(main(args.organization))