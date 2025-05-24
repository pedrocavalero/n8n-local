# n8n Workflow: YouTube Video to WordPress Blog Post

This document provides instructions for setting up and using the n8n workflow that automates converting YouTube video transcripts into WordPress blog posts.

## Workflow Overview

1.  **Telegram Trigger**: You send a YouTube video URL to your configured Telegram bot.
2.  **Extract Video ID**: The workflow extracts the unique video ID from the URL.
3.  **Execute Command (Fetch Transcript)**: A Python script (`get_transcript.py`) uses the `youtube-transcript-api` to fetch the video's transcript.
4.  **OpenAI**: The transcript is sent to OpenAI (using a model like GPT-3.5 Turbo) with a prompt to generate a blog post.
5.  **WordPress**: The generated blog post content is used to create a new draft post in your WordPress site.

## Files Provided

*   `workflow.json`: The n8n workflow definition file.
*   `get_transcript.py`: The Python script required to fetch YouTube transcripts.

## Setup Instructions

### 1. Import the Workflow into n8n

1.  Download the `workflow.json` file.
2.  In your n8n instance, go to "Workflows".
3.  Click the "Import from File" button.
4.  Select the `workflow.json` file you downloaded and import it.

### 2. Set up the Python Script for Transcript Fetching

The workflow uses a Python script to get video transcripts.

1.  **Script Content (`get_transcript.py`)**:
    ```python
    from youtube_transcript_api import YouTubeTranscriptApi
    import json
    import sys

    video_id = ""

    # The n8n Execute Command node passes arguments after the script name.
    # We expect the videoId as the first argument.
    if len(sys.argv) > 1:
        video_id = sys.argv[1]
    else:
        # If no video_id is passed, print an error to stderr and exit.
        # n8n will capture stderr in the 'errorDetails' output of the Execute Command node.
        print("Error: No video ID provided as a command line argument.", file=sys.stderr)
        sys.exit(1)

    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        full_transcript = " ".join([item['text'] for item in transcript_list])
        # Print the transcript to stdout. n8n will capture this in the 'stdout' field.
        print(full_transcript)
    except Exception as e:
        # If any error occurs during transcript fetching, print it to stderr and exit.
        print(f"Error fetching transcript for video ID '{video_id}': {e}", file=sys.stderr)
        sys.exit(1)
    ```

2.  **Place the Script on Your n8n Server**:
    *   The workflow's "Execute Command" node (named "Execute youtube-transcript-api") is pre-configured to find this script at `/home/node/.n8n/scripts/get_transcript.py`.
    *   Create the directory if it doesn't exist (e.g., `mkdir -p /home/node/.n8n/scripts`).
    *   Copy the content above into a file named `get_transcript.py` at that location.
    *   **Important**: If you place the script in a different path, you **must** update the command in the "Execute youtube-transcript-api" node in n8n. For example, if you place it at `/opt/n8n_scripts/get_transcript.py`, change the "Command" field to `python` and the "Arguments" field (specifically the script path argument) to `/opt/n8n_scripts/get_transcript.py`.

3.  **Install Dependencies in n8n's Execution Environment**:
    *   The Python script requires the `youtube-transcript-api` library.
    *   You need to ensure Python 3 is available in your n8n's execution environment.
    *   Install the library using pip:
        ```bash
        pip install youtube-transcript-api
        ```
    *   Depending on your n8n setup (e.g., Docker), you might need to add this to your Dockerfile or install it in the running container. Consult your n8n installation guide for adding custom Python packages. If using a cloud-hosted n8n, check their documentation for Python environment customization.

### 3. Configure Credentials

You'll need to add API keys and credentials to n8n for the workflow to access the required services.

1.  **Telegram Bot API Token**:
    *   **How to get it**: Create a new bot by talking to the "BotFather" on Telegram. He will provide you with an API token.
    *   **In n8n**:
        1.  Go to "Credentials" in the left sidebar.
        2.  Click "Add credential".
        3.  Select "Telegram API" from the list.
        4.  Give it a name (e.g., "My Telegram Bot").
        5.  Paste your bot's API token into the "Access Token" field.
        6.  Save the credential.
        7.  In the "Telegram Trigger" node in the workflow, select your newly created credential from the "Credential for Telegram API" dropdown. The workflow JSON uses `YOUR_TELEGRAM_BOT_API_TOKEN_ID` as a placeholder; n8n will prompt you to select an existing credential or create a new one.

