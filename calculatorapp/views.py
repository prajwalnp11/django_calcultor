
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

import re

def index(request):
    return render(request,'index.html')

def submitquery(request):
    q = request.GET.get('query', '')
    if not q.strip():
        return render(request, 'index.html')

    # Allow only digits, basic arithmetic operators, parentheses, and whitespace
    if re.match(r'^[0-9+\-*/().\s]+$', q):
        try:
            # Preprocess to support implicit multiplication (e.g., 2(3) -> 2*(3))
            processed_q = re.sub(r'(\d)\s*\(', r'\1*(', q)
            processed_q = re.sub(r'\)\s*(\d)', r')*\1', processed_q)
            processed_q = re.sub(r'\)\s*\(', r')*(', processed_q)

            # Evaluate the expression with no global or local namespace builtins for safety
            ans = eval(processed_q, {"__builtins__": None}, {})
            context = {
                'query': q,
                'result': str(ans),
                'error': False
            }
        except Exception as e:
            context = {
                'query': q,
                'result': f"Calculation Error: {str(e)}",
                'error': True
            }
    else:
        context = {
            'query': q,
            'result': "Error: Invalid characters. Use numbers and +, -, *, /, //, (), .",
            'error': True
        }
    return render(request, 'index.html', context)