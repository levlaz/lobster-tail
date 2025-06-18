# 🦞 Lobster Tail

A simple bash script that scrapes [Lobste.rs](https://lobste.rs) and opens all the front page stories in your default browser.

## Features

- 🦞 Scrapes the Lobste.rs front page for story links
- 🌐 Opens all stories in your default browser with one command
- 🖥️ Cross-platform support (macOS, Linux, Windows)
- 📊 Shows you exactly which stories will be opened before proceeding
- ⚡ Built-in rate limiting to avoid overwhelming your browser

## Usage

1. Make the script executable:
   ```bash
   chmod +x lobster_opener.sh
   ```

2. Run the script:
   ```bash
   ./lobster_opener.sh
   ```

3. The script will:
   - Fetch the current stories from Lobste.rs
   - Display a numbered list of all stories found
   - Ask for confirmation before opening them
   - Open each story in your default browser with a small delay

## Example Output

```
🦞 Lobste.rs Story Opener (Bash Version)
========================================
Fetching stories from lobste.rs...
Found 25 stories!

Stories to open:
1. https://example.com/story1
2. https://example.com/story2
...

Open all 25 stories in your browser? (y/N): y

Opening stories...
Opening 1/25: https://example.com/story1
Opening 2/25: https://example.com/story2
...

✅ Successfully opened 25/25 stories!
```

## Requirements

- `curl` - for fetching web pages
- `grep` - for text processing
- `sed` - for text manipulation
- A system command to open URLs:
  - macOS: `open` (built-in)
  - Linux: `xdg-open` (usually pre-installed)
  - Windows: `start` (built-in)

## Platform Support

- ✅ **macOS**: Uses the `open` command
- ✅ **Linux**: Uses `xdg-open` command
- ✅ **Windows**: Uses `start` command
- ⚠️ **Other systems**: Will display URLs for manual copying

## How It Works

1. **Fetches HTML**: Downloads the Lobste.rs front page using `curl`
2. **Extracts URLs**: Uses `grep` and `sed` to find all story links with `class="u-url"`
3. **Processes URLs**: Converts relative URLs to absolute URLs
4. **User Confirmation**: Shows all stories and asks for permission
5. **Opens Stories**: Uses the appropriate system command to open each URL

## Development

This project was built using:
- **[Amazon Q](https://aws.amazon.com/q/)** - AI assistant for development
- **[Claude](https://claude.ai)** - AI assistant for code generation and debugging
- **[Container Use by Dagger](https://github.com/dagger/container-use)** - Development environment management

## Contributing

Feel free to submit issues and pull requests! Some ideas for improvements:

- Add support for filtering stories by tags
- Add option to save stories to a file instead of opening
- Add support for other Lobsters-like sites
- Add configuration file support

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This script is for educational and personal use. Please be respectful of Lobste.rs and don't abuse their servers with excessive requests.