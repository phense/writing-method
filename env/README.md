# Credential examples

This folder holds example files only. They list variable names and where a
value comes from; they contain no values.

| File | Purpose | Secret inside the real file |
|---|---|---|
| `azure-speech.env.example` | Azure AI Speech key and region for per-line voicing | Yes |
| `elevenlabs.env.example` | Non-secret ElevenLabs choices; access runs through the connector | No |

## Set up Azure AI Speech

Prerequisite: an Azure Speech resource. The free tier is enough to start.

1. Copy the example into the folder where your video projects live:

   ```sh
   mkdir -p env
   cp /path/to/writing-method/env/azure-speech.env.example env/azure-speech.env
   chmod 600 env/azure-speech.env
   ```

2. Open `env/azure-speech.env` in an editor and enter key and region.
3. From a video project, check the access:

   ```sh
   python3 tools/voice_azure.py --check
   ```

   Expected: `credentials accepted, <number> voices available` and the
   languages of the profile's voice. Nothing is synthesized and nothing is
   charged.

The tools look for the file in this order: `--env <file>`, the variable
`AZURE_SPEECH_ENV`, `env_file` in the video profile, then `env/azure-speech.env`
in the video project or any parent folder.

If the check fails, the message names the missing file or variable. A rejected
key reads `the provider rejected the key (check key and region)`. The key
itself is never printed.

## Keep keys out of the repository

`env/*.env` is ignored by Git here and in the project template. Before you
publish a repository that contains video projects, confirm it:

```sh
git check-ignore env/azure-speech.env
```

The command prints the path when the file is ignored.
