import requests

"""
Class;

    ____Attributes___:
        domain: name of inputed url domain
        forbidden:  lst of for pathways that should not be accessed on the current website. (respects scraping regulations)

    ____Methods___:
        can_follow_link:
        make_get_request:
        parse_robots:


"""
class RequestGuard:

    #________Instantiates protocals for webcrawler object to abide while recursing through web. 
    def __init__(self, url):
        #splits/ saves domain to variable
        domain = url.split("//")[1].split("/")[0] 
        
        self.domain = domain
        self.forbidden = self.parse_robots()


    #____Determines whether input args url is contained within the specifed traversing domain.( Within was BYU domain)
    def can_follow_link(self, url):

        #checks if  domain is complete, and it segemnted part is accutrate in mathching the full url.
        if (not url.startswith(f"https://{self.domain}")):
            return False
        
        path = url.split(f"https://{self.domain}", 1) [1]


        # checks that the pathway, "what we are trying to access on domain is somthing we can actually acesss"
        #compared current path to list of forbidden paths, and logics accodingly. 
        for forbidden_path in self.forbidden:
            if (path.startswith(forbidden_path)):
                return False
        return True 
            
            

    #Using
    def make_get_request(self, url, use_stream= False): 

        if (self.can_follow_link(url)):
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








        






        













