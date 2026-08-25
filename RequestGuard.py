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
            
            

    #Using full url to pull html,
    # use_stream varible that defines how the information should be 
    # pulled( whehter regular html or images)
    #utulizing attribute of requests get() method. 
    def make_get_request(self, url, use_stream= False): 

        if (self.can_follow_link(url)):
            return requests.get(url, stream= use_stream)
        else:
            return None



    #__________retriving the robot.txt file------> list of fobbiden actions/ pathways
    #that should not be preformed on the website. 
    def parse_robots(self):

        # retrives data from website, saves as obj
        response = requests.get(f"https://{self.domain}/robots.txt")

        #saves text version from responsed object
        lines = response.text.splitlines()


        #creates list object to save paths that should be exluded. 
        # To use a refrence for what not to crawel down. 
        excluded_paths = []  


        """
        Common example of Robot.txt file
        
        # Allow all crawlers access to the entire site

            User-agent: *
            Disallow:

            # Block a specific private folder for all bots
            User-agent: *
            Disallow: /private-admin/

            # Block a specific AI scraper bot completely
            User-agent: GPTBot
            Disallow: /

            # Point to the XML sitemap
            Sitemap: https://example.com     
        """


        #loops over line varible that stores text of exluded paths for website.
        for line in lines:

            #identifies specific persmissions that are not allowed. 
            if line.startswith("Disallow:"):

                #collects parts after permission statement
                parts = line.split(':', 1)

                #collects folder/file name that is part of restircted pathway. 
                path = parts[1].strip()

                #addeds restricited content no to access to list. 
                excluded_paths.append(path)
            else:
                pass
            
        return excluded_paths








        






        













