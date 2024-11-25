cp932.py is a Python script that creates a compressed CP932-to-Unicode lookup
table, in the form of a C header file.

Typical usage:

  ./cp932.py CP932.TXT

This creates a file named cp932data.h.

Caution: Additional logic is needed to handle single-byte characters, and to
handle different variants of "code page 932" and "Shift-JIS".

CP932.TXT was retrieved from
  https://www.unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WINDOWS/CP932.TXT

The CP932.TXT file might be subject to the terms of use in UNICODE LICENSE V3,
reproduced in LICENSE-UNICODE.txt.

LICENSE-UNICODE.txt was retrieved from
  https://www.unicode.org/license.txt
