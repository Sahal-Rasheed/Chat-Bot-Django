import openai
from django.conf import settings
from django.shortcuts import render


def Chat(request):
    result = None
    queries = None
    api_key = settings.OPENAI_API_KEY
    
    if api_key and  request.method == 'POST':
        openai.api_key = api_key
        query = request.POST.get('input')
        prompt = query
        
        response = openai.Completion.create(
            model = 'text-davinci-003',
            prompt = prompt,
            max_tokens = 2000,
            temperature = 0
        )
        
        result = response['choices'][0]['text']
        
        queries = request.session.get('queries',[])
        queries.append({'query':query, 'result':result})
        request.session['queries'] = queries 

        if len(queries) > 3 and request.user.is_authenticated:
            queries.remove(queries[0])
            
        elif len(queries) >= 3 and not request.user.is_authenticated:
            del request.session['queries']
            return render(request, 'alert.html')
            
    return render(request, 'chat.html', {'result':result, 'queries':queries})


