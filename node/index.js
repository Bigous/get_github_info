import { Octokit } from "@octokit/rest";

async function main() {
  const octokit = new Octokit({ auth: process.env.GITHUB_ACCESS_TOKEN });

  // const res = await octokit.rest.orgs.listMembers({ org: 'BCJTI' });
  const members = [];
  let retrieved = 100;
  let page = 1;
  while(retrieved == 100) {
    const res = await octokit.orgs.listMembers({org: 'microsoft', per_page: 100, page});
    if (res.status == 200) {
      page = page + 1;
      retrieved = res.data.length;
      members.push(...res.data);
    } else {
      console.warn(res);
      return;
    }
  }
  // const res = await octokit.rest.repos.listForOrg({org: 'BCJTI', type: 'public'});
  // if (res.status == 200) {
  //   console.log(res.data);
  // } else {
  //   console.warn(res);
  // }

}

if (process.env.GITHUB_ACCESS_TOKEN) {
  main();
} else {
  console.error(`GITHUB_ACCESS_TOKEN not available in the environment.`);
}
