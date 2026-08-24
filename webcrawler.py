import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import sys
import RequestGuard
import lab20 as combineLinks
import csv
import image_proccessing





def modify_img(url, file_name, flag):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    imgLst = []


    for img in soup.find_all("img"):
        src = img.get("src")
        if src:
            content = fix_links(src, url)
            imgLst.append(content)

    
    for imgUrl in imgLst:
        

        split = imgUrl.split("/")
        name = file_name + split[len(split) - 1]

        response = requests.get(imgUrl)

        with open(name, 'wb') as imgUrl:
            imgUrl.write(response.content)

        image_proccessing.applyfilter(name, flag)
        

        
        #


def plot_data(url, plot_png, output_file):

    response = requests.get(url)
    if response.status_code != 200:
        print("Page doesn't exist")
        return

    soup = BeautifulSoup(response.text, 'html.parser')


    table = soup.find('table', id='CS111-Project4b')
    if not table:
        return

    x_values = []
    y_values = []

    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) < 1:
            continue
        
        try:
            x = float(cells[0].text)
            x_values.append(x)

            
            if not y_values:
                y_values = [[] for _ in range(len(cells) - 1)]

            for i in range(1, len(cells)):
                y = float(cells[i].text)
                y_values[i-1].append(y)
        except ValueError:
            print("Could not convert data to float, skipping row.")
            continue

   
    colors = ['blue', 'green', 'red', 'black']
    for i, y in enumerate(y_values):
        plt.plot(x_values, y, color=colors[i % len(colors)], label=f'Dataset {i+1}')

    plt.savefig(plot_png)
    plt.close()


    
    with open(output_file, 'w', newline='') as out_put_file:
        writer = csv.writer(out_put_file)
        for row in zip(x_values, *y_values):
            writer.writerow(row)

    
    


def fix_links(current_href, parentDomain): ## cheks whether passed url is constrcuted properly.

    domain = combineLinks.get_domain(parentDomain)

    if current_href.startswith("https") or current_href.startswith("http"):  ### FULL URLS WITH POUNDS

        if "#" in current_href:
            return current_href.split("#")[0] 
        else:
            return current_href 
    
    elif current_href.startswith("/"):  ### Relative links
        return combineLinks.combine_paths(domain, current_href) 

    elif current_href.startswith("#"): ###### # Fragment
        
        return parentDomain

    else: ## Relative page
        return combineLinks.combine_urls(parentDomain, current_href) 
        



def count_links(inputURL, output1, output2):

    linkstoVist = []
    timesAppeared = {}
    guard = RequestGuard.RequestGuard(inputURL)
    linkstoVist.append(inputURL)

    
    while linkstoVist:

        currentLink = linkstoVist.pop()

        if currentLink in timesAppeared: ### check if I've visited link
            timesAppeared[currentLink] += 1
            continue
        
        timesAppeared[currentLink] = 1

        if guard.can_follow_link(currentLink):
            print(currentLink)

            response = requests.get(currentLink)
            soup = BeautifulSoup(response.text, "html.parser")
            
            for tag in soup.find_all("a"): #### FIRST LAYER OF LINK gets all tags on page

                href = tag.get("href") ### The links on a page
                fixedLink = fix_links(href, currentLink ) ### Fixes the url if not complete
                print(fixedLink)
                linkstoVist.append(fixedLink)

                print(f"Orginal Link: {href}\n Fixed link: {fixedLink}\n")

    print(timesAppeared)


    BINSIZE = []
    VAlUES = timesAppeared.values()
    max_range = max(timesAppeared.values()) + 1
    

    for i in range(1, max_range + 1):
        BINSIZE.append(i)


    NEWVALUES, NEWBINS, temp = plt.hist(VAlUES,BINSIZE)
    plt.savefig(output1)
    plt.close()

    with open(output2, "w") as output_file2:
        for i in range(len(NEWVALUES)):
            output_file2.write(f"{NEWBINS[i]},{NEWVALUES[i]}\n")




def main(argv):

    flag = argv[1]
    url = argv[2]
    elem1 = argv[3]
    elem2 = argv[4]


    if flag == "-c":
        count_links(url, elem1, elem2)

    elif flag == "-p":
        plot_data(url, elem1, elem2)

    elif flag == "-i":
        modify_img(url, elem1, elem2)
        pass
        #argv[3] == "-s" or "-g" or "-f" or "-m"


def test_flags(argv):
    # -p http://cs111.byu.edu/Projects/project04/assets/data.html data.png data.csv
    # -i http://cs111.byu.edu/Projects/project04/assets/images.html grey_ -g
    # -c <url> <output filename 1> <output filename 2>

    if len(argv) > 3:

        flag = argv[1]
        second_flag = argv[4]
        
        if flag == "-c":   #COUNTING LINKS
            return True
        
        elif flag == "-p":  #PLOT AND EXTRACT DATA
            return True
        
        elif flag == "-i":  #FIND AND MANIPULATE IMAGE
            if second_flag == "-s" or second_flag == "-m" or second_flag == "-g" or second_flag == "-f":
                return True
    
        
    return False
    

if __name__ == "__main__":
   
    if test_flags(sys.argv):
        main(sys.argv)
    else:
        print("Invalid arguments")

    # v = ["webCraweler", "-i"," http://cs111.byu.edu/Projects/project04/assets/images.html","grey_", "-f"]
   
    # print(len(v))
    # if test_flags(v):
    #     main(v)
    # else:
    #     print("Invalid arguments")








