import sys
import sqlite3
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from report.args import parse_args


def calc_methods(df):

    df = df.groupby(df["METHOD"],
                   as_index=False).size().sort_values(by=['size'], 
                   ascending=False)

    method_bar = px.bar(df, x="METHOD", y="size", 
                        title="Total of SIP Request Methods", 
                        color="METHOD", labels=dict(value="Count", 
                        variable="Method"))
    method_bar = method_bar.to_html(full_html=False, include_plotlyjs=False)

    method_pie = px.pie(df, names="METHOD", values="size", 
                        title="Total of SIP Request Methods")
    method_pie.update_traces(textinfo='percent+label')
    method_pie = method_pie.to_html(full_html=False, include_plotlyjs=False)

    method_table = go.Figure(data=[go.Table(header=dict(values=['Count', 'Method']),
                             cells=dict(values=[df["size"], df["METHOD"]]))])
    method_table.update_layout(title="Methods")
    method_table = method_table.to_html(full_html=False, include_plotlyjs=False)
    
    return method_bar, method_pie, method_table


def calc_ua(df):
    df = df.groupby(df["USER AGENT"],
                   as_index=False).size().sort_values(by=['size'],
                   ascending=False)
    df_c = df
    df = df.head(5)

    ua_bar = px.bar(df, x="USER AGENT", y="size", 
                    title="Top 5 User Agents", 
                    color="USER AGENT", labels=dict(value="Count", 
                    variable="UserAgents"))
    ua_bar = ua_bar.to_html(full_html=False, include_plotlyjs=False)

    ua_pie = px.pie(df, names="USER AGENT", values="size", 
                    title="Top 5 User Agents")
    ua_pie.update_traces(textinfo='percent+label')
    ua_pie = ua_pie.to_html(full_html=False, include_plotlyjs=False)

    ua_table = go.Figure(data=[go.Table(header=dict(values=['Count', 'UserAgent']),
                         cells=dict(values=[df_c["size"], df_c["USER AGENT"]]))])
    ua_table.update_layout(title="User Agents")
    ua_table = ua_table.to_html(full_html=False, include_plotlyjs=False)
    
    return ua_bar, ua_pie, ua_table


def calc_from(df):
    df = df.groupby(df["FROM USER"],
                   as_index=False).size().sort_values(by=['size'],
                   ascending=False)
    df_c = df
    df = df.head(10)

    from_bar = px.bar(df, x="FROM USER", y="size", 
                      title="Top 10 From Users", 
                      color="FROM USER", labels=dict(value="Count", 
                      variable="From"))
    from_bar = from_bar.to_html(full_html=False, include_plotlyjs=False)

    from_pie = px.pie(df, names="FROM USER", values="size", 
                      title="Top 10 From Users")
    from_pie.update_traces(textinfo='percent+label')
    from_pie = from_pie.to_html(full_html=False, include_plotlyjs=False)

    from_table = go.Figure(data=[go.Table(header=dict(values=['Count', 'From']),
                         cells=dict(values=[df_c["size"], df_c["FROM USER"]]))])
    from_table.update_layout(title="From Users")
    from_table = from_table.to_html(full_html=False, include_plotlyjs=False)
    
    return from_bar, from_pie, from_table


def calc_to(df):
    df = df.groupby(df["TO USER"],
                   as_index=False).size().sort_values(by=['size'],
                   ascending=False)
    df_c = df
    df = df.head(10)

    to_bar = px.bar(df, x="TO USER", y="size", 
                    title="Top 10 To Users", 
                    color="TO USER", labels=dict(value="Count", 
                    variable="To"))
    to_bar = to_bar.to_html(full_html=False, include_plotlyjs=False)

    to_pie = px.pie(df, names="TO USER", values="size", 
                    title="Top 10 To Users")
    to_pie.update_traces(textinfo='percent+label')
    to_pie = to_pie.to_html(full_html=False, include_plotlyjs=False)

    to_table = go.Figure(data=[go.Table(header=dict(values=['Count', 'To']),
                         cells=dict(values=[df_c["size"], df_c["TO USER"]]))])
    to_table.update_layout(title="To Users")
    to_table = to_table.to_html(full_html=False, include_plotlyjs=False)
    
    return to_bar, to_pie, to_table


def calc_ip(df):
    df = df.groupby(df["IP"],
                   as_index=False).size().sort_values(by=['size'],
                   ascending=False)
    df_c = df
    df = df.head(10)

    ip_bar = px.bar(df, x="IP", y="size", 
                    title="Top 10 IPs", 
                    color="IP", labels=dict(value="Count", 
                    variable="IP"))
    ip_bar = ip_bar.to_html(full_html=False, include_plotlyjs=False)

    ip_pie = px.pie(df, names="IP", values="size", 
                    title="Top 10 IPs")
    ip_pie.update_traces(textinfo='percent+label')
    ip_pie = ip_pie.to_html(full_html=False, include_plotlyjs=False)

    ip_table = go.Figure(data=[go.Table(header=dict(values=['Count', 'To']),
                         cells=dict(values=[df_c["size"], df_c["IP"]]))])
    ip_table.update_layout(title="IP Addresses")
    ip_table = ip_table.to_html(full_html=False, include_plotlyjs=False)
    
    return ip_bar, ip_pie, ip_table


