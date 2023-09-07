# World_glimpse

Hey there! Welcome to the repo of my final proyect of the Ironhack Data Analytics course in Madrid: World Glimpse.

World Glimpse is an api built-on project with a front-end to explore different aspects of world countries and regions to get an overall idea of their characteristics and current situation. Some aspects that are included are:

+ General: Main spoken langguages, demographic population, size.
+ Social: Well-being and social indicators, such as the poverty index or the sexism rating.
+ Political: Government system, on-going conflicts if existing, etc.
+ Economical: relative power adquisition indexes such as PPP, economic proportions.

A subsection of news for each country is also included, based on calls to the World News API.

# About the API:

The API built to feed the front-end was made with FastAPI. It was connected to a MySQL database by classes mapped to the tables through sqlalchemy.
The diverse endpoints created were meant to provide specific information to the front, and are described in comments along the code of the main.py file.

Here is an example of an end point that makes a request to two other APIs for a specific country id; to wikipedia for a summary and to restcountries for general data:

![image](https://github.com/MartaRggc/world_glimpse_api/assets/137410300/5f1b1ddc-8774-4af5-9a1a-bbed1ceb81d0)

