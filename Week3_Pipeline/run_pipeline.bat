@echo off
REM run_pipeline.bat
REM Wrapper so Windows Task Scheduler can run the pipeline unattended.
REM Change the path below to match wherever your Pipeline folder actually is.

cd /d "C:\Users\pc\Desktop\Application\Datacamp_Cert\30_Days_Challenge\Day_15\Pipeline"
python run_pipeline.py