def calc_stats(df):
    df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'], errors='coerce')
    
    days = df["TIMESTAMP"].iloc[-1] - df["TIMESTAMP"].iloc[0]
    days = days / np.timedelta64(1, 'D')
    days = round(days, 1)
    days = str(days)
    
    df = df.groupby(pd.Grouper(key='TIMESTAMP', freq='60min')).count()


    stats_freq = go.Figure()
    stats_freq = stats_freq.add_trace(go.Scatter(x=df.index, y=df["IP"],  mode='lines'))
    stats_freq.update_layout(title="Packets per hour")
    stats_freq = stats_freq.to_html(full_html=False, include_plotlyjs=False)

    return stats_freq, days



def gen_report(method_bar, method_pie, method_table, ua_bar, ua_pie, ua_table,
               from_bar, from_pie, from_table, to_bar, to_pie, to_table, 
               stats_freq, days, ip_bar, ip_pie, ip_table, total_req, un_ip, 
               un_ua, un_from, un_to):
    
    with open('./report/template.html','r') as file:
        template = file.read()
    
    template = template.replace("STATS_FREQ", stats_freq)
    template = template.replace("TOTAL_REQ", total_req)
    template = template.replace("TOTAL_RUNTIME", days)
    template = template.replace("UN_IP", un_ip)
    template = template.replace("UN_UA", un_ua)
    template = template.replace("UN_FROM", un_from)
    template = template.replace("UN_TO", un_to)

    template = template.replace("UA_BAR", ua_bar)
    template = template.replace("UA_PIE", ua_pie)
    template = template.replace("UA_TABLE", ua_table)
    
    template = template.replace("METHOD_BAR", method_bar)
    template = template.replace("METHOD_PIE", method_pie)
    template = template.replace("METHOD_TABLE", method_table)

    template = template.replace("FROM_BAR", from_bar)
    template = template.replace("FROM_PIE", from_pie)
    template = template.replace("FROM_TABLE", from_table)

    template = template.replace("TO_BAR", to_bar)
    template = template.replace("TO_PIE", to_pie)
    template = template.replace("TO_TABLE", to_table)

    template = template.replace("IP_BAR", ip_bar)
    template = template.replace("IP_PIE", ip_pie)
    template = template.replace("IP_TABLE", ip_table)
 
    args = parse_args()

    f = open(args.OUTFILE, "w")
    f.write(template)
    f.close()


def db_conn(db):
    db_conn = sqlite3.connect(db)
    db_cursor = db_conn.cursor() 
    return db_conn, db_cursor


def init():
    args = parse_args()
    
    db = args.DATABASE
    conn, cursor = db_conn(db)

    total_req = cursor.execute("SELECT * FROM sip;")
    total_req = total_req.fetchall()
    total_req = str(len(total_req))

    un_ip = cursor.execute("SELECT DISTINCT \"IP\" FROM sip;")
    un_ip = un_ip.fetchall()
    un_ip = str(len(un_ip))

    un_ua = cursor.execute("SELECT DISTINCT \"USER AGENT\" FROM sip;")
    un_ua = un_ua.fetchall()
    un_ua = str(len(un_ua))

    un_from = cursor.execute("SELECT DISTINCT \"FROM USER\" FROM sip;")
    un_from = un_from.fetchall()
    un_from = str(len(un_from))

    un_to = cursor.execute("SELECT DISTINCT \"TO USER\" FROM sip;")
    un_to = un_to.fetchall()
    un_to = str(len(un_to))

    df = pd.read_sql_query("SELECT * FROM sip;", conn)

    conn.commit()
    conn.close()

    method_bar, method_pie, method_table = calc_methods(df)
    ua_bar, ua_pie, ua_table = calc_ua(df)
    from_bar, from_pie, from_table = calc_from(df)
    to_bar, to_pie, to_table = calc_to(df)
    ip_bar, ip_pie, ip_table = calc_ip(df)
    stats_freq, days = calc_stats(df)

    gen_report(method_bar, method_pie, method_table, ua_bar, ua_pie, ua_table,
               from_bar, from_pie, from_table, to_bar, to_pie, to_table, 
               stats_freq, days, ip_bar, ip_pie, ip_table, total_req, un_ip, 
               un_ua, un_from, un_to)
