# mado

One markdown file, edited in its live preview. One window, nothing else.

## Run

```sh
./mado welcome.md
```

Open the printed URL (it opens automatically). `Ctrl+C` stops it. No install — Python 3 standard library only.

## Use

- Click any block to edit its raw markdown in place — headings, lists, tables, code, quotes, even `---` dividers. A blank line splits the block on render; empty text deletes it. Click away or press `Esc` to render it again.
- Task checkboxes are clickable and save their state.
- Click a table field to edit just that cell; Tab or arrow past the last cell opens the full table source. Frontmatter stays hidden — click its marker to edit.
- Click the open space below the last block to append markdown, as if editing the raw file.
- Frontmatter stays hidden in the preview. Autosaves to the one file. `Cmd+S` saves now. `Cmd+E` shows the raw file when you need it, `Cmd+E` again returns to preview.

## Files

- [mado.py](/Users/tomkorbmacher/src/mado/mado.py) — tiny server for the one file
- [index.html](/Users/tomkorbmacher/src/mado/index.html) — the preview editor, markdown renderer included, no dependencies
