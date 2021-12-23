import sqlite3
from pathlib import Path
from sirup import var


def log(ip):
    logcontent = "{} {} IP: {}".format(var.info, var.ts(), ip)
    print(logcontent, end='\r')


def escape(string):
    try:
        escaped_string = string.replace('\"', '')
        return escaped_string
    except:
        return string


def db_init():
    db_file = Path(var.db)
    
    if db_file.is_file():
        print("{} {} Database already exists".format(var.error, var.ts()))
        delete_db = input("{} {} Do you want to delte it [y/N]".format(var.info, var.ts()))
        if delete_db == "y":
            db_file.unlink()
            conn, cursor = var.db_conn()
        else:
            sys.exit(1)
    else:
        conn, cursor = var.db_conn()

    config_table = """CREATE TABLE "config" (
    "ID" INTEGER NOT NULL UNIQUE,
    "START TIME" TEXT,
    "UDP" TEXT,
    "UDP PORT" INTEGER,
    "TCP" TEXT,
    "TCP PORT" INTEGER,
    "TLS" TEXT,
    "TLS PORT" INTEGER,
    "USER AGENT" TEXT,
    "REALM" TEXT,
    "NONCE" TEXT,
    "RTP PORT" INTEGER,
    PRIMARY KEY("ID" AUTOINCREMENT)
);"""

    sip_table = """CREATE TABLE "sip" (
    "IP" TEXT,
    "PORT" INTEGER,
    "PROTOCOL" TEXT,
    "TIMESTAMP" TEXT,
    "METHOD" TEXT,
    "USER AGENT" TEXT,
    "FROM USER" TEXT,
    "TO USER" TEXT,
    "MESSAGE" TEXT
);"""

    insert_config = f"""INSERT INTO "config" (
    "ID",
    "START TIME",
    "UDP",
    "UDP PORT",
    "TCP",
    "TCP PORT",
    "TLS",
    "TLS PORT",
    "USER AGENT",
    "REALM",
    "NONCE",
    "RTP PORT"
) VALUES (
    1,
    "{escape(var.tsdb())}",
    "{escape(var.udp_enable)}",
    {escape(var.udp_port)},
    "{escape(var.tcp_enable)}",
    {escape(var.tcp_port)},
    "{escape(var.tls_enable)}",
    {escape(var.tls_port)},
    "{escape(var.useragent)}",
    "{escape(var.realm)}",
    "{escape(var.nonce)}",
    {escape(var.rtpport)}
);"""

    cursor.execute(config_table)
    cursor.execute(sip_table)
    cursor.execute(insert_config)
    conn.commit()
    conn.close()


def log_msg(ip, port, protocol, data, log_from, log_to, method, 
            log_useragent):
    conn, cursor = var.db_conn()

    if log_useragent is None:
        log_useragent = "None"

    if log_from is None:
        log_from = "None"
    else:
        log_from = var.sip_user(log_from)

    if log_to is None:
        log_to = "None"
    else:
        log_to = var.sip_user(log_to)

    data = data.decode("UTF-8")
    
    insert_msg = f"""INSERT INTO "sip" (
    "IP",
    "PORT",
    "PROTOCOL",
    "TIMESTAMP",
    "METHOD",
    "USER AGENT",
    "FROM USER",
    "TO USER",
    "MESSAGE"
) VALUES (
    "{escape(ip)}",
    "{escape(port)}",
    "{escape(protocol)}",
    "{escape(var.tsdb())}",
    "{escape(method)}",
    "{escape(log_useragent)}",
    "{escape(log_from)}",
    "{escape(log_to)}",
    "{escape(data)}"
);"""

    cursor.execute(insert_msg)
    conn.commit()
    conn.close()
