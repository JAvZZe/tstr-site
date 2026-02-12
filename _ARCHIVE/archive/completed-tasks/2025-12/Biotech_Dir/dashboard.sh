#!/bin/bash
DB_PATH=~/memory/db/tstr.db

clear
echo "========================================"
echo "   TSTR.site | PROVIDER DATABASE      "
echo "========================================"
echo ""

sqlite3 $DB_PATH <<SQL
.headers on
.mode box

SELECT 'TOTAL LEADS' as Metric, COUNT(*) as Value FROM providers;

.print ""
.print "--- Breakdown by Category ---"
SELECT category, COUNT(*) as Count 
FROM providers 
GROUP BY category 
ORDER BY Count DESC;

.print ""
.print "--- Pipeline Status (The Funnel) ---"
SELECT status, tier, COUNT(*) as Count 
FROM providers 
GROUP BY status, tier 
ORDER BY tier DESC;
SQL

echo ""
echo "========================================"
echo "Timestamp: $(date)"
