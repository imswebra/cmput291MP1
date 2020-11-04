#/bin/sh
./gen-report-pdf.sh
rm -f prjcode.tar.gz
tar -czf prjcode.tar.gz sql/ tests/database_test.py tests/utils_test.py README.txt Report.pdf database.py logged_in.py login.py main.py utils.py