2.  **OpenAI API Key**:
    *   **How to get it**: Sign up or log in to your OpenAI account at [platform.openai.com](https://platform.openai.com/) and navigate to the API keys section.
    *   **In n8n**:
        1.  Go to "Credentials".
        2.  Click "Add credential".
        3.  Select "OpenAI API" from the list.
        4.  Give it a name (e.g., "My OpenAI Key").
        5.  Paste your OpenAI API key into the "API Key" field.
        6.  Save the credential.
        7.  In the "OpenAI" node, select your credential from the "Credential for OpenAI API" dropdown. The workflow JSON uses `YOUR_OPENAI_API_KEY_ID`.

3.  **WordPress Credentials**:
    *   **Required**:
        *   Your WordPress site URL (e.g., `https://example.com`).
        *   A WordPress Username.
        *   An **Application Password**. For security, it's highly recommended to use Application Passwords instead of your main user password.
    *   **How to get an Application Password**:
        1.  Log in to your WordPress admin dashboard.
        2.  Go to "Users" -> "Profile".
        3.  Scroll down to the "Application Passwords" section.
        4.  Enter a name for the new application password (e.g., "n8n Workflow") and click "Add New Application Password".
        5.  **Copy the generated password immediately.** You won't be able to see it again.
        6.  For more details, see the official WordPress documentation: [Application Passwords](https://wordpress.org/documentation/article/application-passwords/)
    *   **In n8n**:
        1.  Go to "Credentials".
        2.  Click "Add credential".
        3.  Select "WordPress API" from the list.
        4.  Give it a name (e.g., "My WordPress Site").
        5.  Enter your WordPress site URL in the "Base URL" field (e.g., `https://yourdomain.com`).
        6.  Enter your WordPress username in the "Username" field.
        7.  Paste the **Application Password** (not your main password) into the "Password" field.
        8.  Select "Basic Auth" for Authentication.
        9.  Save the credential.
        10. In the "WordPress" node, select your credential from the "Credential for WordPress API" dropdown. The workflow JSON uses `YOUR_WORDPRESS_CREDENTIALS_ID`.

### 4. Activate and Test the Workflow

1.  Once all nodes are configured and credentials are set up, click the "Active" toggle at the top of the workflow editor to enable it.
2.  Send a YouTube video URL (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ` or `https://youtu.be/dQw4w9WgXcQ`) to the Telegram bot you linked.
3.  Check the "Executions" tab in n8n to see the workflow run. If there are errors, inspect the details for each node.
4.  If successful, a new draft post should appear in your WordPress admin area under "Posts".

## Customizing the Workflow

*   **OpenAI Model**:
    *   In the "OpenAI" node, you can change the "Model" parameter to use a different model (e.g., `gpt-4` if you have access, or other variations of GPT-3.5). Note that different models have different costs and capabilities.
*   **OpenAI Prompt**:
    *   The current prompt in the "OpenAI" node is:
        ```
        Based on the following video transcript, write a comprehensive blog post. The post should have a clear title, an introduction, several paragraphs discussing the key points, and a conclusion. 

        Transcript: {{ $json.stdout }}
        ```
    *   You can modify this prompt to change the tone, length, style, or specific instructions for the blog post. For example, you could ask for a specific number of words, a more casual tone, or to focus on certain aspects.
*   **Dynamic WordPress Post Title**:
    *   Currently, the WordPress post title is static ("New Blog Post from YouTube Video").
    *   To make it dynamic:
        1.  Modify the OpenAI prompt to explicitly ask for a title and content, perhaps in a JSON format. For example:
            ```
            Based on the following video transcript, generate a blog post. Output a JSON object with two keys: "title" (a suitable blog post title) and "content" (the blog post body).

            Transcript: {{ $json.stdout }}
            ```
        2.  In the "OpenAI" node, you might need to adjust how it processes the output if it's JSON (e.g., use "Output Format: JSON").
        3.  In the "WordPress" node:
            *   Set the "Title" field to an expression that extracts the title, e.g., `{{ $json.choices[0].message.content.title }}` (this path depends on how OpenAI returns the JSON and how n8n parses it; you may need to inspect the OpenAI node's output and adjust).
            *   Set the "Content" field to an expression that extracts the content, e.g., `{{ $json.choices[0].message.content.content }}`.
*   **WordPress Post Status**:
    *   The "WordPress" node is currently set to create posts with "Status: draft".
    *   You can change this to "publish" directly, or add other statuses like "pending".
*   **Error Handling**:
    *   Consider adding error handling branches in the workflow (e.g., if a transcript cannot be fetched or OpenAI fails). You could send a notification back via Telegram or another service.

Enjoy automating your content creation!
