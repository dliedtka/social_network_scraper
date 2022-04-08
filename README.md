# "Social Network" Scraper

UPDATE: Doing this will get your account suspended/banned, did not read the ToS... have removed all references to the website.

This is an attempt to scrape profile pictures off of a certain career-oriented social media site to create a small dataset for CNN gender recognition based on the types of pictures people put as their profile pictures. 

The script will search for the [100 most common male first names and 100 most common female names of the last 100 years](https://www.ssa.gov/oact/babynames/decades/century.html) and grab the profile pictures of the top 3 results for each name, so I recommend using an anonymous account to avoid grabbing pictures of people you know (you need to provide an "account.txt" file with your account email on the first line and password on the second line). We assume that pictures found using a "male" name are male and pictures found using a "female" name are female; probably a bad assumption, but some error is fine for my purposes. Ideally I would've just dynamically found profile links and gotten genders from people with their pronouns on their profile, but as mentioned below grabbing tags from the HTML was a pain after logging in.  Obviously, you can edit the name lists to get more/less pictures.

I wanted to use Beautiful Soup, but that ended up being a headache because I guess most social media companies these days use JavaScript to obscure their pages and make them harder to scrape. To work around this I did the scraping in a few steps:

1. Create a list of profile links.
2. Revisit the profile links and use JavaScript to grab each profile picture link.
3. Download each profile picture using its link.

There is some variability obviously based on internet connectivity, so you might want to adjust the length of the sleeps. You won't get all 600 pictures (some profiles don't have pictures, sometimes you fail to grab the profile, it seems like sometimes the JavaScript fails), but it's designed so missing one shouldn't cause you to miss the rest. Getting the profile links should take like an hour to run, and getting the picture links should take like 15 minutes.

This logically should probably be a Jupyter notebook, but I just made each step runnable with command line args.


## Install

- selenium 
- webdriver_manager


## To Do

- Implement downloading of pictures.
