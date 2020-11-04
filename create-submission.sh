#/bin/sh
output_file=prjcode.tgz
./gen-report-pdf.sh
rm -f $output_file
tar -czf $output_file sql/ tests/database_test.py tests/utils_test.py README.txt Report.pdf database.py logged_in.py login.py main.py utils.py
