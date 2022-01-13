import sys
import time
import sqlite3
import requests
import itertools
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


def calc_proto(df):

    df = df.groupby(df["PROTOCOL"],
                   as_index=False).size().sort_values(by=['size'], 
                   ascending=False)

    proto_bar = px.bar(df, x="PROTOCOL", y="size", 
                        title="Protocols", 
                        color="PROTOCOL", labels=dict(value="Count", 
                        variable="Protocol"))
    proto_bar = proto_bar.to_html(full_html=False, include_plotlyjs=False)

    proto_pie = px.pie(df, names="PROTOCOL", values="size", 
                        title="Protocols")
    proto_pie.update_traces(textinfo='percent+label')
    proto_pie = proto_pie.to_html(full_html=False, include_plotlyjs=False)

    return proto_bar, proto_pie


def calc_ua(df):
    df = df.groupby(df["USER AGENT"],
                   as_index=False).size().sort_values(by=['size'],
                   ascending=False)
    df_c = df
    try:
        df = df.head(5)
    except:
        pass

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
    try:
        df = df.head(10)
    except:
        pass

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
    try:
        df = df.head(10)
    except:
        pass

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
    try:
        df = df.head(10)
    except:
        pass

    ip_bar = px.bar(df, x="IP", y="size", 
                    title="Top 10 IPs", 
                    color="IP", labels=dict(value="Count", 
                    variable="IP"))
    ip_bar = ip_bar.to_html(full_html=False, include_plotlyjs=False)

    ip_pie = px.pie(df, names="IP", values="size", 
                    title="Top 10 IPs")
    ip_pie.update_traces(textinfo='percent+label')
    ip_pie = ip_pie.to_html(full_html=False, include_plotlyjs=False)

    ip_table = go.Figure(data=[go.Table(header=dict(values=['Count', 'IP']),
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


def calc_countries(countries):
    df = pd.DataFrame(countries)
    df = df.groupby(df[0],
                   as_index=False).size().sort_values(by=['size'],
                   ascending=False)
    df_c = df
    try:
        df = df.head(10)
    except:
        pass

    country_bar = px.bar(df, x=0, y="size", 
                    title="Top 10 Countries", 
                    color=0, labels=dict(value="Count", 
                    variable="Country"))
    country_bar = country_bar.to_html(full_html=False, include_plotlyjs=False)

    country_pie = px.pie(df, names=0, values="size", 
                    title="Top 10 Countries")
    country_pie.update_traces(textinfo='percent+label')
    country_pie = country_pie.to_html(full_html=False, include_plotlyjs=False)

    country_table = go.Figure(data=[go.Table(header=dict(values=['Count', 'Country']),
                         cells=dict(values=[df_c["size"], df_c[0]]))])
    country_table.update_layout(title="Countries")
    country_table = country_table.to_html(full_html=False, include_plotlyjs=False)
    
    return country_bar, country_pie, country_table


def country_analysis(un_ip):
    countries = []
    i = 1
    for ip in un_ip:
        print("\rRequest " + str(i) + " IP of " + str(len(un_ip)), end="", flush=True)
        i += 1
        ip = ''.join(ip)
        r = requests.get('http://ip-api.com/json/'+ip+'?fields=country')
        try:
            country = r.json()
            country = country["country"]
            countries.append(country)
        except:
            continue
        finally:
            time.sleep(2)
    
    return countries


def gen_report(method_bar, method_pie, method_table, ua_bar, ua_pie, ua_table,
               from_bar, from_pie, from_table, to_bar, to_pie, to_table, 
               stats_freq, days, ip_bar, ip_pie, ip_table, total_req, un_ip, 
               un_ua, un_from, un_to, countries_bar, countries_pie, 
               countries_table, un_countries, proto_bar, proto_pie):
    
    with open('./report/template.html','r') as file:
        template = file.read()
    
    template = template.replace("STATS_FREQ", stats_freq)
    template = template.replace("TOTAL_REQ", total_req)
    template = template.replace("TOTAL_RUNTIME", days)
    template = template.replace("UN_IP", un_ip)
    template = template.replace("UN_UA", un_ua)
    template = template.replace("UN_FROM", un_from)
    template = template.replace("UN_TO", un_to)

    template = template.replace("PROTO_BAR", proto_bar)
    template = template.replace("PROTO_PIE", proto_pie)

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
    if countries_bar == False:
        template = template.replace("COUNTRY_BAR", "N.A.")
    else:
        template = template.replace("COUNTRY_BAR", countries_bar)
        
    if countries_pie == False:
        template = template.replace("COUNTRY_PIE", "N.A.")
    else:
        template = template.replace("COUNTRY_PIE", countries_pie)

    if countries_table == False:
        template = template.replace("COUNTRY_TABLE", "N.A.")
    else:
        template = template.replace("COUNTRY_TABLE", countries_table)

    if un_countries == False:
        template = template.replace("UN_COUNTRY", "N.A.")
    else:
        template = template.replace("UN_COUNTRY", un_countries)
 
    args = parse_args()

    f = open((args.OUTFILE + ".html"), "w")
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
    
    try:
        total_req = cursor.execute("SELECT * FROM sip;")
        total_req = total_req.fetchall()
        total_req = str(len(total_req))
    except:
        print("Database is malformed. Try: sqlite3 " + args.DATABASE + " \".recover\" | sqlite3 <new database>")
        sys.exit(1)

    un_ip = cursor.execute("SELECT DISTINCT \"IP\" FROM sip;")
    un_ip = un_ip.fetchall()
    if args.FULL:
        countries = country_analysis(un_ip)
        un_countries = str(len(set(countries)))
        countries_bar, countries_pie, countries_table = calc_countries(countries)
    else:
        countries_bar = False
        countries_pie = False
        countries_table = False
        un_countries = False
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
    df.to_csv ((args.OUTFILE + ".csv"), index = False, header=True)

    conn.commit()
    conn.close()

    method_bar, method_pie, method_table = calc_methods(df)
    ua_bar, ua_pie, ua_table = calc_ua(df)
    from_bar, from_pie, from_table = calc_from(df)
    to_bar, to_pie, to_table = calc_to(df)
    ip_bar, ip_pie, ip_table = calc_ip(df)
    stats_freq, days = calc_stats(df)
    proto_bar, proto_pie = calc_proto(df)

    gen_report(method_bar, method_pie, method_table, ua_bar, ua_pie, ua_table,
               from_bar, from_pie, from_table, to_bar, to_pie, to_table, 
               stats_freq, days, ip_bar, ip_pie, ip_table, total_req, un_ip, 
               un_ua, un_from, un_to, countries_bar, countries_pie, 
               countries_table, un_countries, proto_bar, proto_pie)
