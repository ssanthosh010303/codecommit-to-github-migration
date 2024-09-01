# Author: Apache X692
# Created on: 31/08/2024
import os

import boto3
import requests
import logging


def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def get_codecommit_repos(codecommit_client):
    repos = []
    paginator = codecommit_client.get_paginator("list_repositories")

    for page in paginator.paginate():
        repos.extend(page["repositories"])

    return [repo["repositoryName"] for repo in repos]


def get_codecommit_repo_data(codecommit_client, repo_name):
    branches = []
    commits = {}
    paginator = codecommit_client.get_paginator("list_branches")

    for page in paginator.paginate(repositoryName=repo_name):
        branches.extend(page["branches"])

    for branch in branches:
        commit_id = codecommit_client.get_branch(
            repositoryName=repo_name,
            branchName=branch
        )["branch"]["commitId"]
        commit_data = codecommit_client.get_commit(
            repositoryName=repo_name,
            commitId=commit_id
        )["commit"]
        commits[branch] = commit_data

    return commits


def create_github_repo(github_token, repo_name, private=True):
    headers = {"Authorization": f"token {github_token}"}
    data = {"name": repo_name, "private": private}

    response = requests.post(
        "https://api.github.com/user/repos",
        headers=headers,
        json=data
    )

    if response.status_code != 201:
        logging.error(f"Failed to create repository: {response.status_code}, {response.text}")

    return response.json()


def push_commits_to_github(github_token, repo_name, commits):
    headers = {"Authorization": f"token {github_token}"}

    for branch, commit_data in commits.items():
        commit_message = commit_data["message"]
        author = commit_data["author"]["name"]
        email = commit_data["author"]["email"]
        tree_sha = commit_data["treeId"]

        data = {
            "message": commit_message,
            "author": {
                "name": author,
                "email": email
            },
            "parents": [],
            "tree": tree_sha
        }

        response = requests.post(
            f"https://api.github.com/repos/yourusername/{repo_name}/git/commits",
            headers=headers,
            json=data
        )

        if response.status_code != 201:
            logging.error(f"Failed to create commit: {response.status_code}, {response.text}")
            continue

        commit_sha = response.json()["sha"]
        ref_data = {"sha": commit_sha}

        response = requests.patch(
            f"https://api.github.com/repos/yourusername/{repo_name}/git/refs/heads/{branch}",
            headers=headers,
            json=ref_data
        )

        if response.status_code != 200:
            logging.error(f"Failed to update ref for branch {branch}: {response.status_code}, {response.text}")


def migrate_repo(codecommit_client, github_token, repo_name):
    commits = get_codecommit_repo_data(codecommit_client, repo_name)
    create_github_repo(github_token, repo_name)

    push_commits_to_github(github_token, repo_name, commits)


def main():
    setup_logging()

    github_token = os.getenv("GITHUB_TOKEN")

    if not github_token:
        logging.error("GitHub token is not set; please set GITHUB_TOKEN environment variable.")
        return

    codecommit_client = boto3.client("codecommit", region_name="us-east-1")

    repos = get_codecommit_repos(codecommit_client)

    for repo in repos:
        logging.info(f"Migrating repository: {repo}")
        migrate_repo(codecommit_client, github_token, repo)


if __name__ == "__main__":
    main()
