from fastapi import HTTPException, status
import httpx
import base64
import re

from core.config import settings

async def get_code_from_github(url: str) -> str:
    """
    Fetches the content of files from a given GitHub repository URL.
    This is a simplified implementation that fetches the main file from a repo link
    or a specific file if the URL points to it.
    A full implementation would clone the repo.
    """
    match = re.match(r"https://github\.com/([^/]+)/([^/]+)", url)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid GitHub repository URL format. Expected: https://github.com/owner/repo",
        )
    
    owner, repo = match.groups()
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    
    headers = {}
    if settings.GITHUB_TOKEN:
        headers["Authorization"] = f"token {settings.GITHUB_TOKEN}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers=headers)
            response.raise_for_status()
            
            files = response.json()
            if not isinstance(files, list):
                 raise HTTPException(status_code=404, detail="No files found or invalid response.")

            # For this example, we'll just concatenate the content of the first 5 files found.
            # A real-world scenario would require a more sophisticated file selection logic.
            content_list = []
            files_to_fetch = [f for f in files if f['type'] == 'file'][:5]

            for file_info in files_to_fetch:
                file_content_response = await client.get(file_info['url'], headers=headers)
                file_content_response.raise_for_status()
                file_data = file_content_response.json()
                
                if file_data.get('encoding') == 'base64':
                    content = base64.b64decode(file_data['content']).decode('utf-8')
                    content_list.append(f"--- FILE: {file_info['name']} ---\n{content}\n")

            if not content_list:
                return "// No files could be fetched or repo is empty."

            return "\n".join(content_list)

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="GitHub repository not found.")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Failed to fetch from GitHub API: {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {e}")