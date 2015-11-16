REM this is run as a task on thurios. to keep the summary files up to date

REM Concatenate the summary files for the hungry donkey task 
python concat_csv.py -o HDT_summary.iqdat -p HDT_summary_*.iqdat -w "//wcs/wtp_common/data/RDoC Computer Tasks/Inquisit tasks - USE ME/HungryDonkeyTask"

REM Concatenate the summary files for PSAP
python concat_csv.py -o PSAP_summary.iqdat -p PSAP_summary_*.iqdat -w "//wcs/wtp_common/data/RDoC Computer Tasks/Inquisit tasks - USE ME/PSAP"
