```
PGPASSWORD=nucracker psql -h nusocialgraph-production.cpc7uj1yh3bv.us-east-1.rds.amazonaws.com -U nusocialgraph nusocialgraph

cat latest.dump.txt | PGPASSWORD=nucracker psql -h nusocialgraph-production.cpc7uj1yh3bv.us-east-1.rds.amazonaws.com -U nusocialgraph nusocialgraph
```