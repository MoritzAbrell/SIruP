import sqlite3
import re
import configparser
import datetime
import random

info = "\033[1;34m[*]\033[0m"
error = "\033[1;31m[!]\033[0m"
loginit = "\n\033[0;36m====== LOG =====\033[0m"

defaulterror = ("{} an error occurred".format(error))

ini = "./config.ini"

config = configparser.ConfigParser()
config.read(ini)

udp_enable = config['UDP']['Enable']
udp_port = config['UDP']['Port']
udp_config = [udp_enable, udp_port]

tcp_enable = config['TCP']['Enable']
tcp_port = config['TCP']['Port']
tcp_config = [tcp_enable, tcp_port]

tls_enable = config['TLS']['Enable']
tls_port = config['TLS']['Port']
cert_path = config['TLS']['Certpath']
key_path = config['TLS']['Keypath']
tls_config = [tls_enable, tls_port, cert_path, key_path]

re_sip = re.compile("SIP", re.IGNORECASE)
re_method = re.compile("^[A-Z]+")
re_user = re.compile("sip:.*?@", re.IGNORECASE)
re_dst = re.compile("\s(.*?):")
re_dport = re.compile(":[0-9]{1,5}")

rtpport = config['RTP']['Port']
ipv4 = config['Server']['IPv4']
useragent = config['Server']['UserAgent']
nonce = config['Server']['Nonce']
realm = config['Server']['Realm'] 

db = config['Report']['Database']


def sip_user(user):
    user = re.findall(re_user, user)
    user = user[0]
    user = user.replace('sip:', '')
    user = user.replace('@', '')
    return user


def ts():
    ts = "[{}]".format(datetime.datetime.now().strftime("%H:%M:%S"))
    return ts


def tsdb():
    tsdb = datetime.datetime.now()    
    return tsdb


def db_conn():
    db_conn = sqlite3.connect(db)
    db_cursor = db_conn.cursor() 
    return db_conn, db_cursor


def response_200(protocol, dst, dport, branch, from_uri, to_uri, tag, callid,
        contact_uri, cseq):
    payload = f"""SIP/2.0 200 OK\r
Via: SIP/2.0/{protocol} {dst}:{dport};branch={branch}\r
From: {from_uri}\r
To: {to_uri};tag={tag}\r
Call-ID: {callid}\r
CSeq: {cseq}\r
Allow: INVITE,REGISTR,ACK,CANCEL,BYE,UPDATE,PRACK,INFO\r
Contact: {contact_uri}\r
Server: {useragent}\r
Content-Length: 0\r\n
"""
    return payload


def response_200_reg(protocol, dst, dport, branch, from_uri, to_uri, tag, callid,
                contact_uri, cseq, expires):
    payload = f"""SIP/2.0 200 OK\r
Via: SIP/2.0/{protocol} {dst}:{dport};branch={branch}\r
From: {from_uri}\r
To: {to_uri};tag={tag}\r
Call-ID: {callid}\r
CSeq: {cseq}\r
Expires: {expires}\r
Allow: INVITE,REGISTR,ACK,CANCEL,BYE,UPDATE,PRACK,INFO\r
Contact: {contact_uri}\r
Server: {useragent}\r
Content-Length: 0\r\n
"""
    return payload


def response_401(protocol, dst, dport, branch, from_uri, to_uri, tag, callid,
                contact_uri, cseq):
    payload = f"""SIP/2.0 401 Unauthorized\r
Via: SIP/2.0/{protocol} {dst}:{dport};branch={branch}\r
From: {from_uri};tag={tag}\r
To: {to_uri};tag={branch}\r
Call-ID: {callid}\r
CSeq: {cseq}\r
WWW-Authenticate: Digest realm="{realm}",nonce="{nonce}",algorithm=md5\r
Server: {useragent}\r
Content-Length: 0\r\n
"""
    return payload


def response_200_sdp(protocol, dst, dport, branch, from_uri, to_uri, tag, callid,
        contact_uri, cseq, sdp, sdp_len):
    payload = f"""SIP/2.0 200 OK\r
Via: SIP/2.0/{protocol} {dst}:{dport};branch={branch}\r
From: {from_uri}\r
To: {to_uri};tag={tag}\r
Call-ID: {callid}\r
CSeq: {cseq}\r
Allow: INVITE,ACK,CANCEL,BYE,UPDATE,PRACK,INFO\r
Content-Type: application/sdp\r
Contact: {contact_uri}\r
Server: {useragent}\r
Content-Length: {sdp_len}\r
\r
{sdp}"""
    return payload


def response_sdp():
    sdpsid = random.randint(00000000, 99999999)
    ssrc = random.randint(0000000000, 9999999999)
    sdp = f"""v=0\r
o=- {sdpsid} 1 IN IP4 {ipv4}\r
s=Asterisk\r
c=IN IP4 {ipv4}\r
t=0 0\r
m=audio {rtpport} RTP/AVP 8 101\r
a=rtpmap:8 PCMA/8000\r
a=rtpmap:101 telephone-event/8000\r
a=fmtp:101 0-15\r
a=ptime:20\r
a=ssrc:{ssrc}\r
a=sendrecv\r
"""
    sdp_len = len(sdp)
    return sdp, sdp_len
