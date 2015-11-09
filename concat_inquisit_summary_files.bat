REM this is run as a task on thurios. to keep the summary files up to date
REM Concatenate the summary files for the hungry donkey task 
python concat_csv.py -o HDT_summary.tsv -p HDT_summary_*.iqdat -w "//wcs/wtp_common/data/RDoC Computer Tasks/Inquisit tasks - USE ME/HungryDonkeyTask"
