-- Testing the queries here before implementing them

select p.pid as pid, count(*) as keywordCount
from posts p join tags t on p.pid = t.pid
where lower(tag) in ('apple', 'pear')
group by p.pid;


.print "Vote Count"
