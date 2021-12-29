from django.http.request import HttpRequest
from django.shortcuts import render
from django.http import HttpResponse
import json
import logging
import openai
import asyncio
import chronological
from chronological import main, read_prompt, gather, fetch_max_search_doc, cleaned_completion

# Create your views here.


def ai_regulations(request):
    if request.method == 'POST':

        user_input = request.POST.get('ai_regulations_input')
        #user_input = input("What technology do you want to regulate? ")
        print(user_input)

        prompt_examples = f"\n\ninput: {user_input}. What are the risks regarding this technology? \n\noutput:"

        prompt_examples2 = f"\n\nMake a list of required regulations to prevent such risks? \n\noutput: Art.1"

        print(prompt_examples)
        print(prompt_examples2)

        async def logic():

            openai.api_key = '< YOUR_API_KEY >'

            risk1 = await cleaned_completion(prompt=prompt_examples, engine="davinci-instruct-beta-v3", max_tokens=50, temperature=0.3, top_p=1, frequency_penalty=0.7, stop=['\n\n'])
            risk2 = await cleaned_completion(prompt=prompt_examples + risk1, engine="davinci-instruct-beta-v3", max_tokens=50, temperature=0.3, top_p=1, frequency_penalty=0.7, stop=['\n\n'])
            risk3 = await cleaned_completion(prompt=prompt_examples + risk2, engine="davinci-instruct-beta-v3", max_tokens=50, temperature=0.5, top_p=1, frequency_penalty=0.7, stop=['\n\n'])
            risk4 = await cleaned_completion(prompt=prompt_examples + risk3, engine="davinci-instruct-beta-v3", max_tokens=100, temperature=0.7, top_p=1, frequency_penalty=0.7, stop=['\n\n'])

            blocks = (risk1, risk2, risk3, risk4)

            # List all risks splitting by new line
            risks = [element.split('\n\n') for element in blocks]

            # print risks as string
            overallrisk = ('\n'.join(['\n'.join(element)
                                      for element in risks]))

            print(overallrisk)

            regulations = []
            for element in blocks:
                regulation = await cleaned_completion(prompt=prompt_examples + element + prompt_examples2, engine="davinci-instruct-beta-v3", max_tokens=100, temperature=0.3, top_p=1, frequency_penalty=0.7, stop=['\n\n'])

                reg = regulation.split("\n\n ")[0]
                regulations.append(reg)

            return(overallrisk, regulations)

        var = asyncio.run(logic())

        overallrisk = var[0]
        regulations = var[1]

        # Return the risk and the regulations on the page
        return render(request, './ai_regulations/ai_regulations.html', {'overallrisk': overallrisk, 'regulations': regulations})

    return render(request, './ai_regulations/ai_regulations.html')
