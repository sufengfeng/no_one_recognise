import socket, select, time
from xml.dom.minidom import Document

http_mimes = {
	"Host": "${ip}",
	"Connection": "keep-alive",
	"Content-Length": "${con_len}",
	"Accept": "text/javascript, text/html, application/xml, text/xml, */*",
	"X-Requested-With": "XMLHttpRequest",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
	"Content-type": "application/x-www-form-urlencoded",
	"Origin": "http://${ip}",
	"Referer": "http://${ip}/",
	"Accept-Encoding": "gzip, deflate",
	"Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
	"Cookie": "DHLangCookie30=SimpChinese; is_First_Login=0; ipc_${ip}_webLanguage=zh_cn; ipc_${ip}_KeepScale=0; ipc_${ip}_username=admin; ipc_${ip}_password=E10ADC3949BA59ABBE56E057F20F883E"
	}

HEADER_RECVING = 0
BODY_RECVING = 1

def gen_xml(cmd):
	doc = Document()
	soap_envelope = doc.createElement("soap:Envelope")
	soap_envelope.setAttribute("xmlns:soap", "http://www.w3.org/2001/12/soap-envelope")
	doc.appendChild(soap_envelope)
	soap_header = doc.createElement("soap:Header")
	soap_envelope.appendChild(soap_header)
	userid = doc.createElement("userid")
	userid.appendChild(doc.createTextNode("52851dbd7918bbae"))
	soap_header.appendChild(userid)
	passwd = doc.createElement("passwd")
	passwd.appendChild(doc.createTextNode("a17faccd02661e4c"))
	soap_header.appendChild(passwd)
	soap_body = doc.createElement("soap:Body")
	xml = doc.createElement("xml")
	soap_body.appendChild(xml)
	cmd_node = doc.createElement("cmd")
	xml.appendChild(cmd_node)
	cmd_node.appendChild(doc.createTextNode(cmd))
	soap_envelope.appendChild(soap_body)
	return doc.toprettyxml(indent="\t", newl="\n", encoding="utf-8")

def parse_header(header):
	header_info = {}
	lines = header.split("\r\n")
	fline_data = lines[0].split(" ")
	header_info["CODE"], header_info["STATUS"] = int(fline_data[1]), fline_data[2]
	for line in lines[1:]:
		if len(line) == 0:
			break
		colon = line.index(":")
		name = line[:colon]
		value = line[colon + 1:].lstrip()
		header_info[name] = value
	return header_info

def send_cmd(ip, cmd):
	ret = (-1, "invalid")
	firstline = b"POST /setPTZCmd HTTP/1.1\r\n"
	body = gen_xml(cmd)
	header = []
	for name in http_mimes:
		value = http_mimes[name]
		value = value.replace("${ip}", ip)
		value = value.replace("${con_len}", "%d"%(len(body)))
		header.append("%s: %s"%(name, value))
	header = firstline + ("\r\n".join(header)).encode() + b"\r\n"
	package = header + b"\r\n" + body

	new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	new_sock.connect((ip, 80))
	new_sock.sendall(package)

	response = b""
	recv_state = HEADER_RECVING
	header_info = {}
	while True:
		if recv_state == HEADER_RECVING:
			response += new_sock.recv(1)
			if response.endswith(b"\r\n\r\n"):
				recv_state = BODY_RECVING
				header_info = parse_header(response.decode())
		if recv_state == BODY_RECVING:
			con_len = int(header_info["Content-Length"])
			if con_len != 0:
				new_sock.recv(con_len)
			ret = (header_info["CODE"], header_info["STATUS"])
			break
	new_sock.close()
	return ret

def zoomstop(ip):
	return send_cmd(ip, "stop")

def zoomtele(ip, sec=-1):
	ret = send_cmd(ip, "zoomtele")
	if ret[0] != 200 or ret[1] != "OK":
		return ret
	if sec != -1:
		time.sleep(sec)
		ret = zoomstop(ip)
	return ret

def zoomwide(ip, sec=-1):
	ret = send_cmd(ip, "zoomwide")
	if ret[0] != 200 or ret[1] != "OK":
		return ret
	if sec != -1:
		time.sleep(sec)
		ret = zoomstop(ip)
	return ret

class zoomcam:
	def __init__(self, ip):
		self.ip = ip

	def zoomstop(self):
		return zoomstop(self.ip)

	def zoomtele(self, sec=-1):
		return zoomtele(self.ip, sec)

	def zoomwide(self, sec=-1):
		return zoomwide(self.ip, sec)

# Demo
if __name__ == "__main__":
	ip = "192.168.3.166"
	flag=False
	value = 0
	cam = zoomcam(ip)
	while True:
		# use as function
		# print(zoomtele(ip))
		# time.sleep(1)
		# print(zoomstop(ip))
		# time.sleep(1)


		# use as object

		if flag:
			print(cam.zoomwide(1)) # auto stop by set time
		else:
			print(cam.zoomtele(1))  # auto stop by set time
		time.sleep(1)


