#!/usr/bin/env python3

# A script to create a compressed CP932 (Shift-JIS) lookup table,
# for use with Deark.
#
# By Jason Summers, 2024.
#
# This file is public domain.
#
# The source file it reads (e.g. CP932.TXT), and any output files it
# generates, might be subject to third-party copyrights.

import sys
import re
import zlib

class context:
    def __init__(ctx):
        ctx.debugmode = False
        ctx.debugmode2 = False
        ctx.re1 = re.compile(r'([0-9a-zA-Z]+)[ \t]+([0-9a-zA-Z]+)[ \t]')

def read_mapping_file(ctx):
    for line in ctx.inf:
        m1 = ctx.re1.match(line)
        if m1:
            w1 = int(m1.group(1), base=0)
            w2 = int(m1.group(2), base=0)
            ctx.mapping[w1] = w2

def mapping_to_uncblob(ctx):
    ctx.uncblob = bytearray(65536)
    for i in range(32768):
        ctx.uncblob[i] = ctx.mapping[32768+i] >> 8
        ctx.uncblob[32768+i] = ctx.mapping[32768+i] & 0xff

def write_c_file(ctx, outfn, is_compressed):
    if is_compressed:
        blob = ctx.cmprblob
    else:
        blob = ctx.uncblob

    outf = open(outfn, "w", encoding='utf8')

    if is_compressed:
        outf.write("// This file is part of Deark.\n\n")

    outf.write("// This is a generated file. Do not edit.\n\n")

    if is_compressed:
        outf.write("// This data is zlib-compressed. After decompression,\n" \
            "// it is a CP932-to-Unicode lookup table for the double-byte\n" \
            "// CP932 characters, from 0x8000 to 0xffff.\n" \
            "// For compressibility reasons, first it has 32768 high bytes,\n" \
            "// then 32768 low bytes.\n" \
            "// For more information, see the \"deark-extras\" project\n" \
            "// listed in the main Deark readme file.\n\n")

    outf.write("#define DE_CP932DATA_LEN %d\n" % (len(blob)))
    outf.write("static const u8 de_cp932data[DE_CP932DATA_LEN] = {")
    for i in range(0, len(blob)):
        if i!=0:
            outf.write(",")
        if (i%16)==0:
            outf.write("\n\t")

        if not is_compressed:
            if i==0:
                outf.write("// high bytes\n\t")
            elif i==32768:
                outf.write("// low bytes\n\t")

        outf.write(str(blob[i]))

    outf.write("\n};\n")
    outf.close()

def write_unc_data_file(ctx, outfn):
    outf = open(outfn, "wb")
    outf.write(ctx.uncblob)
    outf.close()

def compress_mapping(ctx):
    ctx.cmprblob = zlib.compress(ctx.uncblob, level=9)

def write_cmpr_data_file(ctx, outfn):
    outf = open(outfn, "wb")
    outf.write(ctx.cmprblob)
    outf.close()

def dump_mapping(ctx):
    for i in range(65536):
        print("item 0x%x 0x%x" % (i, ctx.mapping[i]))

def main():
    ctx = context()

    if len(sys.argv) != 2:
        print("Need an input file")
        return

    ctx.fn = sys.argv[1]

    ctx.mapping = [0] * 65536

    ctx.inf = open(ctx.fn, "r", encoding='utf8', newline='\n')
    read_mapping_file(ctx)
    ctx.inf.close

    if ctx.debugmode2:
        dump_mapping(ctx)

    mapping_to_uncblob(ctx)

    if ctx.debugmode:
        write_unc_data_file(ctx, "cp932data_u.dat")

    if ctx.debugmode:
        write_c_file(ctx, "cp932data_u.h", False)

    compress_mapping(ctx)

    if ctx.debugmode:
        write_cmpr_data_file(ctx, "cp932data_c.dat")

    write_c_file(ctx, "cp932data.h", True)

main()
