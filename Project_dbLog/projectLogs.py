#!/usr/bin/env python
# SQL REQUESTS FOR LOG PROJECT

import psycopg2
from datetime import datetime as d

if __name__ == '__main__':
    def popular_posts():
        """Return best 3 most popular posts of all time."""
        conn = psycopg2.connect("dbname=news user=vagrant")
        cur = conn.cursor()
        cur.execute("""
            SELECT articles.title, count(log) AS views FROM articles,
            log WHERE articles.slug = replace(log.path,'/article/','')
            GROUP BY articles.title ORDER BY views DESC LIMIT 3;
            """)
        return cur.fetchall()
        conn.close()

    def popular_authors():
        """Return most popular authors"""
        conn = psycopg2.connect("dbname=news user=vagrant")
        cur = conn.cursor()
        cur.execute("""
            SELECT authors.name, count(log) AS views FROM articles,
            authors, log WHERE articles.slug = replace(log.path
            ,'/article/','') AND articles.author = authors.id GROUP BY
            authors.name ORDER BY views DESC;
            """)
        return cur.fetchall()
        conn.close()

    def errors_insights():
        """Return erros over 1%"""
        conn = psycopg2.connect("dbname=news user=vagrant")
        cur = conn.cursor()
        cur.execute("""
           SELECT f.date, (s.errors/(f.requests*1.0))
           FROM (SELECT date(time), COUNT(*) AS requests FROM log
           GROUP BY date(time)) AS f, (SELECT date(time), COUNT(*)
           AS errors FROM log WHERE status = '404 NOT FOUND'
           GROUP BY date(time)) AS s WHERE f.date = s.date
           AND s.errors/(f.requests*1.0)>0.01;
           """)
        return cur.fetchall()
        conn.close()


posts = popular_posts()
authors = popular_authors()
errors = errors_insights()

print("\nThe most popular posts (TOP 3):")
for r in posts:
    print('"%s" \t- %s views' % (r[0], r[1]))

print("\nMost Popular Authors:")
for a in authors:
    print("%s \t- %s views" % (a[0], a[1]))

print("\nDays when errors is up to 1%:")
for e in errors:
    print("%s - %.2f%%" % (e[0].strftime("%B %d, %Y"), e[1]*100))
