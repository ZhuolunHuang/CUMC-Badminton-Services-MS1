-- Get available sessions info for user 1
SELECT t1.*, (CASE WHEN t2.sessionid IS NULL THEN FALSE ELSE TRUE END) is_registered
FROM
(
SELECT s.sessionid, begintime, endtime, s.notes, s.capacity, count(1) enrolled
FROM ms2_db.sessions s
LEFT JOIN ms2_db.waitlist w
ON s.sessionid = w.sessionid
GROUP BY s.sessionid, begintime, endtime, s.notes, s.capacity) t1
LEFT JOIN
(
SELECT distinct s.sessionid
FROM ms2_db.sessions s
LEFT JOIN ms2_db.waitlist w
ON s.sessionid = w.sessionid
WHERE w.userid = 1) t2
ON t1.sessionid = t2.sessionid;
