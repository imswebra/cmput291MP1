#!/bin/sh
pandoc -s -V geometry:margin=0.75in -o Report.pdf Report.md -V urlcolor=cyan
