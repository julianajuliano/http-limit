class IpUidProvider():
    def __init__(self):
        pass
    
    def get_uid(self, request):
        if request.headers.getlist("X-Forwarded-For"):
         ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip = request.remote_addr
        return ip