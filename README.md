# AWS CodeCommit to GitHub Migration Script

## Overview

This Python script allows you to migrate repositories from AWS CodeCommit to GitHub using their respective APIs. The script retrieves the repositories, branches, and commits from AWS CodeCommit and pushes them to newly created repositories on GitHub.

## Features

- **Repository Migration**
- **Branch and Commit Transfer**

## Prerequisites

- **Python 3.6+**
- **AWS SDK for Python (Boto3)**
- **GitHub Personal Access Token**

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/codecommit-to-github-migration.git
    cd ./codecommit-to-github-migration/
    ```

2. **Install Required Python Packages**

    ```bash
    virtualenv -q ./venv/ && source ./venv/bin/activate
    pip install boto3 requests
    ```

3. **Set Environment Variables**

    - **AWS Credentials:** Ensure your AWS credentials are set up, either through environment variables or the AWS credentials file.
    - **GitHub Token:** Set your GitHub personal access token as an environment variable:

    ```bash
    export GITHUB_TOKEN='your_github_token'
    ```

## Important Notes

- **Rate Limits:** Be aware of GitHub's API rate limits. For large repositories or numerous migrations, you may need to handle rate limiting.
- **Error Handling:** The script includes basic error handling, but you may need to enhance this depending on the complexity of your repositories.
