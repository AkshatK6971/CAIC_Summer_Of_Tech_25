#!/bin/bash

timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
report="system_report_$timestamp.txt"

echo "System Uptime:" > "$report"
uptime >> "$report"

echo -e "\nDisk Usage of Home Directory:" >> "$report"
du -sh ~ >> "$report"

echo -e "\nNumber of Running Processes:" >> "$report"
ps aux | wc -l >> "$report"

echo -e "\nCurrent Network Connections:" >> "$report"
netstat -tunapl >> "$report" 2>/dev/null || ss -tunapl >> "$report"

echo "Report saved to $report"