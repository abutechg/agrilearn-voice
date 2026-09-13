Place only consented real WAV recordings in this folder.

1. Copy `metadata.example.csv` to `metadata.csv`.
2. Replace the example row with one row per recording.
3. Keep the `audio` filename exactly equal to the WAV file name.
4. Set `consent` to `yes` only after the speaker has agreed to evaluation use.
5. Run the packager from the repository root:

   & ".\\benchmark\\.venv\\Scripts\\python.exe" ".\\benchmark\\prepare_custom_subset.py"

Do not commit private recordings or identifying metadata.
