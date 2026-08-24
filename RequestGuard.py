import requests

class RequestGuard:


    def __init__(self, url):
    
        domain = url.split("//")[1].split("/")[0] 

        self.domain = domain
        self.forbidden = self.parse_robots()


    def can_follow_link(self, url):

        if not url.startswith(f"https://{self.domain}"):
            return False
        
        path = url.split(f"https://{self.domain}", 1)[1]

        for forbidden_path in self.forbidden:
            if path.startswith(forbidden_path):
                return False
        return True 
            
            

    def make_get_request(self, url, use_stream= False): 

        if self.can_follow_link(url):
            return requests.get(url, stream= use_stream)
        else:
            return None


    
    def parse_robots(self):

        response = requests.get(f"https://{self.domain}/robots.txt")
        lines = response.text.splitlines()

        excluded_paths = []  # Initialize list to store paths

        for line in lines:
            if line.startswith("Disallow:"):
            
                parts = line.split(':', 1)
                path = parts[1].strip()
                excluded_paths.append(path)
            else:
                pass
        return excluded_paths








        






        













