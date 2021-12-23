import re
from sirup import var, logger
from kiss_headers import parse_it


def handle_request(method, data, client_address, proto):
    protocol = proto.upper()

    header = parse_it(data)

    if header.has("via"):
        dst = re.findall(var.re_dst, repr(header.via[0]))
        dport = re.findall(var.re_dport, repr(header.via[0]))
        if len(dst) <= 1:
            dport = str(client_address[1])
            dst = client_address[0]
        else:
            dst = dst[0]
            dport = dport[0][1:]
    else:
        dport = str(client_address[1])
        dst = client_address[0]

    if header.via.has("branch"):
        branch = header.via.branch
    else:
        branch = "z9hG4bK-1717536410"

    if header.has("from"):
        from_uri = header.from_[0]
        log_from = from_uri
    else:
        from_uri = "{}:{}".format(dst, dport)
        log_from = None

    if header.has("to"):
        to_uri = header.to[0]
        log_to = to_uri
    else:
        to_uri = from_uri
        log_to = None

    if header.from_.has("tag"):
        tag = header.from_.tag
    else:
        tag = "1337"

    if header.has("Call_ID"):
        callid = header.Call_ID[0]
    else:
        callid = "13371337"

    if header.has("contact"):
        contact_uri = header.contact[0]
    else:
        contact_uri = to_uri

    if header.has("Cseq"):
        cseq = header.cseq[0]
    else:
        cseq = "1 {}".format(method.upper())

    if header.has("User-Agent"):
        log_useragent = header.User_Agent[0]
    elif header.has("Server"):
        log_useragent = header.Server[0]
    else:
        log_useragent = None

    if method == "OPTIONS":
        payload = var.response_200(protocol, dst, dport, branch, from_uri,
                                   to_uri, tag, callid, contact_uri, cseq)
    elif method == "REGISTER":
        if header.has("Authorization"):
            if header.has("Expires"):
                expires = header.expires[0]
            else:
                expires = "600"
            payload = var.response_200_reg(protocol, dst, dport, branch,
                                           from_uri, to_uri, tag, callid,
                                           contact_uri, cseq, expires)
        else:
            payload = var.response_401(protocol, dst, dport, branch, from_uri,
                                       to_uri, tag, callid, contact_uri,
                                       cseq)

    elif method == "INVITE":
        if header.has("Authorization"):
            sdp, sdp_len = var.response_sdp()
            payload = var.response_200_sdp(protocol, dst, dport, branch,
                                           from_uri, to_uri, tag, callid,
                                           contact_uri, cseq, sdp,
                                           sdp_len)
        else:
            payload = var.response_401(protocol, dst, dport, branch, from_uri,
                                       to_uri, tag, callid, contact_uri,
                                       cseq)

    logger.log_msg(client_address[0], client_address[1], protocol, data, 
                   log_from, log_to, method, log_useragent)

    if payload is None:
        return None
    else:
        return payload


def handler(client_address, data, proto):
    try:
        if re.search(var.re_sip, data.decode("UTF-8")):
            method = re.findall(var.re_method, data.decode("UTF-8"))
            method = method[0]
        else:
            return None
    except:
        return None

    try:
        payload = handle_request(method, data, client_address, proto)
        if payload is None:
            return None
        else:
            return payload.encode()
    except:
        return None
