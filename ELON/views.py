from cgitb import html
from django.http.request import HttpRequest
from django.shortcuts import render
from django.http import HttpResponse
import json
import logging
import openai
import asyncio
import chronological
from chronological import main, read_prompt, gather, fetch_max_search_doc, cleaned_completion
from sqlalchemy import false

# Create your views here.

final_prompt = []


def ai_regulations(request):
    if request.method == 'POST':

        user_input = request.POST.get('ai_regulations_input')
        #user_input = input("What technology do you want to regulate? ")
        print(user_input)

        prompt_examples = f"The following is an interview with Elon Musk. As always, Elon makes punchlines.\n\n Journalist: Welcome Elon! \n\n Elon Musk: Thank you! It's great to be here. \n\n "
        new_input = f"Journalist: {user_input} \n\n Elon Musk:"

        async def logic():
            new_prompt = str(final_prompt)
            prompt = (prompt_examples + new_prompt + new_input)
            print(prompt)
            openai.api_key = '<GPT3_APIKEY>'

            risk1 = await cleaned_completion(prompt=prompt, engine="davinci-instruct-beta-v3", max_tokens=500, temperature=0.9, top_p=1, frequency_penalty=0.7, stop=['Journalist: ', 'Elon Musk: '])
            blocks = (risk1)
            return(blocks)

        var = asyncio.run(logic())

        new_example = f"{new_input} {var}"
        print(new_example)
        final_prompt.append(new_example)

        return render(request, './ai_regulations/ai_regulations.html', {'answer': var, 'final_prompt': final_prompt, 'user_input': user_input})
        # Return final_prompt as a string
        # return HttpResponse(final_prompt)

    return render(request, './ai_regulations/ai_regulations.html')
