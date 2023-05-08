import openai
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai.api_key  = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

# Principle 1: write clear and specific instructions

# Tactics:

# Tactic 1: Delimit to distinct parts of the input
text_p1_t1 = f"""
You should express what you want a model to do by \ 
providing instructions that are as clear and \ 
specific as you can possibly make them. \ 
and reduce the chances of receiving irrelevant \ 
This will guide the model towards the desired output, \ 
or incorrect responses. Don't confuse writing a \ 
clear prompt with writing a short prompt. \ 
In many cases, longer prompts provide more clarity \ 
and context for the model, which can lead to \ 
more detailed and relevant outputs.
"""

prompt__p1_t1 = f"""
Summarize the text delimited by triple backticks \ 
into a single sentence.
```{text_p1_t1}```
"""

# Tactic 2: ask for structured output
prompt_p1_t2 = f"""
Generate a list of three made-up book titles along \ 
with their authors and genres. 
Provide them in JSON format with the following keys: 
book_id, title, author, genre.
"""

#Tactic 3: Whether conditions are satisfied
text_p1_t3_1 = f"""
Making a cup of tea is easy! First, you need to get some \ 
water boiling. While that's happening, \ 
grab a cup and put a tea bag in it. Once the water is \ 
hot enough, just pour it over the tea bag. \ 
Let it sit for a bit so the tea can steep. After a \ 
few minutes, take out the tea bag. If you \ 
like, you can add some sugar or milk to taste. \ 
And that's it! You've got yourself a delicious \ 
cup of tea to enjoy.
"""

text_p1_t3_2 = f"""
The sun is shining brightly today, and the birds are \
singing. It's a beautiful day to go for a \ 
walk in the park. The flowers are blooming, and the \ 
trees are swaying gently in the breeze. People \ 
are out and about, enjoying the lovely weather. \ 
Some are having picnics, while others are playing \ 
games or simply relaxing on the grass. It's a \ 
perfect day to spend time outdoors and appreciate the \ 
beauty of nature.
"""

prompt_p1_t3 = f"""
You will be provided with text delimited by triple quotes. 
If it contains a sequence of instructions, \ 
re-write those instructions in the following format:

Step 1 - ...
Step 2 - …
…
Step N - …

If the text does not contain a sequence of instructions, \ 
then simply write \"No steps provided.\"

\"\"\"{text_p1_t3_2}\"\"\"
"""

# Tactic 4: Provide examples
prompt_p1_t4 = f"""
Your task is to answer in a consistent style.

<child>: Teach me about patience.

<grandparent>: The river that carves the deepest \ 
valley flows from a modest spring; the \ 
grandest symphony originates from a single note; \ 
the most intricate tapestry begins with a solitary thread.

<child>: Teach me about resilience.
"""

# Principle 2: Give the model to think

# Tactics:

# Tactic 1: Use delimiters to indicate separate parts of the input
text_p2_t1 = f"""
In a charming village, siblings Jack and Jill set out on \ 
a quest to fetch water from a hilltop \ 
well. As they climbed, singing joyfully, misfortune \ 
struck—Jack tripped on a stone and tumbled \ 
down the hill, with Jill following suit. \ 
Though slightly battered, the pair returned home to \ 
comforting embraces. Despite the mishap, \ 
their adventurous spirits remained undimmed, and they \ 
continued exploring with delight.
"""
# example 1
prompt_p2_t1_1 = f"""
Perform the following actions: 
1 - Summarize the following text delimited by triple \
backticks with 1 sentence.
2 - Translate the summary into Spanish.
3 - List each name in the Spanish summary.
4 - Output a json object that contains the following \
keys: spanish_summary, num_names.

Separate your answers with line breaks.

Text:
```{text_p2_t1}```
"""

#Example 2
prompt_p2_t1_2 = f"""
Your task is to perform the following actions: 
1 - Summarize the following text delimited by 
  <> with 1 sentence.
2 - Translate the summary into Spanish.
3 - List each name in the Spanish summary.
4 - Output a json object that contains the 
  following keys: spanish_summary, num_names.

Use the following format:
Text: <text to summarize>
Summary: <summary>
Translation: <summary translation>
Names: <list of names in Spanish summary>
Output JSON: <json with summary and num_names>

Text: <{text_p2_t1}>
"""

# Tactic 2: Instruct the model to work out its own solution before rushing to a conclusion
prompt_p2_t2_1 = f"""
Determine if the student's solution is correct or not.

Question:
I'm building a solar power installation and I need \
 help working out the financials. 
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost \ 
me a flat $100k per year, and an additional $10 / square \
foot
What is the total cost for the first year of operations 
as a function of the number of square feet.

Student's Solution:
Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
"""
#Note: Incorrect solution but the model returns correct

#Fix:
prompt_p2_t2_2 = f"""
Your task is to determine if the student's solution \
is correct or not.
To solve the problem do the following:
- First, work out your own solution to the problem. 
- Then compare your solution to the student's solution \ 
and evaluate if the student's solution is correct or not. 
Don't decide if the student's solution is correct until 
you have done the problem yourself.

Use the following format:
Question:
```
question here
```
Student's solution:
```
student's solution here
```
Actual solution:
```
steps to work out the solution and your solution here
```
Is the student's solution the same as actual solution \
just calculated:
```
yes or no
```
Student grade:
```
correct or incorrect
```

Question:
```
I'm building a solar power installation and I need help \
working out the financials. 
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost \
me a flat $100k per year, and an additional $10 / square \
foot
What is the total cost for the first year of operations \
as a function of the number of square feet.
``` 
Student's solution:
```
Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
```
Actual solution:
"""

# Model limitations
prompt_limitation = f"""
Tell me about AeroGlide UltraSlim Smart Toothbrush by OpenAi
"""

# Hallucination:
"""
As an AI language model, I do not have personal experiences or opinions. \
However, I can provide you with information about the AeroGlide UltraSlim Smart Toothbrush by OpenAi.
The AeroGlide UltraSlim Smart Toothbrush is a high-tech toothbrush that uses artificial intelligence \
to provide a personalized brushing experience. It is designed to be ultra-slim, making it easy to \
maneuver and reach all areas of the mouth. The toothbrush uses advanced sensors to detect the \
position and movement of the brush head, allowing it to provide real-time feedback on brushing technique.
The toothbrush also connects to a mobile app, which provides personalized coaching and tracks brushing \
habits over time. The app uses machine learning algorithms to analyze brushing data and provide \
recommendations for improving oral hygiene.
The AeroGlide UltraSlim Smart Toothbrush is developed by OpenAi, \
a company that specializes in artificial intelligence and machine learning. \
The toothbrush is designed to be both effective and convenient, making it a \
great choice for anyone looking to improve their oral hygiene.
"""
response = get_completion(prompt_limitation)
print(response)