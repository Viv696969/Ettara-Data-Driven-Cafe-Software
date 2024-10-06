
# Ettara AI and Data Driven Cafe Software

## Problem Statement
Imagine a bustling coffee shop eager to elevate its game in the highly
competitive market. To achieve this, the problem statement is to harness the
power of data analytics and AI. The coffee shop wishes to revolutionize its
operations, decision-making processes, and customer engagement
strategies. Keep high focus on documentation, git version control, good
coding practices, making a proper ReadMe and so on.


### Core objectives:
1. Insight Extraction: Analyze Customer Reviews and Competitor Data.
- Utilize web scraping techniques to extract user reviews from platforms like Zomato and Swiggy for the Target Restaurant (Ettarra Coffee).
- Analyze customer reviews to understand the strengths and weaknesses of the coffee shop and its competitors.
- Compare and contrast competitors' (Similar restaurants in the region) data to identify areas for improvement and strategic opportunities. Example: If you go to Zomato and search biryanis in the search bar then the top 10 competitors of that region are shown based on the relevance. Now with this competitor basket, curate the summary of how their business is doing.

2. Market Basket Analysis: Understand Customer Buying Patterns
- Analyzing transaction data to identify rules/patterns in customer purchasing behavior.
- Determine associations between products using market basket analysis to optimize menu offerings.

3. AI Recommender System: Enhance Customer Experience
- Developed a recommender system for menu items based on customer preferences.

4. Analytics Dashboard Development: Provide Comprehensive Business Insights
- Create a dynamic dashboard that consolidates insights from customer reviews, competitor analysis, and market basket analysis.
- Visualize key performance indicators, customer sentiment trends, and sales patterns for quick decision-making.

5. Sales Analysis:
- Examine sales data to pinpoint intervals with reduced transaction activity, such as during extended weekends when patrons usually travel to other cities, and communicate these findings to the management. This information can then be utilized to launch targeted seasonal promotions.
- Also peruse purchases data and see how those insights can be used in these targeted seasonal promotions.

## Technology Stack
[![My Skills](https://skillicons.dev/icons?i=py,django,fastapi,mysql,gmail,aws,git,github)](https://skillicons.dev)

### Other Libraries
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![hf](https://img.shields.io/badge/-HuggingFace-FDEE21?style=for-the-badge&logo=HuggingFace&logoColor=black)
![hf](https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=fff&style=for-the-badge)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

## Features
* Supports JWT Authentication.
* OTP Verification Using JWT and Cryptography Support.
* Email Verification Using JWT and Cryptography Support.
* Recommendation System (Content Based Filtering) Based on user history and specific product.
* Web Scraping of Reviews from Zomato and JustDial.
* Market Basket Analysis based on Users buying habits.
* Sentiment Analysis Pipeline and Dashboard for analyzing customer feedback and understanding user emotions and make data driven decisions.
* Low latency dashboard API's for data driven decisions.
* Offline Store Features.
   - Add to cart
   - Create order for customer.
   - Place order for customer.

* Online Store
   - Create User using JWT.
   - Add to Cart.
   - Place order.
   - Send ocational Mails.

### Best practices used
- Used Cryptography Keys using Fernet Library of python to encrypt and decrypt Jwt tokens.
- Modular approach: Divided the software into various components.
- Storing encryption and JWT secret keys along with DB and api keys in Env files for security.
- Normalized Database Design.

### Folder Structure
![alt text](https://github.com/Viv696969/Ettara-Data-Driven-Cafe-Software/blob/main/folder_structure_ettara.png?raw=true)

## Documentation
Click here to view the documentation.

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SECRET`
`DEBUG`
`DATABASE_NAME`
`DATABASE_USER`
`DATABASE_PASSWORD`
`DATABASE_PORT`
`EMAIL`
`EMAIL_PASSWORD`
`HUGGING_FACE_TOKEN`

## Run Locally

```bash
  git clone https://github.com/Viv696969/Ettara-Data-Driven-Cafe-Software.git
  python -m env ettara_env
  ettara_env\Scripts\activate
  pip install -r requirements.txt
```

## 🔗 Links
[![medium](https://img.shields.io/badge/Medium-000?logo=medium&logoColor=fff&style=for-the-badge)](https://medium.com/@vivekchouhan69696)

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vivek-chouhan/)

[![github](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=fff&style=for-the-badge)](https://github.com/Viv696969)

[![geeksforgeeks](https://img.shields.io/badge/GeeksforGeeks-2F8D46?logo=geeksforgeeks&logoColor=fff&style=for-the-badge)](https://www.geeksforgeeks.org/user/chouhanvlxst/)

[![leetcode](https://img.shields.io/badge/LeetCode-FFA116?logo=leetcode&logoColor=fff&style=for-the-badge)](https://leetcode.com/u/vivekchouhan69696/)





## My current status
👩‍💻 I'm currently working on medical based project and and an Ai platform named CSGPT.

🧠 I'm currently learning AWS,Java,Langchain.

👯‍♀️ I'm looking to collaborate on Backend and data science projects.

🤔 I'm looking for help with Job and internship Search.

💬 Ask me about Python,Data science,Machine Learning etc.

⚡️ Fun fact: Nothing is Impossible.




    


