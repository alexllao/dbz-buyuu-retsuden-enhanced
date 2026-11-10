R9 native pipeline, 10 November 2026.
Run from the project root; working dependencies and R6/R7 pipeline resources are required.
Approved parent ROM: work/combo-startup/candidate.bin. ROM is not included.
Build/import resources with prepare-namek-r9-assets.py and build.py, then integrate.py.
After every changed ROM, use a fresh state directory consistently in preparation/recording/verification.
prepare-scenes.py refuses to reuse an existing seed silently.
record.py captures real ROM output; package.py only scales by integer2x and concatenates.
No video or ROM is published. See docs/namek-native-r9.md for scope and pending ground report.
