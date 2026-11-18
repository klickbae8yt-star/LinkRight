
## 13 Oct 2026: never run the name scrubber on job text
The scrubber treats a first line like "Analyst-Risk Management" as a person's name and wipes those words from the whole text. Job posts hold no personal data. Only CV text goes through `scrub()`. Rebuild job text from the export, never from a second scrub. Found when the pilot JDs showed "[NAME]" in place of "Team Leader" and "Management".
