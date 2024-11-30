cp932.py is a Python script that creates a compressed CP932-to-Unicode lookup
table, in the form of a C header file.

Typical usage:

  ./cp932.py sjis-0213-2004-std.txt

This creates a file named cp932data.h.

Caution: Additional logic is needed to handle single-byte characters, codes
that map to multiple Unicode codepoints, and to handle different variants of
"code page 932" and "Shift-JIS".

The sjis-0213-2004-std.txt file was retrieved from
  https://x0213.org/codetable/sjis-0213-2004-std.txt

This script was originally designed to work with CP932.TXT from
  https://www.unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WINDOWS/CP932.TXT
