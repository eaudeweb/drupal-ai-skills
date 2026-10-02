#!/usr/bin/env python3
"""Worked example: Drupal hosting with production, dev/staging, shared database and backups.

Run from any directory:
    python3 example_infrastructure.py out.svg

Layout plan (x columns):
    50-470    Production panel (pipeline centred at x=260)
    590-850   Shared services column (database, backups), axis x=720
    970-1390  Dev/Staging panel (mirror of production, centred at x=1180)
    1430-1650 Side column (analytics)
Rows (y): header 0-80, actors 88-310, hosting boundary 340-1180, outside 1215+.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from edw_diagram import Diagram  # noqa: E402

d = Diagram(1700, 1330, "Infrastructure Diagram - Example Website", "Hosting, data flows and backup")

# Groups --------------------------------------------------------------------
d.boundary(30, 340, 1640, 840, ["Eau de Web", "Hetzner Nuremberg"])
d.boundary(590, 196, 260, 112, ["Microsoft Cloud"])
d.panel(50, 420, 420, 715, "Production Environment")
d.panel(970, 420, 420, 715, "Dev/Staging Environments")
d.panel(590, 828, 260, 162, "Managed Database Service", "High Availability Database Cluster")
d.panel(1430, 420, 220, 132, "Matomo Managed Instance")

# Actors and external services ----------------------------------------------
d.person(720, 88, "Visitor Browser")
d.card(640, 240, 160, 52, "Power BI", role="ext")

# Two identical stacks, side by side ----------------------------------------
for x0 in (50, 970):
    nx, cx = x0 + 70, x0 + 210
    d.card(nx, 475, 280, 60, "NGINX", "Reverse Proxy & SSL Termination", role="edge")
    d.card(nx, 575, 280, 60, "Varnish", "Cache dynamic content", role="edge")
    d.card(nx, 715, 280, 78, "NGINX", "Host", "Handle HTTP requests", role="app")
    d.card(nx, 873, 280, 78, "Drupal Instance", "PHP", "Generate dynamic pages", role="app")
    d.card(x0 + 30, 1031, 175, 78, "Redis", "Docker container", "Cache bins storage", role="svc")
    d.card(x0 + 215, 1031, 175, 78, "Apache Solr", "Docker Container", "Search engine for Drupal", role="svc")

    d.arrow([(cx, 535), (cx, 571)])
    d.arrow([(cx, 635), (cx, 711)], "HTTPS", "TCP/443", at=(cx + 10, 670), anchor="start")
    d.arrow([(cx, 793), (cx, 869)], "PHP/FCGI", "Unix socket", at=(cx + 10, 828), anchor="start")
    rc, sc = x0 + 117, x0 + 302
    d.arrow([(rc, 951), (rc, 1027)], "RESP", "TCP/6379", at=(rc + 8, 986), anchor="start")
    d.arrow([(sc, 951), (sc, 1027)], "Search queries", "HTTP/8983", at=(sc + 8, 986), anchor="start")

# Shared column -------------------------------------------------------------
d.database(720, 926, 150, 82, "MariaDB", "Drupal Database")
d.card(620, 1065, 200, 60, "On-Site Backup", role="node")
d.card(620, 1215, 200, 60, "Off-Site Backup", role="node")
d.card(1450, 470, 180, 72, "Matomo instance", None, "Visitor analytics", role="ext")

# Visitor traffic: leave the person card sideways, then drop into the target
d.arrow([(635, 130), (260, 130), (260, 471)])
d.arrow([(805, 148), (1180, 148), (1180, 471)])
d.arrow([(805, 112), (1540, 112), (1540, 416)], "Visitor actions", at=(1300, 104))

# Power BI integration runs up the free space in the shared column
d.arrow([(400, 754), (690, 754), (690, 292)], kind="integration")
d.arrow([(1040, 754), (750, 754), (750, 292)], kind="integration")

# Database access from both stacks, labels above the horizontal segment
d.arrow([(400, 912), (646, 912)], "SQL queries", "<PRIVATE-IP>:3306", at=(530, 884))
d.arrow([(1040, 912), (794, 912)], "SQL queries", "<PRIVATE-IP>:3306", at=(910, 884))

# Backups
d.arrow([(400, 936), (520, 936), (520, 1095), (616, 1095)], "Drupal files backup", "Restic",
        at=(528, 1030), anchor="start", kind="backup")
d.arrow([(720, 966), (720, 1061)], "Database backup", "Restic", at=(728, 1022), anchor="start", kind="backup")
d.arrow([(720, 1125), (720, 1211)], "Backup replication", at=(728, 1172), anchor="start", kind="backup")

d.legend(1240, 1205)

d.save(sys.argv[1] if len(sys.argv) > 1 else "example_infrastructure.svg")
