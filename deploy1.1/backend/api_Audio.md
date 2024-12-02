

Here's the `curl` command that you can copy and test directly in your terminal or command prompt:

```bash
curl -L -X POST "http://103.253.20.13:25010/api/text-to-speech" \
-H "Content-Type: application/json" \
-d "{\"text\": \"Hello, this is a test message\", \"voice\": \"en-CA-ClaraNeural\", \"speed\": 1}" \
--output "test_output.mp3"
```

Or as a single line:

```bash
curl -L -X POST "http://103.253.20.13:25010/api/text-to-speech" -H "Content-Type: application/json" -d "{\"text\": \"Hello, this is a test message\", \"voice\": \"en-CA-ClaraNeural\", \"speed\": 1}" --output "test_output.mp3"
```

To test different voices, you can try these variations:

```bash
# British English voice
curl -L -X POST "http://103.253.20.13:25010/api/text-to-speech" -H "Content-Type: application/json" -d "{\"text\": \"Hello, this is a test message\", \"voice\": \"en-GB-SoniaNeural\", \"speed\": 1}" --output "british_voice.mp3"

# American English voice
curl -L -X POST "http://103.253.20.13:25010/api/text-to-speech" -H "Content-Type: application/json" -d "{\"text\": \"Hello, this is a test message\", \"voice\": \"en-US-JennyNeural\", \"speed\": 1}" --output "american_voice.mp3"
```

Parameters explained:
- `-L`: Follow redirects
- `-X POST`: Specify POST method
- `-H`: Set header
- `-d`: Send data
- `--output`: Save the response to a file

The audio file will be saved in your current directory with the specified filename (e.g., `test_output.mp3`, `british_voice.mp3`, etc.).
